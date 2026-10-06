import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MediSub",
    page_icon="🏥",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin-top: 30px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 30px;
}

.card {
    padding: 25px;
    border: 1px solid #ddd;
    border-radius: 12px;
    min-height: 170px;
    margin-bottom: 20px;
}

.warning {
    padding: 20px;
    border: 1px solid #f0ad4e;
    border-radius: 10px;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# NAVIGATION
# =========================================================

def navigation():

    st.sidebar.title("🏥 MediSub")

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    if st.sidebar.button("💬 Ask a Question", use_container_width=True):
        st.session_state.page = "ask"
        st.rerun()

    if st.sidebar.button("📋 Check Requirements", use_container_width=True):
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

    # ASK QUESTION BUTTON
    with col1:

        if st.button(
            "💬 Ask a Question",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.page = "ask"
            st.rerun()

    # CHECK REQUIREMENTS BUTTON
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

        st.markdown("""
        <div class="card">

        ### 🤖 AI Question Classification

        Ask a question and MediSub identifies
        the relevant administrative category.

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">

        ### 📋 Requirement Checking

        Check the important requirements
        before submitting your medical documents.

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="card">

        ### 🧭 Next-Step Guidance

        Receive guidance about what you
        should do next.

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="warning">

    ### 🔒 Privacy Warning

    Please do not enter sensitive personal or medical
    information into this prototype.

    Avoid entering:

    - Student registration numbers
    - Passwords
    - Private medical records
    - Detailed medical diagnoses
    - Other sensitive personal information

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.info(
        """
        ⚠️ **Prototype Disclaimer**

        MediSub is an academic prototype developed for
        educational purposes. It provides administrative
        guidance and does not replace official university
        staff or official university procedures.
        """
    )


# =========================================================
# ASK QUESTION PAGE
# =========================================================

def ask_question_page():

    st.title("💬 Ask a Question")

    st.write(
        "Ask a question about the university medical submission process."
    )

    # HOME BUTTON
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.divider()

    st.subheader("Enter your question")

    question = st.text_area(
        "Question",
        placeholder=(
            "Example: What documents do I need "
            "for medical submission?"
        ),
        height=150
    )

    st.subheader("Example Questions")

    example_col1, example_col2 = st.columns(2)

    with example_col1:

        if st.button(
            "What documents do I need?",
            use_container_width=True
        ):
            st.session_state.question = (
                "What documents do I need for medical submission?"
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

    with example_col2:

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

    # Use selected example question
    if "question" in st.session_state:
        question = st.session_state.question

    st.divider()

    col1, col2 = st.columns(2)

    # CHECK QUESTION
    with col1:

        if st.button(
            "🔍 Check Question",
            use_container_width=True,
            type="primary"
        ):

            if not question.strip():

                st.warning("Please enter a question first.")

            else:

                # Temporary classification
                # We will connect predictor.py here next.

                question_lower = question.lower()

                if (
                    "document" in question_lower
                    or "documents" in question_lower
                    or "report" in question_lower
                ):

                    category = "DOCUMENT_REQUIREMENTS"
                    confidence = 90

                    guidance = (
                        "Check that you have prepared the required "
                        "medical documents before submission."
                    )

                    next_action = (
                        "Review the required documents and prepare "
                        "any missing items."
                    )

                elif (
                    "submit" in question_lower
                    or "submission" in question_lower
                    or "process" in question_lower
                ):

                    category = "PROCESS_GUIDANCE"
                    confidence = 88

                    guidance = (
                        "Follow the university medical submission "
                        "process and confirm the required steps."
                    )

                    next_action = (
                        "Review the submission process and contact "
                        "the relevant university staff if you are unsure."
                    )

                elif (
                    "reference" in question_lower
                    or "number" in question_lower
                ):

                    category = "REFERENCE_NUMBER_HELP"
                    confidence = 87

                    guidance = (
                        "Your medical reference number is used to "
                        "identify your medical submission."
                    )

                    next_action = (
                        "Check your medical documentation or contact "
                        "the relevant medical centre."
                    )

                else:

                    category = "OUT_OF_SCOPE"
                    confidence = 45

                    guidance = (
                        "MediSub could not confidently identify "
                        "the category of your question."
                    )

                    next_action = (
                        "Please contact the relevant university "
                        "staff member for confirmation."
                    )

                # RESULTS
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
                        f"{confidence}%"
                    )

                st.subheader("🧭 Guidance")

                st.info(guidance)

                st.subheader("➡️ Recommended Next Action")

                st.success(next_action)

                if confidence < 60:

                    st.warning(
                        "⚠️ The system is not confident about "
                        "this question. Please contact university "
                        "staff for confirmation."
                    )

    # CLEAR BUTTON
    with col2:

        if st.button(
            "🗑️ Clear",
            use_container_width=True
        ):

            if "question" in st.session_state:
                del st.session_state.question

            st.rerun()


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
        "I have contacted/visited the Medical Centre."
    )

    reference_number = st.checkbox(
        "I have obtained my medical reference number."
    )

    medical_report = st.checkbox(
        "I have the required medical report/document."
    )

    required_documents = st.checkbox(
        "I have prepared all required documents."
    )

    submission_information = st.checkbox(
        "I know where and how to submit the documents."
    )

    completed = sum([
        called_medical,
        reference_number,
        medical_report,
        required_documents,
        submission_information
    ])

    total = 5

    progress = completed / total

    st.progress(progress)

    st.write(
        f"### Progress: {completed}/{total} requirements completed"
    )

    if st.button(
        "🔍 Check My Progress",
        type="primary",
        use_container_width=True
    ):

        missing = []

        if not called_medical:
            missing.append("Contact/visit the Medical Centre")

        if not reference_number:
            missing.append("Obtain your medical reference number")

        if not medical_report:
            missing.append("Prepare the medical report")

        if not required_documents:
            missing.append("Prepare all required documents")

        if not submission_information:
            missing.append("Confirm the submission procedure")

        st.divider()

        if len(missing) == 0:

            st.success(
                "✅ Your checklist is complete. "
                "You appear to have completed the required steps."
            )

            st.info(
                "Recommended next action: Proceed with the "
                "official submission process."
            )

        else:

            st.warning("⚠️ You still have missing requirements.")

            st.subheader("Missing Requirements")

            for item in missing:
                st.write(f"❌ {item}")

            st.info(
                "Recommended next action: Complete the missing "
                "requirements before submitting."
            )

    if st.button(
        "🔄 Reset Checklist",
        use_container_width=True
    ):

        st.rerun()


# =========================================================
# PAGE ROUTING
# =========================================================

navigation()

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "ask":

    ask_question_page()

elif st.session_state.page == "checklist":

    checklist_page()