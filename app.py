import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Churn Sentinel AI", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS FOR BETTER LOOKS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Customer Churn Analysis & Explainable AI")
st.write("Predict if a customer will leave and understand **why** using SHAP explanations.")

# --- SIDEBAR / INPUT SECTION ---
with st.sidebar:
    st.header("📋 Customer Information")
    
    # Categorical Inputs
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", [0, 1], help="0 = No, 1 = Yes")
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    phone = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    
    # Numerical Inputs
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    monthly_charges = st.number_input("Monthly Charges ($)", value=50.0)
    total_charges = st.number_input("Total Charges ($)", value=600.0)

# Create the payload for the API
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
    "OnlineBackup": "No", # Adding defaults for missing UI fields
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

# --- MAIN DISPLAY AREA ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Analysis")
    if st.button("🚀 Analyze Churn Risk", use_container_width=True):
        try:
            # Call the FastAPI Backend
            with st.spinner('Calculating risk and generating SHAP values...'):
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                res = response.json()

            # 1. Result Metrics
            prob = res['probability']
            risk_level = res['risk']
            
            # Color logic for metrics
            color = "inverse" if prob > 0.5 else "normal"
            
            st.metric(label="Churn Probability", value=f"{prob*100:.1f}%", delta=risk_level + " Risk", delta_color=color)
            
            if prob > 0.5:
                st.error("⚠️ This customer is likely to CHURN.")
            else:
                st.success("✅ This customer is likely to STAY.")

            # 2. Features impacting this specific prediction
            st.write("---")
            st.markdown("### 🔍 Key Drivers for this Result")
            
            # Create DataFrame for SHAP
            shap_df = pd.DataFrame({
                'Feature': res['feature_names'],
                'Impact': res['shap_values']
            })
            
            # Filter out zero-impact features and show top 10
            shap_df = shap_df[shap_df['Impact'] != 0].sort_values(by='Impact', ascending=True).tail(10)
            
            fig = px.bar(
                shap_df, 
                x='Impact', 
                y='Feature', 
                orientation='h',
                color='Impact',
                color_continuous_scale='RdYlGn_r',
                title="What influenced this prediction?"
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Could not connect to Backend. Is the FastAPI server running? Error: {e}")

with col2:
    st.subheader("Dashboard & Insights")
    # Small placeholder for "Dashboard" features you mentioned
    tab1, tab2 = st.tabs(["Retention Strategy", "Customer Segment"])
    
    with tab1:
        st.info("Based on the SHAP analysis, here are recommended actions:")
        st.write("1. Offer a long-term contract discount.")
        st.write("2. Provide tech support bundle.")
    
    with tab2:
        # Mini chart showing where this customer sits
        st.write("Customer Monthly Charges vs Tenure")
        chart_data = pd.DataFrame({'Tenure': [tenure], 'Charges': [monthly_charges]})
        st.scatter_chart(chart_data, x='Tenure', y='Charges')