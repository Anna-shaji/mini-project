import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0f0f0f;
        color: #e5e5e5;
    }

    .card {
        background: #1a1a1a;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #2a2a2a;
        margin-bottom: 1rem;
    }

    .title {
        color: #ff2b2b;
        font-size: 2rem;
        font-weight: bold;
    }

    .subtitle {
        color: #aaaaaa;
        font-size: 1rem;
    }

    .stButton>button {
        background-color: #e50914;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.6rem 1.2rem;
        border: none;
    }

    .stButton>button:hover {
        background-color: #b80610;
    }

    .stMetric {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)