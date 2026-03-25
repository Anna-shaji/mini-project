import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Predict Churn", layout="wide", page_icon="🔮")

st.title("🔮 Predict Customer Churn")
st.write("Provide customer features below and run prediction. Returns churn probability and risk.")

with st.form(key='predict_form'):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1], help="0 = No, 1 = Yes")
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.slider("Tenure (Months)", 0, 72, 12)
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

    with col2:
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        monthly_charges = st.number_input("Monthly Charges ($)", value=50.0, format="%.2f")
        total_charges = st.number_input("Total Charges ($)", value=600.0, format="%.2f")

    submit = st.form_submit_button("Predict")

if submit:
    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": tech_support,
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
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

        if "feature_names" in result and "shap_values" in result:
            shap_df = pd.DataFrame({"Feature": result["feature_names"], "Impact": result["shap_values"]})
            shap_df = shap_df[shap_df["Impact"] != 0].sort_values("Impact", ascending=True).tail(10)
            fig = px.bar(shap_df, x="Impact", y="Feature", orientation="h", color="Impact", color_continuous_scale="RdYlGn_r", title="Top feature impacts")
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Prediction request failed: {e}")

st.write("---")
st.info("For historical churn analytics, go to **Dashboard** page.")