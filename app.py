import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Churn Sentinel Home", layout="wide", page_icon="🏠")

# --- Custom CSS for Netflix red/black theme ---
st.markdown(
    """
    <style>
    .stApp {
        background: #111111;
        color: #e0e0e0;
    }
    .css-1d391kg {
        padding: 1.5rem 2rem 2rem 2rem;
    }
    [data-testid="stSidebar"] {
        background: #141414 !important;
        color: #e0e0e0;
        border-right: 1px solid #333333;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] a {
        color: #e0e0e0 !important;
    }
    .section,
    .section-card,
    .chart-card {
        background: #1f1f1f;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        margin-bottom: 1.25rem;
        border: 1px solid #333333;
    }
    h1, h2, h3, .section h1, .section h2 {
        color: #ff0000;
    }
    p, .section p, .stTextInput>div, .stSelectbox>div {
        color: #dcdcdc;
    }
    .stButton>button {
        background-color: #e50914;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        border: none;
        font-weight: 700;
    }
    .stButton>button:hover {
        background-color: #b80610;
    }
    .stMetric > div {
        background: #222;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero Section
st.markdown("""
<div class='section'>
  <h1>🏡 Churn Sentinel AI</h1>
  <p style='font-size: 1.1rem; color:#1b3e78;'>Predict customer behavior and reduce churn using machine learning insights.</p>
  <div style='display:flex; gap:0.7rem; margin-top: 12px;'>
    <button onclick="window.location.href='?page=predict_customer'">🔵 Predict Customer</button>
    <button onclick="window.location.href='?page=dashboard'">📊 View Analytics</button>
  </div>
</div>
""", unsafe_allow_html=True)

# About Section
st.markdown("""
<div class='section'>
  <h2>About</h2>
  <p>This system helps businesses identify customers who are likely to leave by analyzing behavioral patterns and historical data.</p>
  <p>Using machine learning models, users can predict churn and take proactive actions to improve customer retention.</p>
  <p>Quickly get a snapshot of risk, and understand feature contributions with explainability outputs.</p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class='section'>
  <h2>Features</h2>
  <div style='display:flex; gap:1rem; flex-wrap:wrap;'>
    <div style='background:#ebf3ff; border-radius:10px; padding:1rem; flex:1; min-width:220px;'>
      <strong>🔍 Customer Prediction</strong><br>Predict whether a customer will churn.
    </div>
    <div style='background:#ebf3ff; border-radius:10px; padding:1rem; flex:1; min-width:220px;'>
      <strong>📈 Analytics Dashboard</strong><br>Visual insights of churn trends.
    </div>
    <div style='background:#ebf3ff; border-radius:10px; padding:1rem; flex:1; min-width:220px;'>
      <strong>⚡ Real-time Results</strong><br>Instant predictions and risk status.
    </div>
    <div style='background:#ebf3ff; border-radius:10px; padding:1rem; flex:1; min-width:220px;'>
      <strong>📂 Bulk Upload</strong><br>Upload CSV to analyze customer segments.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='section'>
  <h2>Footer</h2>
  <p><strong>Built by:</strong> Your Name</p>
  <p><strong>GitHub:</strong> <a href='https://github.com/yourusername' target='_blank'>https://github.com/yourusername</a></p>
  <p><strong>Project:</strong> Customer Churn Prediction with Streamlit and ML</p>
</div>
""", unsafe_allow_html=True)
