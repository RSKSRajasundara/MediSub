from pathlib import Path
from html import escape
import streamlit as st

from styles import apply_styles
from documents import render_documents_page

try:
    from question_service import predict_question
except ImportError:
    predict_question = None

st.set_page_config(
    page_title="MediSub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)



CATEGORY_GUIDANCE = {
    "PROCESS_GUIDANCE": {
        "title": "Medical-submission process",
        "answer": "Confirm the procedure, obtain the reference number, prepare the required documents and submit them through the correct university office.",
        "next_step": "Open Documents and review the required forms.",
    },
    "REFERENCE_NUMBER_HELP": {
        "title": "Reference-number guidance",
        "answer": "Contact the University Medical Centre on the required day and follow its official instructions to obtain your reference number.",
        "next_step": "Confirm the reference-number procedure with the Medical Centre.",
    },
    "DOCUMENT_REQUIREMENTS": {
        "title": "Required documents",
        "answer": "Prepare the Medical Approval Request Form, cover letter and supporting medical certificate or report. Complete only the student sections.",
        "next_step": "Download and check the documents on the Documents page.",
    },
    "MA_SUBMISSION_HELP": {
        "title": "Submission guidance",
        "answer": "After completing the documents and obtaining the required signatures, submit them to the confirmed Medical Assistant or responsible faculty office.",
        "next_step": "Confirm the submission location with your faculty.",
    },
    "OUT_OF_SCOPE": {
        "title": "Outside MediSub's scope",
        "answer": "MediSub only provides guidance about the university medical-submission process.",
        "next_step": "Ask about the process, reference number, documents or submission point.",
    },
}


def change_page(page_name: str) -> None:
    st.session_state.page = page_name


def clear_question() -> None:
    st.session_state.medical_question = ""


def render_header() -> None:
    st.markdown(
        '<div class="brand"><span class="brand-mark">M</span>'
        '<span class="brand-name">MediSub</span></div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<p class="footer">MediSub — academic prototype for medical-submission guidance</p>',
        unsafe_allow_html=True,
    )


def home_page() -> None:
    st.markdown(
        '<section class="hero">'
        '<p class="eyebrow">Medical submission guidance</p>'
        '<h1>Prepare your medical submission correctly</h1>'
        '<p class="lead">Ask a question, prepare the required documents and check every requirement before submission.</p>'
        '</section>',
        unsafe_allow_html=True,
    )
    # Home-page buttons
    empty_left, action_1, action_2, empty_right = st.columns(
        [1, 1.2, 1.2, 1]
    )

    with action_1:
        st.button(
            "Ask a question",
            type="primary",
            use_container_width=True,
            on_click=change_page,
            args=("Ask a Question",),
        )

    with action_2:
        st.button(
            "Check requirements",
            use_container_width=True,
            on_click=change_page,
            args=("Checklist",),
        )

    # Feature cards
    col1, col2, col3 = st.columns(3)

    cards = [
        (
            col1,
            "teal-edge",
            "01",
            "AI question guidance",
            "Get a predicted category, confidence score and suggested next step.",
        ),
        (
            col2,
            "violet-edge",
            "02",
            "Document preparation",
            "Download templates and check scanned documents for possible missing information.",
        ),
        (
            col3,
            "coral-edge",
            "03",
            "Submission checklist",
            "Track the important requirements before submitting documents to staff.",
        ),
    ]

    for column, edge, number, title, description in cards:
        with column:
            st.markdown(
                f"""
                <div class="card {edge}">
                    <div class="icon-box">{number}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


    st.markdown(
        '<div class="notice notice-teal"><strong>Privacy notice:</strong> '
        'Use fictional or redacted documents for prototype demonstrations. Do not upload real sensitive medical information.</div>',
        unsafe_allow_html=True,
    )


def ask_page() -> None:
    st.title("Ask a question")
    st.markdown('<p class="page-lead">Describe your medical-submission question in plain language.</p>', unsafe_allow_html=True)

    question = st.text_area(
        "Your question",
        placeholder="Example: What documents do I need to submit?",
        height=120,
        key="medical_question",
    )
    st.markdown(
        '<div class="chips"><span>How do I get a reference number?</span>'
        '<span>Which documents are required?</span><span>Where should I submit them?</span></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 4])
    with left:
        run_prediction = st.button("Get guidance", type="primary", use_container_width=True)
    with right:
        st.button("Clear", key="clear_question_button", on_click=clear_question)

    if not run_prediction:
        return
    if not question.strip():
        st.warning("Please enter a question first.")
        return
    if predict_question is None:
        st.error("question_service.py could not be loaded. Keep it beside app.py.")
        return

    try:
        prediction = predict_question(question)
        category = prediction["category"]
        confidence = float(prediction["confidence"])
        needs_referral = prediction["needs_referral"]
        model_answer = ""
        percent = round(confidence * 100 if confidence <= 1 else confidence)
        details = CATEGORY_GUIDANCE.get(category, CATEGORY_GUIDANCE["OUT_OF_SCOPE"])
        answer = model_answer or details["answer"]

        st.markdown('<div class="section-divider"></div><p class="result-label">Suggested result</p>', unsafe_allow_html=True)
        result_col, confidence_col = st.columns([3, 1])
        with result_col:
            st.markdown(
                f'<div class="result-card"><span class="pill pill-teal">{escape(details["title"])}</span>'
                f'<p class="result-answer">{escape(answer)}</p>'
                f'<div class="notice notice-teal"><strong>Recommended action:</strong> {escape(details["next_step"])}</div></div>',
                unsafe_allow_html=True,
            )
        with confidence_col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Model confidence", f"{percent}%")
            st.progress(max(0, min(percent, 100)) / 100)
            st.caption(f"Category: {category}")
            st.markdown('</div>', unsafe_allow_html=True)
        if needs_referral:
            st.warning("The model is not fully certain. Add more detail or confirm the answer with authorized staff.")
    except Exception as exc:
        st.error(f"The question could not be checked: {exc}")


def checklist_page() -> None:
    st.title("Submission checklist")
    st.markdown('<p class="page-lead">Complete these checks before submitting your medical documents.</p>', unsafe_allow_html=True)
    st.markdown(
        '<div class="step-row"><div><b>1</b><span>Get reference</span></div>'
        '<div><b>2</b><span>Prepare documents</span></div>'
        '<div><b>3</b><span>Submit to staff</span></div></div>',
        unsafe_allow_html=True,
    )
    items = [
        "I obtained or confirmed the required reference number.",
        "I completed the student sections of the request form.",
        "I prepared and signed the cover letter.",
        "I obtained the required signatures, initials or stamps.",
        "I attached the supporting medical certificate or report.",
        "I checked that names, dates and document images are readable.",
        "I confirmed the correct Medical Assistant or submission office.",
    ]
    completed = sum(st.checkbox(item, key=f"requirement_{i}") for i, item in enumerate(items))
    st.markdown(f'<p class="progress-label"><strong>{completed} of {len(items)}</strong> requirements completed</p>', unsafe_allow_html=True)
    st.progress(completed / len(items))
    missing = len(items) - completed
    if missing == 0:
        st.success("Your checklist is complete. Staff must still perform the official review.")
    else:
        st.markdown(f'<div class="notice notice-coral"><strong>{missing} requirement(s) remaining.</strong> Complete them before submission.</div>', unsafe_allow_html=True)
    st.markdown('<div class="notice notice-amber"><strong>Reminder:</strong> Confirm all deadlines and procedures with the responsible university office.</div>', unsafe_allow_html=True)


def about_page() -> None:
    st.title("About and help")
    st.markdown('<p class="page-lead">MediSub gives initial administrative guidance for the university medical-submission process.</p>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.subheader("How to use MediSub")
        st.markdown("1. Ask your question in plain language.\n\n2. Review the category and confidence score.\n\n3. Prepare documents and complete the checklist.")
    with right:
        st.subheader("What MediSub can do")
        st.markdown("✅ Suggest a question category\n\n✅ Provide a recommended next step\n\n✅ Check possible document omissions\n\n❌ Give medical advice or approve a submission")
    st.subheader("Common questions")
    with st.expander("Can MediSub approve my submission?"):
        st.write("No. Only authorized university staff can review and approve it.")
    with st.expander("Can MediSub issue a reference number?"):
        st.write("No. Contact the University Medical Centre and follow its official procedure.")
    with st.expander("Is the AI model always correct?"):
        st.write("No. The TF-IDF and Logistic Regression model gives a prediction. Low-confidence answers should be confirmed with staff.")
    st.markdown('<div class="notice notice-teal"><strong>Privacy:</strong> Avoid entering personal identifiers or uploading real medical records during prototype testing.</div>', unsafe_allow_html=True)


apply_styles()
if "page" not in st.session_state:
    st.session_state.page = "Home"


render_header()

pages = [
    "Home",
    "Ask a Question",
    "Documents",
    "Checklist",
    "About and Help",
]

selected = st.radio(
    "Main navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed",
    key="page",
)

if selected == "Home":
    home_page()
elif selected == "Ask a Question":
    ask_page()
elif selected == "Documents":
    render_documents_page()
elif selected == "Checklist":
    checklist_page()
else:
    about_page()

render_footer()
