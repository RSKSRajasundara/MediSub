from pathlib import Path

import streamlit as st

from document_checker import (
    check_cover_letter,
    check_medical_certificate,
    check_request_form,
    extract_text,
)


BASE_DIR = Path(__file__).resolve().parent
if BASE_DIR.name == "pages":
    BASE_DIR = BASE_DIR.parent
DOWNLOAD_DIR = BASE_DIR / "downloads"

st.set_page_config(page_title="MediSub Documents", page_icon="📄", layout="centered")
st.markdown(
    """
    /* Keep every page component inside the same width */
[data-testid="stAppViewContainer"] .main .block-container,
.stMainBlockContainer {
    width: 100% !important;
    max-width: 1200px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 28px !important;
    padding-right: 28px !important;
}

/* Make navigation use the complete content width */
[data-testid="stRadio"] {
    display: block !important;
    width: 100% !important;
}

[data-testid="stRadio"] > div {
    display: block !important;
    width: 100% !important;
}

[data-testid="stRadio"] div[role="radiogroup"] {
    display: grid !important;
    grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
    width: 100% !important;
    max-width: 100% !important;
}

/* Improve home-page spacing */
.hero {
    max-width: 720px !important;
    margin: 2.8rem auto 1.8rem !important;
}

.hero h1 {
    max-width: 680px;
    margin: 0.4rem auto 0.9rem !important;
}

.hero .lead {
    max-width: 600px !important;
}

/* Keep the three cards aligned */
[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}
    <style>
    :root {
        --teal: #0E7C7B;
        --violet: #6D4AFF;
        --paper: #F6F7F9;
        --ink: #151A21;
        --slate: #5B6472;
        --line: #E4E7EC;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 12% -15%,
                #E3F4F3 0%,
                transparent 42%
            ),
            radial-gradient(
                circle at 100% -5%,
                #EEEAFF 0%,
                transparent 38%
            ),
            #F6F7F9;

        color: #151A21;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp span {
        color: #151A21;
    }

    [data-testid="stCaptionContainer"] p {
        color: #5B6472 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E4E7EC;
    }

    [data-testid="stSidebar"] * {
        color: #151A21;
    }

    button[data-baseweb="tab"] p {
        color: #5B6472 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #0E7C7B !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #151A21;
    }

    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 10px;
    }

    .doc-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 18px;
        padding: 18px;
        margin: 12px 0;
        color: #151A21;
    }

    .status {
        border-radius: 999px;
        padding: 5px 11px;
        font-weight: 600;
        display: inline-block;
    }

    .ready {
        background: #E3F6EF;
        color: #12855F !important;
    }

    .warning {
        background: #FDF2E2;
        color: #8A5C15 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,

)

st.title("Prepare and check documents")
st.caption("Download the templates, complete the papers, obtain required signatures, then upload clear scans or photos.")

prepare_tab, upload_tab = st.tabs(["1. Prepare documents", "2. Upload and check"])

with prepare_tab:
    st.subheader("Medical Approval Request Form")
    st.write("Print both pages. Complete the student sections on page 1. Do not complete the Medical Centre or office-only sections yourself.")
    form_path = DOWNLOAD_DIR / "Request-form-for-Medical-Approval.pdf"
    if form_path.exists():
        st.download_button("Download official request form", form_path.read_bytes(), form_path.name, "application/pdf")

    st.subheader("Cover letter")
    st.write("Address the letter to the University Medical Officer and route it through the required Dean, Assistant Registrar and Head of Department. Confirm the exact roles with your faculty, then obtain every required approval before upload.")
    letter_path = DOWNLOAD_DIR / "MediSub-Cover-Letter-Template.docx"
    if letter_path.exists():
        st.download_button("Download cover-letter template", letter_path.read_bytes(), letter_path.name)

    with st.expander("How to complete the letter"):
        st.markdown("""
        1. Replace every square-bracket placeholder.
        2. State the absence reason, dates/period, and the action requested.
        3. Keep the medical details brief; include only what the university requires.
        4. Print and sign the letter.
        5. Take it through every role listed under **Through** and obtain each required signature, initial, or stamp.
        6. Scan or photograph the full page in good light without cutting off edges.
        """)

    st.info("The second official form has not been supplied yet. Add its verified template and checking rules before enabling that upload.")

with upload_tab:
    st.warning("This checker finds possible omissions. It does not authenticate signatures, validate medical evidence, or approve a submission.")

    request_file = st.file_uploader("Completed request form - upload page images separately", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    r1 = st.checkbox("All student and certificate fields are completed")
    r2 = st.checkbox("At least one absence row is completed")
    r3 = st.checkbox("The student signature is present")
    r4 = st.checkbox("The Assistant Registrar date and signature are present")
    r5 = st.checkbox("Both pages are included")

    letter_file = st.file_uploader("Signed and routed cover letter", type=["jpg", "jpeg", "png"])
    l1 = st.checkbox("Letter identity details are correct")
    l2 = st.checkbox("Absence period and requested action are stated")
    l3 = st.checkbox("The student signature is present on the letter")
    l4 = st.checkbox("Every required routing approval is present")

    certificate_file = st.file_uploader("Medical certificate or report", type=["jpg", "jpeg", "png"])
    m1 = st.checkbox("Identity matches the request form")
    m2 = st.checkbox("Issue date and recommended absence period are visible")
    m3 = st.checkbox("Practitioner signature and official stamp are visible")

    if st.button("Check uploaded documents", type="primary"):
        results = []
        try:
            if request_file:
                request_text = "\n".join(extract_text(f.getvalue()) for f in request_file)
                results.append(check_request_form(request_text, {
                    "student_fields": r1, "absence_rows": r2, "student_signature": r3,
                    "assistant_registrar": r4, "two_pages": r5,
                }))
            else:
                st.error("Request form is missing.")

            if letter_file:
                results.append(check_cover_letter(extract_text(letter_file.getvalue()), {
                    "identity": l1, "period": l2, "student_signature": l3, "routing_approvals": l4,
                }))
            else:
                st.error("Cover letter is missing.")

            if certificate_file:
                results.append(check_medical_certificate(extract_text(certificate_file.getvalue()), {
                    "identity": m1, "period": m2, "signature_stamp": m3,
                }))
            else:
                st.error("Medical certificate or report is missing.")

            for result in results:
                css = "ready" if result.status == "Ready for staff review" else "warning"
                st.markdown(f'<div class="doc-card"><b>{result.document_type}</b><br><span class="status {css}">{result.status}</span></div>', unsafe_allow_html=True)
                for item in result.passed:
                    st.success(item)
                for item in result.warnings:
                    st.warning(item)
                for item in result.manual_checks:
                    st.info(item)
        except RuntimeError as exc:
            st.error(f"OCR is not available: {exc}. Install Tesseract and pytesseract, then try again.")
