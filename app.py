import streamlit as st
import re
import json
import joblib
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st
import json
from pdf_utils import extract_text_from_pdf
from ml_model import load_model
from input_handler import clean_text, build_structured_medical_intent
from diet_rules import generate_weekly_diet
from ocr_utils import extract_text_from_image
from export_utils import save_diet_json, save_diet_pdf
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



DEFAULT_FEATURES = {
    "Pregnancies": 0,
    "Glucose": 110,
    "BloodPressure": 120,
    "SkinThickness": 20,
    "Insulin": 80,
    "BMI": 24.0,
    "DiabetesPedigreeFunction": 0.5,
    "Age": 35
}
@st.cache_resource
def get_model():
    return load_model()

model = get_model()



# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI-Based Personalized Diet Planner",
    page_icon=os.path.join(BASE_DIR, "assets", "image", "favicon.png"),
    layout="centered"
)
if "intent" not in st.session_state:
    st.session_state.intent = None

if "preference" not in st.session_state:
    st.session_state.preference = None


logo_path = os.path.join(BASE_DIR, "assets", "image", "logo.png")
logo = Image.open(logo_path)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, width=200)

# ================= CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f6f9fc, #e9f0f7);
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #1f3c88;
    margin-top: 40px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #4a4a4a;
    margin-bottom: 30px;
}

/* Main buttons */
div.stButton > button {
    background-color: #1f3c88 !important;
    color: white !important;
    border-radius: 12px;
    height: 48px;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    border: none;
}
div.stButton > button:hover {
    background-color: #162c66 !important;
    color: white !important;
}

/* Download buttons */
.download-btn {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}
div.stDownloadButton > button {
    background-color: #28a745 !important;
    color: white !important;
    border-radius: 12px;
    height: 45px;
    font-size: 15px;
    font-weight: 600;
    border: none;
    padding: 0 25px;
}
div.stDownloadButton > button:hover {
    background-color: #1e7e34 !important;
    color: white !important;
}
div.stButton > button {
    box-shadow: 0px 6px 14px rgba(31, 60, 136, 0.25);
}
div.stButton > button:hover {
    transform: translateY(-1px);
}
            
</style>
""", unsafe_allow_html=True)

# ================= LOAD ML MODEL =================
@st.cache_resource
def load_ml_model():
    model_path = os.path.join(os.path.dirname(__file__), "xgboost_diet_model.pkl")
    return joblib.load(model_path)

ml_model = load_ml_model()

# ================= DEFAULT FEATURES =================
DEFAULT_FEATURES = {
    "Pregnancies": 0,
    "Glucose": 110,
    "BloodPressure": 120,
    "SkinThickness": 20,
    "Insulin": 80,
    "BMI": 24.0,
    "DiabetesPedigreeFunction": 0.5,
    "Age": 35
}
# ---------------- PAGE STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "intent" not in st.session_state:
    st.session_state.intent = None

if "preference" not in st.session_state:
    st.session_state.preference = None


# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":
    st.markdown('<div class="main-title">AI-Based Personalized Diet Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">ML + AI nutrition recommendation system</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Diet Planning"):
            st.session_state.page = "input"


# ---------------- INPUT PAGE ----------------
elif st.session_state.page == "input":
    st.subheader("📝 Enter Doctor Notes / Prescription")

    uploaded_pdf = st.file_uploader(
        "Upload Prescription (PDF)",
        type=["pdf"]
    )

    uploaded_image = st.file_uploader(
        "Upload Scanned Prescription (Image)",
        type=["png", "jpg", "jpeg"]
    )

    raw_text = st.text_area(
        "Doctor Notes",
        height=150,
        placeholder="Patient aged 45 yrs. BMI 32. Glucose is 180.",
        label_visibility="collapsed"
    )

    if uploaded_pdf is not None:
        raw_text = extract_text_from_pdf(uploaded_pdf)
        st.info("Text extracted from uploaded PDF")

    elif uploaded_image is not None:
        raw_text = extract_text_from_image(uploaded_image)
        st.info("Text extracted from uploaded Image (OCR)")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate Diet Plan"):
            cleaned_text = clean_text(raw_text)

            intent = build_structured_medical_intent(
                cleaned_text,
                model,
                DEFAULT_FEATURES
            )

            st.session_state.intent = intent
            st.session_state.page = "preferences"

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- PREFERENCES PAGE ----------------
elif st.session_state.page == "preferences":
    st.subheader("🍽 Select Your Dietary Preference")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🥦 Vegetarian"):
            st.session_state.preference = "veg"
            st.session_state.page = "output"

    with col2:
        if st.button("🍗 Non-Vegetarian"):
            st.session_state.preference = "nonveg"
            st.session_state.page = "output"

    if st.button("⬅ Back"):
        st.session_state.page = "input"


# ---------------- OUTPUT PAGE ----------------
elif st.session_state.page == "output":
    st.subheader("📅 Weekly Personalized Diet Plan")

    weekly_diet = generate_weekly_diet(
        st.session_state.intent,
        st.session_state.preference
    )

    st.json(weekly_diet)

    # -------- Export files --------
    json_file = save_diet_json(weekly_diet)
    pdf_file = save_diet_pdf(weekly_diet)

    st.markdown("<div class='download-btn'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        with open(json_file, "rb") as jf:
            st.download_button(
                "⬇ Download Diet Plan (JSON)",
                jf,
                file_name=json_file,
                mime="application/json"
            )

        with open(pdf_file, "rb") as pf:
            st.download_button(
                "⬇ Download Diet Plan (PDF)",
                pf,
                file_name=pdf_file,
                mime="application/pdf"
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"



