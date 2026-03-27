import streamlit as st
import pandas as pd
import plotly.express as px
import os

from components.styles import load_css, render_sidebar

st.set_page_config(page_title="Bulk Customer Segmentation", layout="wide", page_icon="🧩")
load_css()
render_sidebar(active_page="Segmentation")

st.markdown("<div class='page-header'>🧩 Bulk Customer Segmentation</div>", unsafe_allow_html=True)
st.write("Segment customers using historical churn data and prediction results to identify high-risk groups.")

# CSV upload option
upload_file = st.file_uploader("Upload bulk customer CSV for segmentation", type=["csv"], help="Upload a CSV file with same fields as base dataset")

csv_path = os.path.join(os.path.dirname(__file__), "WA_Fn-UseC_-Telco-Customer-Churn.csv")
if upload_file is not None:
    try:
        base_df = pd.read_csv(upload_file)
        st.success("CSV uploaded and loaded successfully")
    except Exception as e:
        st.error(f"Could not read uploaded file: {e}")
        st.stop()
else:
    if os.path.exists(csv_path):
        base_df = pd.read_csv(csv_path)
    else:
        st.error("Dataset csv not found in pages folder and no upload provided. Please add WA_Fn-UseC_-Telco-Customer-Churn.csv or upload a CSV.")
        st.stop()

hist_path = os.path.join(os.path.dirname(__file__), "predictions_history.csv")

# Load prediction history if available
pred_df = None
if os.path.exists(hist_path):
    pred_df = pd.read_csv(hist_path)
    if "predicted_churn" not in pred_df.columns and "pred_probability" in pred_df.columns:
        pred_df["predicted_churn"] = pred_df["pred_probability"].apply(lambda x: "Churn" if x > 0.5 else "No Churn")

st.write("## Available Data")
st.write("- Base dataset rows:", len(base_df))
if pred_df is not None:
    st.write("- Prediction history rows:", len(pred_df))
else:
    st.warning("Prediction history not found. Go to the Predict Customer page and generate some predictions first.")

st.write("---")

# Segmentation controls
st.sidebar.header("Segmentation Options")
segment_field = st.sidebar.selectbox("Segment by", ["Contract", "InternetService", "PaymentMethod", "SeniorCitizen"])
risk_threshold = st.sidebar.slider("Churn probability threshold", 0.0, 1.0, 0.5, 0.05)

if pred_df is not None:
    seg_df = pred_df.copy()
    seg_df["risk_level"] = seg_df["pred_probability"].apply(lambda x: "High" if x >= risk_threshold else "Low")

    st.write("## Bulk segmentation based on historical predictions")
    st.write(seg_df[[segment_field, "pred_probability", "risk_level"]].head(20))

    group = seg_df.groupby([segment_field, "risk_level"]).size().reset_index(name="count")
    fig = px.bar(group, x=segment_field, y="count", color="risk_level", barmode="group", title=f"Segmentation by {segment_field} (threshold {risk_threshold})")
    st.plotly_chart(fig, use_container_width=True)

    st.write("## Top high-risk segments")
    high_risk = seg_df[seg_df["risk_level"] == "High"].groupby(segment_field).size().reset_index(name="high_count").sort_values(by="high_count", ascending=False)
    st.write(high_risk.head(10))

    st.write("## Heatmap of numeric features vs churn probability")
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    corr_df = seg_df[numeric_cols + ["pred_probability"]].corr()
    st.write(corr_df)

    fig2 = px.imshow(corr_df, text_auto=True, title="Correlation matrix")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No prediction-based segmentation data available yet.")