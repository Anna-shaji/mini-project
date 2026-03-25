import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Churn Dashboard", layout="wide", page_icon="📊")

st.title("📊 Customer Churn Dashboard")

csv_path = os.path.join(os.path.dirname(__file__), "WA_Fn-UseC_-Telco-Customer-Churn.csv")
if not os.path.exists(csv_path):
    st.error("Dataset csv not found in pages folder. Please add WA_Fn-UseC_-Telco-Customer-Churn.csv")
    st.stop()


# Load data
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(csv_path)

# Basic charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Distribution")
    pie = px.pie(df, names="Churn", title="Churn vs No Churn")
    st.plotly_chart(pie, use_container_width=True)

with col2:
    st.subheader("Churn by Contract Type")
    contract = df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")
    bar_contract = px.bar(contract, x="Contract", y="Count", color="Churn", barmode="group", title="Churn by Contract")
    st.plotly_chart(bar_contract, use_container_width=True)

st.write("---")

col3, col4 = st.columns(2)
with col3:
    st.subheader("Churn by Internet Service")
    internet = df.groupby(["InternetService", "Churn"]).size().reset_index(name="Count")
    bar_internet = px.bar(internet, x="InternetService", y="Count", color="Churn", barmode="group", title="Churn by Internet Service")
    st.plotly_chart(bar_internet, use_container_width=True)

with col4:
    st.subheader("Average Monthly Charges")
    monthly = df.groupby("Churn")["MonthlyCharges"].mean().reset_index()
    bar_monthly = px.bar(monthly, x="Churn", y="MonthlyCharges", title="Average Monthly Charges: Churn vs Stay", color="Churn")
    st.plotly_chart(bar_monthly, use_container_width=True)

st.write("---")

st.subheader("Tenure distribution compared to churn")

df['tenure_bin'] = pd.cut(df['tenure'], bins=[0, 12, 24, 36, 48, 60, 72], labels=["0-12","13-24","25-36","37-48","49-60","61-72"])
tenure_dist = df.groupby(["tenure_bin", "Churn"]).size().reset_index(name="Count")

line = px.line(tenure_dist, x="tenure_bin", y="Count", color="Churn", markers=True, title="Tenure Bucket churn trend")
st.plotly_chart(line, use_container_width=True)

st.markdown("## Insight
- Customers on month-to-month contracts have the highest churn share.
- Fiber optic and no internet service segments show different churn patterns.
- Higher monthly charges correlate with higher churn rates on average.")