from pathlib import Path

import joblib


MODEL_PATH = Path(__file__).parent / "models" / "medical_classifier.joblib"
CONFIDENCE_THRESHOLD = 0.60


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "The trained model was not found. Run train_model.ipynb first."
        )

    return joblib.load(MODEL_PATH)


def predict_question(question):
    clean_question = question.strip()

    if not clean_question:
        raise ValueError("Please enter a question.")

    if len(clean_question) > 500:
        raise ValueError("The question must contain 500 characters or fewer.")

    model = load_model()

    category = model.predict([clean_question])[0]
    probabilities = model.predict_proba([clean_question])[0]
    confidence = float(probabilities.max())

    needs_referral = confidence < CONFIDENCE_THRESHOLD

    return {
        "category": category,
        "confidence": confidence,
        "needs_referral": needs_referral
    }