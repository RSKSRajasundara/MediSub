# MediSub

simple process steps:
Students can enter a question, and the system classifies it into one of the following categories:

- `PROCESS_GUIDANCE`
- `REFERENCE_NUMBER_HELP`
- `DOCUMENT_REQUIREMENTS`
- `MA_SUBMISSION_HELP`
- `OUT_OF_SCOPE`

The current version uses TF-IDF and Logistic Regression to classify questions and display a confidence score.

## technologies used 

- Python 3.12
- Streamlit
- pandas
- scikit-learn
- TF-IDF
- Logistic Regression
- joblib
- SQLite
- Jupyter Notebook
- Pytest
- Git and GitHub
- Tesseract OCR (required for document image text extraction)

## Project Structure

```text
MediSub/
├── data/               Dataset files
├── models/             Trained AI model
├── notebooks/          Model-training notebook
├── tests/              Test files
├── app.py              Streamlit application
├── database.py         Database functions
├── guidance.py         Guidance messages
├── predictor.py        AI prediction functions
├── rules.py            Checklist rules
├── security.py         Security functions
└── requirements.txt    Required packages
```

## ssetup Instructions

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR-USERNAME/MediSub.git
cd MediSub
code .
```

Replace the URL with the actual GitHub repository URL.

### 2. Create the virtual environment

```powershell
py -3.12 -m venv .venv
```

### 3. Activate the environment

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks the command:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 4. Install the packages

```powershell
pip install -r requirements.txt
```

### 5. Train the AI model

Open:

```text
notebooks/train_model.ipynb
```

Select the `.venv` Python kernel and click **Run All**.

The trained model will be saved as:

```text
models/medical_classifier.joblib
```

### 6. Run the application

From the main `MediSub` folder, run:

```powershell
streamlit run app.py
```

### Document checker OCR setup

The document checker uses `pytesseract` to read uploaded JPG, JPEG, and PNG
images. Install the Tesseract OCR application separately, then either add its
installation folder to `PATH` or set `TESSERACT_CMD` to the full path of
`tesseract.exe`, for example:

```powershell
$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
streamlit run app.py
```

Without Tesseract, the manual checklist still loads, but image OCR checks
will show an explicit setup error.

The application will normally open at:

```text
http://localhost:8501
```

Press `Ctrl + C` in the terminal to stop it.

## Current Progress

- Project environment created
- Initial fictional dataset created
- TF-IDF and Logistic Regression model added
- Model training notebook created
- Basic Streamlit classification interface created
