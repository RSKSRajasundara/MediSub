"""OCR-assisted completeness checks for MediSub documents.

The module detects visible text and combines it with the student's manual
confirmations. It does not authenticate signatures, stamps, identities, or
medical evidence, and it never approves a submission.
"""

from dataclasses import dataclass
from io import BytesIO
import os
import re
import shutil
from typing import Mapping

from PIL import Image, ImageEnhance, ImageOps

@dataclass(frozen=True)
class CheckResult:
    document_type: str
    status: str
    passed: list[str]
    warnings: list[str]
    manual_checks: list[str]


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _manual_value(checks: Mapping[str, bool], key: str) -> bool:
    return bool(checks.get(key, False))


def _tesseract_command() -> str:
    configured = os.getenv("TESSERACT_CMD")
    candidates = (
        configured,
        shutil.which("tesseract"),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    )
    for candidate in candidates:
        if candidate and (os.path.isfile(candidate) or shutil.which(candidate)):
            return candidate
    raise RuntimeError(
        "Tesseract OCR is not installed. Install Tesseract and either add it "
        "to PATH or set TESSERACT_CMD to tesseract.exe."
    )


def _result(
    document_type: str,
    passed: list[str],
    warnings: list[str],
    manual_checks: list[str],
) -> CheckResult:
    status = "Ready for staff review" if not warnings else "Needs correction"
    return CheckResult(document_type, status, passed, warnings, manual_checks)


def extract_text(image_bytes: bytes) -> str:
    """Extract text from a JPG, JPEG, or PNG image using Tesseract OCR."""
    if not image_bytes:
        raise ValueError("The uploaded image is empty.")

    try:
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = _tesseract_command()
        image = Image.open(BytesIO(image_bytes)).convert("L")
        image = ImageOps.autocontrast(image)
        image = ImageEnhance.Contrast(image).enhance(1.5)
        return pytesseract.image_to_string(image, config="--psm 6").strip()
    except ImportError as exc:
        raise RuntimeError(
            "pytesseract is not installed. Install the project requirements."
        ) from exc
    except RuntimeError:
        raise
    except Exception as exc:
        if exc.__class__.__name__ == "TesseractNotFoundError":
            raise RuntimeError(
                "Tesseract OCR could not be started. Check TESSERACT_CMD or PATH."
            ) from exc
        if isinstance(exc, (OSError, ValueError)):
            raise RuntimeError(
                "The uploaded image could not be opened. Upload a JPG, JPEG, or PNG image."
            ) from exc
        raise RuntimeError("The uploaded image could not be processed.") from exc


def check_request_form(text: str, checks: Mapping[str, bool]) -> CheckResult:
    clean = _normalise(text)
    passed: list[str] = []
    warnings: list[str] = []

    if len(clean) >= 80:
        passed.append("Readable text was detected on the request form.")
    else:
        warnings.append("Very little text was detected. Upload clearer images of both pages.")

    if _contains_any(clean, ("medical approval", "medical certificate", "student", "registration")):
        passed.append("Request-form wording was detected.")
    else:
        warnings.append("The image could not be confidently identified as the medical request form.")

    required = {
        "student_fields": "Confirm that the student and certificate fields are completed.",
        "absence_rows": "Complete at least one absence row.",
        "student_signature": "Add the student's signature.",
        "assistant_registrar": "Obtain the Assistant Registrar date and signature.",
        "two_pages": "Upload both pages of the request form.",
    }
    for key, message in required.items():
        if _manual_value(checks, key):
            passed.append(message.replace("Confirm that ", "Confirmed: ").replace("Complete ", "Completed: ").replace("Add ", "Confirmed: ").replace("Obtain ", "Confirmed: ").replace("Upload ", "Confirmed: "))
        else:
            warnings.append(message)

    manual = [
        "Staff must verify the identity details, handwriting, signatures, dates and official sections.",
        "OCR does not confirm that the information is genuine or accurate.",
    ]
    return _result("Medical Approval Request Form", passed, warnings, manual)


def check_cover_letter(text: str, checks: Mapping[str, bool]) -> CheckResult:
    clean = _normalise(text)
    passed: list[str] = []
    warnings: list[str] = []

    if len(clean) >= 60:
        passed.append("Readable text was detected on the cover letter.")
    else:
        warnings.append("Very little cover-letter text was detected. Upload a clearer image.")

    if _contains_any(clean, ("medical officer", "medical", "absence", "dean", "registrar")):
        passed.append("Medical-submission wording was detected in the letter.")
    else:
        warnings.append("The image could not be confidently identified as a medical-submission cover letter.")

    required = {
        "identity": "Confirm that the identity details are correct.",
        "period": "State the absence period and requested action.",
        "student_signature": "Add the student's signature to the letter.",
        "routing_approvals": "Obtain every required routing approval.",
    }
    for key, message in required.items():
        if _manual_value(checks, key):
            passed.append("Confirmed: " + message[0].lower() + message[1:].rstrip("."))
        else:
            warnings.append(message)

    manual = [
        "Staff must verify the named student, dates, signatures and routing approvals.",
        "The checker cannot decide whether the stated reason is acceptable.",
    ]
    return _result("Cover Letter", passed, warnings, manual)


def check_medical_certificate(text: str, checks: Mapping[str, bool]) -> CheckResult:
    clean = _normalise(text)
    passed: list[str] = []
    warnings: list[str] = []

    if len(clean) >= 40:
        passed.append("Readable text was detected on the medical document.")
    else:
        warnings.append("Very little text was detected. Upload a clearer certificate or report.")

    if _contains_any(clean, ("medical certificate", "hospital", "doctor", "medical officer", "patient")):
        passed.append("Medical-document wording was detected.")
    else:
        warnings.append("The image could not be confidently identified as a medical certificate or report.")

    required = {
        "identity": "Confirm that the identity matches the request form.",
        "period": "Confirm that the issue date and recommended absence period are visible.",
        "signature_stamp": "Confirm that the practitioner signature and official stamp are visible.",
    }
    for key, message in required.items():
        if _manual_value(checks, key):
            passed.append("Confirmed: " + message[0].lower() + message[1:].rstrip("."))
        else:
            warnings.append(message)

    manual = [
        "Authorized staff must verify the practitioner, signature, stamp, dates and medical evidence.",
        "The checker does not diagnose illness or validate the medical claim.",
    ]
    return _result("Medical Certificate or Report", passed, warnings, manual)
