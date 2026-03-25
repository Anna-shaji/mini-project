import streamlit as st
import pandas as pd
import plotly.express as px

import os
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "WA_Fn-UseC_-Telco-Customer-Churn.csv"))

st.title("Customer Churn Dashboard")

fig = px.pie(df, names="Churn", title="Churn Distribution")

st.plotly_chart(fig)