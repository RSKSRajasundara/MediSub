import base64
import os
import streamlit as st


def get_base64_image(image_path: str) -> str:
    """Converts a local image file into a base64 encoded string."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def apply_styles(use_second_bg: bool = False) -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))

    image_filename = "background2.jpg" if use_second_bg else "medical_background.jpg"

    # Search paths in order
    candidate_paths = [
        os.path.join(base_dir, "assets", image_filename),
        os.path.join(base_dir, image_filename),
        os.path.join(os.getcwd(), "assets", image_filename),
        os.path.join(os.getcwd(), image_filename),
        r"C:\Users\my pc\Downloads\medical_background.jpg",
    ]

    img_path = ""
    for path in candidate_paths:
        if os.path.exists(path):
            img_path = path
            break

    if not img_path:
        st.warning(f"⚠️ Background image '{image_filename}' not found! Search paths checked: {candidate_paths[:2]}")

    img_base64 = get_base64_image(img_path)

    if img_base64:
        bg_style = f"""
        background-image: 
            linear-gradient(rgba(246, 247, 249, 0.40), rgba(246, 247, 249, 0.40)),
            url("data:image/jpeg;base64,{img_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        """
    else:
        bg_style = """
        background: 
            radial-gradient(circle at 12% -15%, var(--teal-tint), transparent 42%),
            radial-gradient(circle at 100% -5%, var(--violet-tint), transparent 38%),
            var(--paper) !important;
        """

    st.markdown(
        f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
        
        :root {{
            --ink: #000000;
            --slate: #000000;
            --mist: #000000;
            --paper: #F6F7F9;
            --card: #FFFFFF;
            --line: #D0D5DD;
            --teal: #0E7C7B;
            --teal-tint: #E3F4F3;
            --violet: #6D4AFF;
            --violet-tint: #EEEAFF;
            --coral: #F4633A;
            --coral-tint: #FEEAE4;
            --amber-tint: #FDF2E2;
            --green: #12855F;
            --green-tint: #E3F6EF;
        }}

        /* 1. App container and background image */
        .stApp {{
            background-color: transparent !important;
        }}

        [data-testid="stAppViewContainer"] {{
            {bg_style}
        }}

        /* 2. Transparent inner containers so medical_background.jpg is fully visible */
        [data-testid="stHeader"],
        [data-testid="stMain"],
        .stMain,
        .main,
        section[data-testid="stMain"],
        [data-testid="stAppViewContainer"] > section,
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
            border-bottom: 1px solid rgba(208, 213, 221, 0.6) !important;
        }}

        [data-testid="stMainBlockContainer"],
        .block-container,
        [data-testid="stAppViewContainer"] .block-container {{
            width: 100% !important;
            max-width: 1100px !important;
            padding: 4.2rem 28px 2rem !important;
        }}

        /* 3. Universal Black Font Colors replacing ash/slate/mist */
        html, body, [class*="css"], p, span, label, div {{
            font-family: Inter, sans-serif;
            color: #000000;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: Manrope, sans-serif !important;
            color: #000000 !important;
        }}
        h1 {{
            font-size: 30px !important;
            letter-spacing: -0.02em;
        }}

        .page-lead {{
            color: #000000 !important;
            font-weight: 500;
            font-size: 15px;
            margin-top: -0.4rem;
            margin-bottom: 1.4rem;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0 0 0.7rem;
        }}
        .brand-mark {{
            width: 34px;
            height: 34px;
            border-radius: 9px;
            display: grid;
            place-items: center;
            color: #FFFFFF !important;
            background: linear-gradient(160deg, var(--teal), var(--violet));
            font: 800 15px Manrope;
        }}
        .brand-name {{
            font: 700 17px Manrope;
            color: #000000 !important;
        }}

        /* Radio Navigation */
        [data-testid="stRadio"], [data-testid="stRadio"] > div {{
            width: 100% !important;
        }}
        [data-testid="stRadio"] div[role="radiogroup"] {{
            display: grid !important;
            grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
            width: 100% !important;
            gap: 4px;
            padding: 6px;
            margin-bottom: 1.25rem;
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid var(--line);
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }}
        [data-testid="stRadio"] div[role="radiogroup"] label {{
            width: 100% !important;
            min-width: 0 !important;
            min-height: 40px;
            display: flex !important;
            align-items: center;
            justify-content: center;
            margin: 0 !important;
            padding: 0.35rem 0.45rem !important;
            border-radius: 8px;
            cursor: pointer;
        }}
        [data-testid="stRadio"] div[role="radiogroup"] label p {{
            color: #000000 !important;
            font-weight: 600;
        }}
        [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {{
            background: var(--teal-tint);
        }}
        [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {{
            color: var(--teal) !important;
            font-weight: 700;
        }}

        /* Hero */
        .hero {{
            max-width: 650px;
            margin: 2rem auto 1.4rem;
            text-align: center;
        }}
        .eyebrow {{
            font: 600 12px 'IBM Plex Mono';
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--teal) !important;
            margin-bottom: 0.7rem;
        }}
        .hero h1 {{
            font-size: 36px !important;
            margin: 0.2rem 0 0.8rem;
            color: #000000 !important;
        }}
        .hero .lead {{
            max-width: 520px;
            margin: auto;
            color: #000000 !important;
            font-size: 15.5px;
            line-height: 1.6;
            font-weight: 500;
        }}

        /* Cards */
        .card {{
            height: 100%;
            padding: 20px;
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid var(--line);
            border-left: 4px solid var(--teal);
            border-radius: 3px 18px 18px 3px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}
        .card.violet-edge {{ border-left-color: var(--violet); }}
        .card.coral-edge {{ border-left-color: var(--coral); }}
        .card h3 {{
            font-size: 16px;
            margin: 12px 0 6px;
            color: #000000 !important;
            font-weight: 700;
        }}
        .card p {{
            color: #000000 !important;
            font-size: 13.5px;
            line-height: 1.55;
            font-weight: 500;
        }}
        .icon-box {{
            width: 36px;
            height: 36px;
            display: grid;
            place-items: center;
            border-radius: 10px;
            color: var(--teal) !important;
            background: var(--teal-tint);
            font-weight: 700;
        }}

        /* Notices */
        .notice {{
            margin: 18px 0;
            padding: 14px 17px;
            border-radius: 16px;
            font-size: 13.5px;
            line-height: 1.55;
            font-weight: 500;
        }}
        .notice strong, .notice b {{
            font-weight: 700;
        }}
        .notice-teal {{
            background: var(--teal-tint);
            color: #053b3b !important;
            border: 1px solid #b2dfdb;
        }}
        .notice-amber {{
            background: var(--amber-tint);
            color: #5a3c0a !important;
            border: 1px solid #ffe0b2;
        }}
        .notice-coral {{
            background: var(--coral-tint);
            color: #6e200c !important;
            border: 1px solid #ffccbc;
        }}

        /* Chips & Dividers */
        .chips {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin: 10px 0 18px;
        }}
        .chips span {{
            padding: 6px 12px;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.95);
            color: #000000 !important;
            font-size: 12px;
            font-weight: 500;
        }}
        .section-divider {{
            border-top: 1px solid var(--line);
            margin: 26px 0 20px;
        }}

        /* Results & Metrics */
        .result-label {{
            font: 600 12px 'IBM Plex Mono';
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #000000 !important;
        }}
        .result-card, .metric-card, .doc-card {{
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}
        .doc-card h3 {{
            color: #000000 !important;
            margin-top: 8px;
        }}
        .doc-card p {{
            color: #000000 !important;
        }}
        .pill, .status {{
            display: inline-block;
            padding: 5px 11px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
        }}
        .pill-teal {{
            background: var(--teal-tint);
            color: var(--teal) !important;
        }}
        .result-answer {{
            margin: 16px 0;
            color: #000000 !important;
            line-height: 1.65;
            font-size: 15px;
            font-weight: 500;
        }}

        /* Step rows */
        .step-row {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 8px 0 22px;
        }}
        .step-row div {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid var(--line);
            border-radius: 12px;
        }}
        .step-row b {{
            width: 26px;
            height: 26px;
            display: grid;
            place-items: center;
            border-radius: 50%;
            background: var(--teal-tint);
            color: var(--teal);
        }}
        .step-row span {{
            font-size: 13.5px;
            color: #000000 !important;
            font-weight: 600;
        }}
        .progress-label {{
            color: #000000 !important;
            font-weight: 600;
        }}

        /* Streamlit Widgets Text & Black color overrides */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] li {{
            color: #000000 !important;
        }}

        [data-testid="stCheckbox"] label p,
        [data-testid="stCheckbox"] label span {{
            color: #000000 !important;
            font-weight: 500;
        }}

        [data-testid="stExpander"] {{
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
        }}
        [data-testid="stExpander"] details summary p,
        [data-testid="stExpander"] details summary span {{
            color: #000000 !important;
            font-weight: 600;
        }}
        [data-testid="stExpander"] details div p,
        [data-testid="stExpander"] details div span {{
            color: #000000 !important;
        }}

        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label {{
            color: #000000 !important;
            font-weight: 600;
        }}

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div {{
            color: #000000 !important;
        }}
        [data-testid="stMetricLabel"] p {{
            color: #000000 !important;
            font-weight: 600;
        }}
        [data-testid="stCaptionContainer"] p,
        caption, small {{
            color: #000000 !important;
            font-weight: 500;
        }}

        button[data-baseweb="tab"] p {{
            color: #000000 !important;
            font-weight: 600;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: var(--teal) !important;
            font-weight: 700;
        }}

        .stButton > button, .stDownloadButton > button {{
            min-height: 40px;
            border-radius: 10px;
            font-weight: 600;
        }}
        .stButton > button[kind="primary"] {{
            background: var(--teal);
            border-color: var(--teal);
            color: #FFFFFF !important;
        }}

        .stTextArea textarea {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid var(--line) !important;
            border-radius: 10px;
            color: #000000 !important;
        }}
        .stTextArea textarea::placeholder {{
            color: #555555 !important;
        }}

        [data-testid="stFileUploaderDropzone"] {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            border: 1px dashed var(--line);
        }}
        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] small {{
            color: #000000 !important;
        }}

        .footer {{
            margin: 2.2rem 0 0;
            text-align: center;
            color: #000000 !important;
            font-size: 13px;
            font-weight: 500;
        }}

        @media(max-width: 800px) {{
            [data-testid="stMainBlockContainer"],
            .block-container {{
                padding: 4rem 18px 1.5rem !important;
            }}
            [data-testid="stRadio"] div[role="radiogroup"] {{
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            }}
            .hero {{
                margin-top: 1rem;
            }}
            .hero h1 {{
                font-size: 28px !important;
            }}
            .step-row {{
                grid-template-columns: 1fr;
            }}
        }}
        </style>""",
        unsafe_allow_html=True,
    )