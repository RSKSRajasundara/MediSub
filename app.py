import streamlit as st

from predictor import predict_question


st.set_page_config(
    page_title="Medical Submission Assistant",
    page_icon="🏥",
    layout="centered"
)

st.title("Medical Submission Assistant")

st.info(
    "This prototype provides administrative guidance only. "
    "Do not enter your diagnosis, registration number, password "
    "or other sensitive medical information."
)

st.subheader("Ask a Medical-Submission Question")

student_question = st.text_area(
    "Enter your question",
    placeholder="Example: What documents should I prepare?",
    max_chars=500
)

if st.button("Classify Question"):
    try:
        result = predict_question(student_question)

        st.write("Category:", result["category"])
        st.write(
            "Confidence:",
            f"{result['confidence'] * 100:.2f}%"
        )

        if result["needs_referral"]:
            st.warning(
                "The system is not confident about this question. "
                "Please contact the relevant staff member."
            )
        else:
            st.success("The question was classified successfully.")

    except ValueError as error:
        st.error(str(error))

    except FileNotFoundError as error:
        st.error(str(error))

    except Exception:
        st.error(
            "An unexpected error occurred. "
            "Please try again or contact the project team."
        )