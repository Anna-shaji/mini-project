import streamlit as st
from components.styles import load_css, render_sidebar

st.set_page_config(page_title="Churn Sentinel AI", page_icon="🏠", layout="wide")
load_css()
render_sidebar(active_page="Home")

st.markdown("<div class='page-header'>Home - Churn Sentinel AI</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🚀 Instant churn prediction suite</div>", unsafe_allow_html=True)
    st.write("Advanced analytics and machine learning to identify at-risk customers before they leave. Reduce churn, increase lifetime value, and boost retention.")
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        st.subheader("📊 Get started")
        st.write("Use the left menu to open pages:")
        st.write("• Predict Customer")
        st.write("• Dashboard")
        st.write("• Segmentation")
        st.write("• Loss Analysis")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        st.subheader("🎯 Quick stats")
        st.metric("Model accuracy", "86%", "Stable")
        st.metric("Focus", "Churn risk prediction", "Customer retention")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📌 About this app</div>", unsafe_allow_html=True)
    st.write("This tool helps businesses identify customers at risk of churn by combining feature-based ML predictions with analytics and loss modeling.")
    st.write("Recommendations are computed per customer and aggregated into dashboard reports.")
    st.write("Use the navigation sidebar to move between core application flows.")
    st.markdown("</div>", unsafe_allow_html=True)


