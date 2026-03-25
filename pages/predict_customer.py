import streamlit as st
import requests

st.title("Predict Customer Churn")

tenure = st.slider("Tenure",0,72)

monthly = st.number_input("Monthly Charges")

contract = st.selectbox(
"Contract Type",
["Month-to-month","One year","Two year"]
)

if st.button("Predict"):

    data = {
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "Contract": contract
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    result = response.json()

    st.write("Churn Probability:", result["probability"])
    st.write("Risk Level:", result["risk"])