from pathlib import Path

import streamlit as st

try:
    from document_checker import (
        check_cover_letter,
        check_medical_certificate,
        check_request_form,
        extract_text,
    )
except ImportError:
    check_cover_letter = None


BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"


def render_documents_page() -> None:
    st.title("Prepare and check documents")
    st.markdown(
        '<p class="page-lead">Download the templates, complete the papers and upload clear scans for a basic completeness check.</p>',
        unsafe_allow_html=True,
    )
    prepare_tab, upload_tab = st.tabs(["1. Prepare documents", "2. Upload and check"])

    with prepare_tab:
        left, right = st.columns(2)
        with left:
            st.markdown('<div class="doc-card"><span class="pill pill-teal">Required form</span><h3>Medical Approval Request Form</h3><p>Complete only the student sections and obtain the required official signatures.</p></div>', unsafe_allow_html=True)
            form_path = DOWNLOAD_DIR / "Request-form-for-Medical-Approval.pdf"
            if form_path.exists():
                st.download_button("Download official request form", form_path.read_bytes(), form_path.name, "application/pdf", use_container_width=True)
            else:
                st.info(f"Add {form_path.name} to the downloads folder.")
        with right:
            st.markdown('<div class="doc-card"><span class="pill pill-teal">Letter</span><h3>Cover letter</h3><p>State the absence period and route the letter through the required faculty officials.</p></div>', unsafe_allow_html=True)
            letter_path = DOWNLOAD_DIR / "MediSub-Cover-Letter-Template.docx"
            if letter_path.exists():
                st.download_button("Download cover-letter template", letter_path.read_bytes(), letter_path.name, use_container_width=True)
            else:
                st.info(f"Add {letter_path.name} to the downloads folder.")
        with st.expander("How to complete the cover letter"):
            st.markdown("1. Replace every placeholder.\n2. Include your identity and absence dates.\n3. State the requested action.\n4. Sign the letter.\n5. Obtain every required approval.\n6. Scan the complete page clearly.")

    with upload_tab:
        st.warning("The checker identifies possible omissions only. It cannot authenticate signatures, validate evidence or approve a submission.")
        request_files = st.file_uploader("Completed request form — upload both page images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        with st.expander("Request-form manual checks", expanded=False):
            r1 = st.checkbox("Student and certificate fields are completed")
            r2 = st.checkbox("At least one absence row is completed")
            r3 = st.checkbox("Student signature is present")
            r4 = st.checkbox("Assistant Registrar date and signature are present")
            r5 = st.checkbox("Both pages are included")

        letter_file = st.file_uploader("Signed and routed cover letter", type=["jpg", "jpeg", "png"])
        with st.expander("Cover-letter manual checks", expanded=False):
            l1 = st.checkbox("Identity details are correct")
            l2 = st.checkbox("Absence period and requested action are stated")
            l3 = st.checkbox("Student signature is present on the letter")
            l4 = st.checkbox("Required routing approvals are present")

        certificate_file = st.file_uploader("Medical certificate or report", type=["jpg", "jpeg", "png"])
        with st.expander("Medical-document manual checks", expanded=False):
            m1 = st.checkbox("Identity matches the request form")
            m2 = st.checkbox("Issue date and absence period are visible")
            m3 = st.checkbox("Practitioner signature and official stamp are visible")

        if st.button("Check uploaded documents", type="primary"):
            if check_cover_letter is None:
                st.error("document_checker.py could not be loaded. Keep it beside app.py.")
                return
            results = []
            try:
                if request_files:
                    text = "\n".join(extract_text(file.getvalue()) for file in request_files)
                    results.append(check_request_form(text, {"student_fields": r1, "absence_rows": r2, "student_signature": r3, "assistant_registrar": r4, "two_pages": r5}))
                else:
                    st.error("Request form is missing.")
                if letter_file:
                    results.append(check_cover_letter(extract_text(letter_file.getvalue()), {"identity": l1, "period": l2, "student_signature": l3, "routing_approvals": l4}))
                else:
                    st.error("Cover letter is missing.")
                if certificate_file:
                    results.append(check_medical_certificate(extract_text(certificate_file.getvalue()), {"identity": m1, "period": m2, "signature_stamp": m3}))
                else:
                    st.error("Medical certificate or report is missing.")

                for result in results:
                    st.markdown(f'<div class="doc-card"><h3>{result.document_type}</h3><span class="status">{result.status}</span></div>', unsafe_allow_html=True)
                    for item in result.passed:
                        st.success(item)
                    for item in result.warnings:
                        st.warning(item)
                    for item in result.manual_checks:
                        st.info(item)
            except RuntimeError as exc:
                st.error(f"OCR is not available: {exc}")
