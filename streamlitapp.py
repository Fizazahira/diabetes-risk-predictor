
import streamlit as st
import requests

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="wide"
)

API_URL = "https://interosseous-hilaria-amicably.ngrok-free.dev"

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #123b55, #168c89);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e5f5f5;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 21px;
        font-weight: 650;
        margin-top: 12px;
        margin-bottom: 5px;
    }

    .result-card {
        padding: 24px;
        border-radius: 15px;
        background: #edf7f5;
        border: 1px solid #c8e5df;
        margin-top: 15px;
    }

    .small-note {
        color: #64748b;
        font-size: 13px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 48px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🩺 Diabetes Risk Predictor</h1>
    <p>
        Enter patient measurements to receive a prediction
        from your machine-learning model.
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "This tool is an educational demonstration, not a medical "
    "diagnosis. Enter measurements carefully."
)

# ---------------- PATIENT INPUTS ----------------
st.markdown(
    '<div class="section-title">👤 Patient Information</div>',
    unsafe_allow_html=True
)
st.caption("Enter the patient's age and pregnancy history.")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age (years)",
        min_value=1,
        max_value=120,
        value=30,
        help="Patient's age in years."
    )

with col2:
    pregnancies = st.number_input(
        "Number of pregnancies",
        min_value=0,
        max_value=20,
        value=2,
        help="Number of times the patient has been pregnant."
    )

st.markdown("---")

st.markdown(
    '<div class="section-title">🧪 Health Measurements</div>',
    unsafe_allow_html=True
)
st.caption("Enter the recorded clinical measurements.")

col1, col2 = st.columns(2)

with col1:
    glucose = st.number_input(
        "Glucose (mg/dL)",
        min_value=0.0,
        max_value=700.0,
        value=120.0,
        help="Plasma glucose concentration."
    )

    blood_pressure = st.number_input(
        "Diastolic blood pressure (mm Hg)",
        min_value=0.0,
        max_value=300.0,
        value=70.0
    )

    skin_thickness = st.number_input(
        "Skin thickness (mm)",
        min_value=0.0,
        max_value=150.0,
        value=20.0
    )

    insulin = st.number_input(
        "Insulin (mu U/mL)",
        min_value=0.0,
        max_value=3000.0,
        value=79.0
    )

with col2:
    bmi = st.number_input(
        "BMI",
        min_value=0.0,
        max_value=150.0,
        value=25.0,
        help="Body mass index."
    )

    pedigree = st.number_input(
        "Diabetes pedigree function",
        min_value=0.0,
        max_value=10.0,
        value=0.5,
        help="A score related to family history of diabetes."
    )

    st.markdown("""
    <div style="
        padding: 15px;
        border-radius: 12px;
        background: rgba(128,128,128,0.08);
        margin-top: 8px;
    ">
        <b>Before predicting</b><br>
        <span style="font-size: 14px;">
        Check that all measurements match the patient's records.
        Do not use zero for missing measurements unless zero is
        the actual recorded value.
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- PREDICTION ----------------
st.markdown(
    '<div class="section-title">📊 Prediction</div>',
    unsafe_allow_html=True
)
st.caption("Your inputs will be sent to the FastAPI model.")

if st.button("🔍 Predict Diabetes Risk", type="primary"):

    patient = {
        "Pregnancies": int(pregnancies),
        "Glucose": float(glucose),
        "BloodPressure": float(blood_pressure),
        "SkinThickness": float(skin_thickness),
        "Insulin": float(insulin),
        "BMI": float(bmi),
        "DiabetesPedigreeFunction": float(pedigree),
        "Age": int(age)
    }

    try:
        with st.spinner("Analyzing patient measurements..."):
            response = requests.post(
                API_URL,
                json=patient,
                timeout=15
            )

        if response.status_code == 200:
            result = response.json()

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            if result["prediction"] == 1:
                st.error("Model prediction: Diabetic")
                st.write(
                    "The model classified these inputs as belonging "
                    "to the diabetic class."
                )
            else:
                st.success("Model prediction: Not Diabetic")
                st.write(
                    "The model classified these inputs as belonging "
                    "to the non-diabetic class."
                )

            confidence = float(result["confidence"])
            st.metric(
                "Model confidence",
                f"{confidence * 100:.1f}%"
            )
            st.progress(max(0.0, min(1.0, confidence)))

            st.markdown('</div>', unsafe_allow_html=True)

            st.caption(
                "Confidence is the model's predicted probability for "
                "its selected class. It is not a person's actual "
                "probability of having diabetes."
            )

        else:
            st.error(
                f"API error ({response.status_code}): "
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the prediction API. "
            "Please start FastAPI in another terminal."
        )

    except requests.exceptions.Timeout:
        st.error("The API took too long to respond. Please try again.")

    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    '<p class="small-note">'
    'Diabetes Risk Predictor · K-Nearest Neighbours (KNN) · '
    'Educational project only'
    '</p>',
    unsafe_allow_html=True
)
