import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Churn Sentinel Home", layout="wide", page_icon="🏠")

st.title("🏡 Churn Sentinel AI - Home")
st.write("Welcome to the Customer Churn Prediction app. Use the sidebar to navigate to **Predict Customer** and **Dashboard** pages.")

st.markdown("""
## How to use
1. Go to **Predict Customer** (left sidebar).
2. Provide customer details and click **Predict**.
3. Open **Dashboard** to explore historical churn trends and feature graphs.
""")

st.info("➡️ Prediction and explainability are now moved to **pages/predict_customer.py**.")