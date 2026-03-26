import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

st.set_page_config(page_title="Predict Churn", layout="wide", page_icon="🔮")

st.markdown(
    """
    <style>
    .stApp {
        background: #111111;
        color: #e0e0e0;
    }
    .section-card, .metric-card {
        background: #1f1f1f;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        margin-bottom: 1.1rem;
        border: 1px solid #333333;
    }
    .stButton>button {
        background-color: #e50914;
        color: #fff;
        border-radius: 9px;
        padding: 0.65rem 1.1rem;
        font-weight: 700;
        border: none;
    }
    .stButton>button:hover {
        background-color: #b80610;
    }
    .stSelectbox>div, .stNumberInput>div, .stSlider>div {
        border-radius: 8px;
        background: #2a2a2a;
        color: #e5e5e5;
    }
    .section-card h1 {
        color: #ff0000;
        margin-bottom: 0.25rem;
    }
    .section-card p {
        color: #dcdcdc;
        font-size: 1.04rem;
        line-height: 1.6;
    }
    .section-title {
        font-size: 1.3rem;
        color: #ff0000;
        margin-top: 16px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<div class='section-card'>
<h1>🔮 Predict Customer Churn</h1>
<p>Enter a customer profile to estimate churn probability and receive retention guidance.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='section-card'>
  <div class='section-title'>Customer Input</div>
  <p>Use the form below to provide the latest customer details and compute churn risk.</p>
</div>
""", unsafe_allow_html=True)

st.write("Provide customer features below and run prediction. Returns churn probability and risk.")

with st.form(key='predict_form'):
    col1, col2 = st.columns(2)

    with col1:
        senior = st.selectbox("Senior Citizen", [0, 1], help="0 = No, 1 = Yes")
        tenure = st.slider("Tenure (Months)", 0, 72, 12)
        monthly_charges = st.number_input("Monthly Charges ($)", value=50.0, format="%.2f")
        total_charges = st.number_input("Total Charges ($)", value=600.0, format="%.2f")

    with col2:
        clv = st.number_input("CLV", value=1000.0, format="%.2f")
        service_count = st.number_input("Service Count", value=1, step=1)
        engagement_score = st.number_input("Engagement Score", value=50.0, format="%.2f")
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

    submit = st.form_submit_button("Predict")

if submit:
    payload = {
        "SeniorCitizen": senior,
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "CLV": clv,
        "ServiceCount": service_count,
        "EngagementScore": engagement_score,
        "Contract": contract,
        # Default values for required features not present in form
        "gender": "Female",
        "Partner": "No",
        "Dependents": "No",
        "PhoneService": "No",
        "MultipleLines": "No",
        "InternetService": "No",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "PaperlessBilling": "No",
        "PaymentMethod": "Electronic check"
    }

    try:
        with st.spinner("Requesting prediction from backend..."):
            response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()

        prob = result.get("probability", None)
        risk = result.get("risk", "Unknown")

        st.metric("Churn Probability", f"{prob*100:.1f}%" if prob is not None else "N/A", delta=risk)

        if prob is not None:
            if prob > 0.5:
                st.error("⚠️ This customer is likely to CHURN.")
            else:
                st.success("✅ This customer is likely to STAY.")

            st.write("### 💡 Suggested Retention Strategy")
            if prob > 0.7:
                st.warning("High churn risk: prioritize immediate customer outreach and retention offers.")
            elif prob > 0.5:
                st.info("Moderate churn risk: offer incentives, personalize communication, and monitor closely.")
            else:
                st.success("Low churn risk: maintain current satisfaction initiatives and upsell opportunities.")

            st.markdown("""
- Offer a discount on long-term contracts for at-risk customers (e.g., 1 year / 2 year deals).
- Resolve service issues quickly, especially for Fiber optic or no online security complaints.
- Provide loyalty rewards or usage credits (e.g., for high monthly charges).
- Proactively call customers with `Month-to-month` contracts in the churn zone.
""")

        if "feature_names" in result and "shap_values" in result:
            shap_df = pd.DataFrame({"Feature": result["feature_names"], "Impact": result["shap_values"]})
            # Filter to only changing features that cause impact
            changing_features = ["tenure", "MonthlyCharges", "CLV", "TotalCharges"]
            shap_df = shap_df[shap_df["Feature"].isin(changing_features)]
            shap_df = shap_df[shap_df["Impact"] != 0].sort_values("Impact", ascending=True).tail(10)
            fig = px.bar(shap_df, x="Impact", y="Feature", orientation="h", color="Impact", color_continuous_scale="RdYlGn_r", title="Top feature impacts")
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Save prediction to local history so dashboard can use it dynamically
        history_path = os.path.join(os.path.dirname(__file__), "predictions_history.csv")
        row = {
            "timestamp": pd.Timestamp.now(),
            "SeniorCitizen": senior,
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "CLV": clv,
            "ServiceCount": service_count,
            "EngagementScore": engagement_score,
            "Contract": contract,
            "pred_probability": prob,
            "pred_risk": risk,
            "predicted_churn": "Churn" if prob is not None and prob > 0.5 else "No Churn"
        }

        prev_df = pd.DataFrame([row])
        if os.path.exists(history_path):
            existing = pd.read_csv(history_path)
            updated = pd.concat([existing, prev_df], ignore_index=True)
        else:
            updated = prev_df
        updated.to_csv(history_path, index=False)

    except Exception as e:
        st.error(f"Prediction request failed: {e}")

st.write("---")
st.info("For historical churn analytics, go to **Dashboard** page.")