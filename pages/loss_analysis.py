import os

import pandas as pd
import plotly.express as px
import streamlit as st

from components.styles import load_css

st.set_page_config(page_title="Annual Loss Analysis", layout="wide", page_icon="💸")
load_css()

st.markdown("<div class='title'>💸 Annual Revenue Loss Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze expected churn loss by segment using uploaded data and prediction history.</div>", unsafe_allow_html=True)

# Data load
upload_file = st.file_uploader("Upload customer CSV (optional)", type=["csv"], help="Upload same schema as the base dataset")
base_csv_path = os.path.join(os.path.dirname(__file__), "WA_Fn-UseC_-Telco-Customer-Churn.csv")

base_df = None
pred_df = None
if upload_file is not None:
    try:
        base_df = pd.read_csv(upload_file)
        st.success("CSV uploaded and loaded successfully.")
        if "MonthlyCharges" in base_df.columns and "pred_probability" in base_df.columns:
            pred_df = base_df.copy()
            st.info("Using uploaded data for loss analysis based on pred_probability.")
    except Exception as exc:
        st.error(f"Unable to read uploaded CSV: {exc}")
        st.stop()
else:
    if os.path.exists(base_csv_path):
        base_df = pd.read_csv(base_csv_path)
    else:
        st.warning("No uploaded CSV and default dataset not found. Some features will not be available.")

if pred_df is None:
    history_path = os.path.join(os.path.dirname(__file__), "predictions_history.csv")
    if os.path.exists(history_path):
        try:
            pred_df = pd.read_csv(history_path)
        except Exception as exc:
            st.warning(f"Could not load prediction history: {exc}")
            pred_df = None
    else:
        st.warning("Prediction history not found. Generate predictions first in Predict Customer page.")

# Validate needed columns
required_pred_cols = ["MonthlyCharges", "pred_probability"]
if pred_df is not None:
    missing_pred_cols = [c for c in required_pred_cols if c not in pred_df.columns]
    if missing_pred_cols:
        st.warning(f"Prediction history missing columns: {', '.join(missing_pred_cols)}")
        pred_df = None

if pred_df is None:
    st.markdown("<div class='card'><h3>No analysis available</h3><p>Please upload data and have prediction history with MonthlyCharges + pred_probability.</p></div>", unsafe_allow_html=True)
    st.stop()

# Keep segment fields consistent
segment_fields = ["Contract", "InternetService", "PaymentMethod", "SeniorCitizen"]
# If pred_df lacks segment_column then fallback to base_df or warn
available_segment_fields = [f for f in segment_fields if f in pred_df.columns or (base_df is not None and f in base_df.columns)]
if not available_segment_fields:
    st.warning("No segmentation fields available in data (Contract/InternetService/PaymentMethod/SeniorCitizen).")
    st.stop()

st.sidebar.header("Segmentation Options")
segment_by = st.sidebar.selectbox("Segment by", available_segment_fields, index=0)

# Merge a best-effort dataset: start with prediction history for loss and segment data, fallback to base data for segment values
analysis_df = pred_df.copy()
if segment_by not in analysis_df.columns and base_df is not None and "customerID" in analysis_df.columns and "customerID" in base_df.columns:
    analysis_df = analysis_df.merge(base_df[["customerID", segment_by]], on="customerID", how="left")

# Ensure required columns exist for expected loss
if "MonthlyCharges" not in analysis_df.columns or "pred_probability" not in analysis_df.columns:
    st.error("Could not identify MonthlyCharges and pred_probability in merged data.")
    st.stop()

analysis_df = analysis_df.copy()
analysis_df["MonthlyCharges"] = pd.to_numeric(analysis_df["MonthlyCharges"], errors="coerce")
analysis_df["pred_probability"] = pd.to_numeric(analysis_df["pred_probability"], errors="coerce")
analysis_df = analysis_df.dropna(subset=["MonthlyCharges", "pred_probability"])

if analysis_df.empty:
    st.warning("No rows with valid MonthlyCharges and pred_probability available for analysis.")
    st.stop()

analysis_df["expected_loss"] = analysis_df["MonthlyCharges"] * 12 * analysis_df["pred_probability"]

# Loss category
def loss_category(value):
    if value > 10000:
        return "Critical"
    if value > 5000:
        return "High"
    return "Moderate"

analysis_df["loss_category"] = analysis_df["expected_loss"].apply(loss_category)

# Summary metrics
total_expected_loss = analysis_df["expected_loss"].sum()
avg_loss_per_customer = analysis_df["expected_loss"].mean()
high_risk_count = analysis_df[analysis_df["pred_probability"] > 0.5].shape[0]

st.markdown("<div class='card'><h3>Summary Metrics</h3></div>", unsafe_allow_html=True)
cols = st.columns(3)
cols[0].metric("Total Expected Annual Loss", f"₹{total_expected_loss:,.2f}")
cols[1].metric("Average Loss per Customer", f"₹{avg_loss_per_customer:,.2f}")
cols[2].metric("High-Risk Customers (p > 0.5)", f"{high_risk_count:,}")

# Segment-wise loss
if segment_by not in analysis_df.columns:
    st.warning(f"Selected segment field '{segment_by}' missing; using pred_df data.")

seg_table = analysis_df.groupby(segment_by, dropna=False)["expected_loss"].sum().reset_index().rename(columns={"expected_loss": "total_expected_loss"})
seg_table = seg_table.sort_values("total_expected_loss", ascending=False)

st.markdown("<div class='card'><h3>Segment-wise Expected Loss</h3></div>", unsafe_allow_html=True)
fig_segment = px.bar(
    seg_table,
    x=segment_by,
    y="total_expected_loss",
    color="total_expected_loss",
    color_continuous_scale="OrRd",
    labels={segment_by: segment_by, "total_expected_loss": "Total Expected Loss"},
    title=f"Total Expected Annual Loss by {segment_by}",
)
fig_segment.update_layout(plot_bgcolor="#0f0f0f", paper_bgcolor="#0f0f0f", font_color="#e5e5e5")

st.plotly_chart(fig_segment, use_container_width=True)

# Top segments
st.markdown("<div class='card'><h3>Top Loss-Contributing Segments</h3></div>", unsafe_allow_html=True)
st.dataframe(seg_table.head(10).style.format({"total_expected_loss": "₹{:,.2f}"}))

# Top customers
st.markdown("<div class='card'><h3>Top 10 Customers by Expected Loss</h3></div>", unsafe_allow_html=True)
key_cols = [c for c in ["customerID", "Contract", "InternetService", "PaymentMethod", "SeniorCitizen", "MonthlyCharges", "pred_probability", "expected_loss", "loss_category"] if c in analysis_df.columns]
top_customers = analysis_df.sort_values("expected_loss", ascending=False).head(10)
if top_customers.empty:
    st.warning("No customer-level rows found for top loss customers.")
else:
    st.dataframe(top_customers[key_cols].reset_index(drop=True).style.format({"MonthlyCharges": "₹{:,.2f}", "pred_probability": "{:.2f}", "expected_loss": "₹{:,.2f}"}))

# Loss category distribution
cat_table = analysis_df.groupby("loss_category")["expected_loss"].agg(total_loss="sum", customers="count").reset_index()

st.markdown("<div class='card'><h3>Loss Category Distribution</h3></div>", unsafe_allow_html=True)
if cat_table.empty:
    st.info("No loss categories to display.")
else:
    fig_pie = px.pie(
        cat_table,
        names="loss_category",
        values="customers",
        title="High/Medium/Critical Loss Customer Share",
        color_discrete_sequence=["#ff4b4b", "#ffa500", "#58d68d"],
    )
    fig_pie.update_layout(plot_bgcolor="#0f0f0f", paper_bgcolor="#0f0f0f", font_color="#e5e5e5")
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<div class='card'><em>Data source:</em> uploaded dataset (if provided) + prediction history from predictions_history.csv.</div>", unsafe_allow_html=True)
