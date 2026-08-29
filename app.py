import streamlit as st

from predictor import predict_question


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MediSub - Medical Submission Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "question" not in st.session_state:
    st.session_state.question = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 25px;
        border: 1px solid #dddddd;
        border-radius: 12px;
        min-height: 180px;
        margin-bottom: 20px;
    }

    .warning-box {
        padding: 20px;
        border: 1px solid #f0ad4e;
        border-radius: 10px;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NAVIGATION
# =========================================================

def show_navigation():

    st.sidebar.title("🏥 MediSub")

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    if st.sidebar.button("💬 Ask a Question", use_container_width=True):
        st.session_state.page = "ask"
        st.rerun()

    if st.sidebar.button(
        "📋 Check Requirements",
        use_container_width=True
    ):
        st.session_state.page = "checklist"
        st.rerun()


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    st.markdown(
        '<div class="main-title">🏥 MediSub</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'University Medical Submission Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.header("Welcome to MediSub")

    st.write(
        """
        MediSub is an AI-based university administrative assistant
        designed to help students understand the medical submission
        process.

        You can ask questions about medical submissions, check
        your requirements, and receive guidance about the next
        administrative step.
        """
    )

    st.divider()

    st.subheader("How can we help you?")

    col1, col2 = st.columns(2)

    # ASK QUESTION
    with col1:

        if st.button(
            "💬 Ask a Question",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.page = "ask"
            st.rerun()

    # CHECK REQUIREMENTS
    with col2:

        if st.button(
            "📋 Check Requirements",
            use_container_width=True
        ):

            st.session_state.page = "checklist"
            st.rerun()

    st.divider()

    st.header("Main Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🤖 AI Question Classification</h3>

            <p>
            Ask a question and MediSub identifies
            the relevant administrative category.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            <h3>📋 Requirement Checking</h3>

            <p>
            Check important requirements before
            submitting your medical documents.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🧭 Next-Step Guidance</h3>

            <p>
            Receive guidance about the appropriate
            next administrative step.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown(
        """
        <div class="warning-box">

        <h3>🔒 Privacy Warning</h3>

        <p>
        Please do not enter sensitive personal or medical
        information into this prototype.
        </p>

        <ul>
            <li>Student registration numbers</li>
            <li>Passwords</li>
            <li>Private medical records</li>
            <li>Detailed medical diagnoses</li>
            <li>Other sensitive personal information</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.warning(
        """
        ⚠️ Prototype Disclaimer

        MediSub is an academic prototype developed for
        educational purposes. It provides administrative
        guidance only and does not replace official university
        staff or official university procedures.
        """
    )


# =========================================================
# ASK QUESTION PAGE
# =========================================================

def ask_question_page():

    st.title("💬 Ask a Medical-Submission Question")

    st.write(
        "Enter your question below and MediSub will classify it "
        "using the existing AI prediction model."
    )

    if st.button("🏠 Back to Home"):

        st.session_state.page = "home"
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # QUESTION INPUT
    # -----------------------------------------------------

    student_question = st.text_area(
        "Enter your question",
        value=st.session_state.question,
        placeholder="Example: What documents should I prepare?",
        max_chars=500,
        height=150
    )

    # -----------------------------------------------------
    # EXAMPLES
    # -----------------------------------------------------

    st.subheader("Example Questions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "What documents should I prepare?",
            use_container_width=True
        ):
            st.session_state.question = (
                "What documents should I prepare?"
            )
            st.rerun()

        if st.button(
            "How do I submit my medical?",
            use_container_width=True
        ):
            st.session_state.question = (
                "How do I submit my medical?"
            )
            st.rerun()

    with col2:

        if st.button(
            "Where can I get my reference number?",
            use_container_width=True
        ):
            st.session_state.question = (
                "Where can I get my reference number?"
            )
            st.rerun()

        if st.button(
            "What is the medical submission process?",
            use_container_width=True
        ):
            st.session_state.question = (
                "What is the medical submission process?"
            )
            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # BUTTONS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        classify_clicked = st.button(
            "🔍 Classify Question",
            use_container_width=True,
            type="primary"
        )

    with col2:

        clear_clicked = st.button(
            "🗑️ Clear",
            use_container_width=True
        )

    # -----------------------------------------------------
    # CLEAR
    # -----------------------------------------------------

    if clear_clicked:

        st.session_state.question = ""
        st.rerun()

    # -----------------------------------------------------
    # AI CLASSIFICATION
    # -----------------------------------------------------

    if classify_clicked:

        if not student_question.strip():

            st.warning(
                "Please enter a question before clicking "
                "'Classify Question'."
            )

        else:

            try:

                result = predict_question(student_question)

                category = result["category"]
                confidence = result["confidence"]
                needs_referral = result["needs_referral"]

                st.divider()

                st.subheader("Prediction Result")

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    st.metric(
                        "Predicted Category",
                        category
                    )

                with result_col2:

                    st.metric(
                        "Confidence",
                        f"{confidence * 100:.2f}%"
                    )

                # -------------------------------------------------
                # REFERRAL
                # -------------------------------------------------

                if needs_referral:

                    st.warning(
                        """
                        ⚠️ The system is not confident about
                        this question.

                        Please contact the relevant university
                        staff member for confirmation.
                        """
                    )

                else:

                    st.success(
                        "The question was classified successfully."
                    )

                    # Basic guidance based on category
                    if category == "DOCUMENT_REQUIREMENTS":

                        st.info(
                            """
                            📋 **Guidance**

                            Review the required medical documents
                            before submitting your request.

                            **Recommended next action:**
                            Prepare the required documents and
                            confirm the submission procedure.
                            """
                        )

                    elif category == "PROCESS_GUIDANCE":

                        st.info(
                            """
                            🧭 **Guidance**

                            Follow the official university medical
                            submission process.

                            **Recommended next action:**
                            Review the submission steps or contact
                            the relevant staff member if you are unsure.
                            """
                        )

                    elif category == "REFERENCE_NUMBER_HELP":

                        st.info(
                            """
                            🔢 **Guidance**

                            Your medical reference number may be
                            required to identify your submission.

                            **Recommended next action:**
                            Check your medical documentation or
                            contact the relevant medical centre.
                            """
                        )

                    elif category == "MA_SUBMISSION_HELP":

                        st.info(
                            """
                            📝 **Guidance**

                            Review the medical submission
                            requirements and submission procedure.

                            **Recommended next action:**
                            Check your prepared documents and
                            follow the official submission process.
                            """

                        )

                    else:

                        st.info(
                            """
                            Please review the official university
                            procedure or contact the relevant staff
                            member for assistance.
                            """
                        )

            except ValueError as error:

                st.error(str(error))

            except FileNotFoundError as error:

                st.error(str(error))

            except Exception as error:

                st.error(
                    "An unexpected error occurred. "
                    "Please try again or contact the project team."
                )


# =========================================================
# CHECKLIST PAGE
# =========================================================

def checklist_page():

    st.title("📋 Check Medical Requirements")

    st.write(
        "Use this checklist to check whether you are ready "
        "for medical submission."
    )

    if st.button("🏠 Back to Home"):

        st.session_state.page = "home"
        st.rerun()

    st.divider()

    st.subheader("Medical Submission Checklist")

    called_medical = st.checkbox(
        "I have contacted or visited the Medical Centre."
    )

    reference_number = st.checkbox(
        "I have obtained my medical reference number."
    )

    medical_report = st.checkbox(
        "I have the required medical report."
    )

    required_documents = st.checkbox(
        "I have prepared all required documents."
    )

    submission_information = st.checkbox(
        "I know where and how to submit the documents."
    )

    completed = sum(
        [
            called_medical,
            reference_number,
            medical_report,
            required_documents,
            submission_information
        ]
    )

    total = 5

    st.progress(completed / total)

    st.write(
        f"### Progress: {completed}/{total} requirements completed"
    )

    if st.button(
        "🔍 Check My Progress",
        use_container_width=True,
        type="primary"
    ):

        missing = []

        if not called_medical:
            missing.append(
                "Contact or visit the Medical Centre"
            )

        if not reference_number:
            missing.append(
                "Obtain your medical reference number"
            )

        if not medical_report:
            missing.append(
                "Prepare the medical report"
            )

        if not required_documents:
            missing.append(
                "Prepare all required documents"
            )

        if not submission_information:
            missing.append(
                "Confirm the submission procedure"
            )

        st.divider()

        if not missing:

            st.success(
                "✅ Your checklist is complete."
            )

            st.info(
                "Recommended next action: Proceed with the "
                "official submission process."
            )

        else:

            st.warning(
                "⚠️ You still have missing requirements."
            )

            st.subheader("Missing Requirements")

            for item in missing:

                st.write(f"❌ {item}")

            st.info(
                "Complete the missing requirements before "
                "submitting your documents."
            )

    if st.button(
        "🔄 Reset Checklist",
        use_container_width=True
    ):

        st.rerun()


# =========================================================
# APPLICATION ROUTING
# =========================================================

show_navigation()

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "ask":

    ask_question_page()

elif st.session_state.page == "checklist":

    checklist_page()