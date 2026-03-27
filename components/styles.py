import streamlit as st


def load_css():
    st.markdown("""
    <style>
    :root {
      --background: #0f0f0f;
      --panel: #12151d;
      --card: #1a1a1a;
      --border: #2a2a2a;
      --accent: #2563eb;
      --accent-red: #e50914;
      --text: #edf0f9;
      --muted: #9aa8bf;
    }

    * {
      font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
      box-sizing: border-box;
    }

    body, .stApp, .css-1d391kg {
        background: var(--background) !important;
        color: var(--text) !important;
    }

    [data-testid="stSidebar"] {
        background: #0b0f16 !important;
        color: var(--text) !important;
        border-right: 1px solid #182330;
        padding: 1rem 0.75rem 1.25rem;
    }

    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    .sidebar-title {
        font-size: 1.95rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.15rem;
    }

    .sidebar-subtitle {
        color: var(--muted);
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }

    .sidebar-nav-link {
        display: flex;
        align-items: center;
        font-size: 1.06rem;
        font-weight: 600;
        color: #cfd8ef;
        padding: 0.64rem 0.9rem;
        border-radius: 10px;
        margin-bottom: 0.4rem;
        text-decoration: none !important;
        border-left: 3px solid transparent;
        transition: background 0.2s ease, color 0.2s ease, border-left 0.2s ease;
    }

    .sidebar-nav-link svg, .sidebar-nav-link .icon {
        margin-right: 0.7rem;
    }

    .sidebar-nav-link.active {
        background: #1a5cff;
        color: #ffffff !important;
        border-left: 3px solid #2563eb;
        box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.2);
    }

    .sidebar-nav-link:hover {
        background: #0e1d40;
        color: #ffffff !important;
    }

    .page-header {
        margin-bottom: 0.75rem;
        color: #ffffff;
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .card-container {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.35);
    }

    .section-title {
        color: #e5f1ff;
        font-size: 1.2rem;
        margin-bottom: 0.75rem;
        font-weight: 700;
    }

    .metric-light {
        color: #a7b7d9;
    }

    .result-card {
        background: #16212e;
        border: 1px solid #2a3b54;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar(active_page: str = "Home"):
    st.sidebar.markdown("<div class='sidebar-title'>Churn Sentinel AI</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='sidebar-subtitle'>Customer Analytics</div>", unsafe_allow_html=True)

    pages = [
        ("Home", "/", "🏠"),
        ("Dashboard", "/dashboard", "📊"),
        ("Predict Customer", "/predict_customer", "🔮"),
        ("Segmentation", "/segmentation", "🧩"),
        ("Loss Analysis", "/loss_analysis", "💸"),
    ]

    for label, link, icon in pages:
        active = "active" if label == active_page else ""
        st.sidebar.markdown(
            f"<a class='sidebar-nav-link {active}' href='{link}' target='_self'><span class='icon'>{icon}</span>{label}</a>",
            unsafe_allow_html=True,
        )

