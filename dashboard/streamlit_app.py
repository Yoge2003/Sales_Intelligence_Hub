import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from datetime import date
import textwrap

from app.queries import (
    get_sales,
    add_sale,
    check_login,
    get_kpis,
    get_branch_sales,
    get_payment_analysis,
    get_branch_list,
    update_sale,
    delete_sale,
    get_sale_by_id,
    record_payment,
    get_sales_trend,
    get_product_performance,
    get_status_analysis,
    get_recent_activity,
    execute_custom_query,
)
import plotly.express as px
import plotly.graph_objects as go
import io


def init_page():
    st.set_page_config(
        page_title="Sales Intelligence Hub",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ─────────────────────────────────────────────────────────────────────────────
#  PREMIUM DARK DASHBOARD CSS  (via st.markdown – CSS injection is fine)
# ─────────────────────────────────────────────────────────────────────────────
def inject_dashboard_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp { background: #0a0e1a !important; font-family: 'Inter', sans-serif !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1120; }
::-webkit-scrollbar-thumb { background: #2a3a5c; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #4f7cff; }

.block-container { padding: 2rem 3rem !important; max-width: 1500px !important; background: transparent !important; }

[data-testid="stSidebar"] {
    background: #080c18 !important;
    border-right: 1px solid rgba(79,124,255,0.12) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.5) !important;
}
[data-testid="stSidebarContent"] { background: transparent !important; padding: 1.5rem 1rem !important; }

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #111827 0%, #0f1629 100%) !important;
    border: 1px solid rgba(79,124,255,0.15) !important;
    border-radius: 16px !important;
    padding: 1.6rem 1.4rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04) !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(79,124,255,0.5) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 16px 40px rgba(79,124,255,0.18), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
[data-testid="stMetric"]::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #4f7cff, #a78bfa, #06d6a0);
    border-radius: 16px 16px 0 0;
}
[data-testid="stMetricValue"] { color: #f0f6ff !important; font-weight: 800 !important; font-size: 26px !important; font-family: 'Inter', sans-serif !important; letter-spacing: -0.03em !important; }
[data-testid="stMetricLabel"] { color: #7c8db5 !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; font-family: 'Inter', sans-serif !important; }

.stButton > button {
    border-radius: 10px !important;
    border: 1px solid rgba(79,124,255,0.25) !important;
    background: rgba(79,124,255,0.08) !important;
    color: #a0b4e8 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: rgba(79,124,255,0.2) !important;
    border-color: rgba(79,124,255,0.6) !important;
    color: #e0eaff !important;
    box-shadow: 0 0 20px rgba(79,124,255,0.2) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #4f7cff 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    box-shadow: 0 4px 20px rgba(79,124,255,0.35) !important;
    transition: all 0.3s ease !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    box-shadow: 0 8px 30px rgba(79,124,255,0.5) !important;
    transform: translateY(-2px) !important;
}

.stTextInput input, .stNumberInput input, .stDateInput input {
    background: #0d1120 !important;
    border: 1px solid rgba(79,124,255,0.2) !important;
    border-radius: 10px !important;
    color: #e0eaff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.3) !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus {
    border-color: rgba(79,124,255,0.7) !important;
    box-shadow: 0 0 0 3px rgba(79,124,255,0.15), inset 0 2px 8px rgba(0,0,0,0.3) !important;
}

.stSelectbox > div[data-baseweb="select"] > div {
    background: #0d1120 !important;
    border: 1px solid rgba(79,124,255,0.2) !important;
    border-radius: 10px !important;
    color: #e0eaff !important;
}
div[data-baseweb="popover"] {
    background: #111827 !important;
    border: 1px solid rgba(79,124,255,0.2) !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7) !important;
}
div[data-baseweb="popover"] ul li { color: #c0d0f0 !important; background: transparent !important; }
div[data-baseweb="popover"] ul li:hover { background: rgba(79,124,255,0.15) !important; color: #fff !important; }

[data-testid="stTabs"] { background: transparent !important; }
[data-testid="stTabs"] > div:first-child {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(79,124,255,0.1) !important;
    padding: 4px !important;
}
[data-testid="stTabs"] button {
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    color: #7c8db5 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    border: none !important;
    transition: all 0.25s ease !important;
    background: transparent !important;
}
[data-testid="stTabs"] button:hover { color: #c0d0f0 !important; background: rgba(79,124,255,0.1) !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, rgba(79,124,255,0.25), rgba(124,58,237,0.2)) !important;
    color: #e0eaff !important;
    border: 1px solid rgba(79,124,255,0.3) !important;
    box-shadow: 0 4px 12px rgba(79,124,255,0.15) !important;
}

[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    border: 1px solid rgba(79,124,255,0.15) !important;
    overflow: hidden !important;
    background: #080c18 !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
}

[data-testid="stForm"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(79,124,255,0.12) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
}

[data-testid="stAlert"] { border-radius: 12px !important; font-family: 'Inter', sans-serif !important; font-size: 14px !important; }

h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif !important; color: #e8f0ff !important; }
p, span, label, div { font-family: 'Inter', sans-serif !important; }
.stMarkdown p { color: #8a9bc0 !important; font-size: 14px; }

[data-testid="stCheckbox"] label { color: #8a9bc0 !important; font-size: 13px !important; }

.js-plotly-plot { border-radius: 14px; overflow: hidden; }

[data-testid="stDownloadButton"] button {
    background: rgba(6,214,160,0.08) !important;
    border: 1px solid rgba(6,214,160,0.25) !important;
    color: #06d6a0 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.25s ease !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(6,214,160,0.18) !important;
    border-color: rgba(6,214,160,0.5) !important;
    box-shadow: 0 0 16px rgba(6,214,160,0.2) !important;
}

.sidebar-section-label {
    font-size: 10px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.12em; color: #3a4d6e;
    padding: 1.2rem 0.5rem 0.4rem; font-family: 'Inter', sans-serif;
}

code {
    background: rgba(79,124,255,0.12) !important;
    color: #a5b4fc !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
pre {
    background: #080c18 !important;
    border: 1px solid rgba(79,124,255,0.15) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""


def format_currency(value):
    return f"₹ {value:,.2f}" if value is not None else "₹ 0.00"


# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }

.stApp {
    background: radial-gradient(ellipse at 20% 50%, #0d1b3e 0%, #030712 50%, #0a0612 100%) !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 100vh;
}

.block-container {
    padding: 0 !important;
    max-width: 1100px !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    min-height: 100vh !important;
}

[data-testid="stColumn"]:nth-of-type(1) { padding: 4rem 4.5rem !important; }
[data-testid="stColumn"]:nth-of-type(2) { padding: 0 !important; }

.block-container > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(79,124,255,0.15) !important;
    border-radius: 28px !important;
    box-shadow: 0 40px 100px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    overflow: hidden !important;
    backdrop-filter: blur(20px) !important;
}

[data-testid="stForm"] { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }

[data-testid="stTextInput"] div div input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(79,124,255,0.2) !important;
    border-radius: 12px !important;
    color: #e0eaff !important;
    padding: 16px 18px !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.3) !important;
}
[data-testid="stTextInput"] div div { background: transparent !important; border: none !important; box-shadow: none !important; }
[data-testid="stTextInput"] div div:focus-within input {
    border-color: rgba(79,124,255,0.7) !important;
    box-shadow: 0 0 0 3px rgba(79,124,255,0.2), inset 0 2px 8px rgba(0,0,0,0.3) !important;
    background: rgba(79,124,255,0.07) !important;
}

[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #4f7cff 0%, #7c3aed 100%) !important;
    border-radius: 12px !important;
    width: 100% !important;
    padding: 1rem !important;
    border: none !important;
    margin-top: 0.5rem !important;
    box-shadow: 0 8px 32px rgba(79,124,255,0.4), 0 0 0 1px rgba(79,124,255,0.3) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFormSubmitButton"] button p { color: white !important; font-weight: 800 !important; font-size: 15px !important; letter-spacing: 0.06em !important; }
[data-testid="stFormSubmitButton"] button:hover { box-shadow: 0 12px 40px rgba(79,124,255,0.6) !important; transform: translateY(-2px) !important; }

[data-testid="stCheckbox"] label p { color: #5a6e94 !important; font-size: 13px !important; }
::placeholder { color: #3a4d6e !important; opacity: 1 !important; }
[data-testid="stMarkdownContainer"] p { color: #4a5e82 !important; font-size: 13px !important; }
[data-testid="stTextInput"] button { background: transparent !important; border: none !important; color: #4a5e82 !important; }
</style>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.15])

    with col1:
        st.html("""
<div style="margin-bottom: 2.5rem;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
<div style="width: 40px; height: 40px; background: linear-gradient(135deg, #4f7cff, #7c3aed);
            border-radius: 10px; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(79,124,255,0.4);">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
<polyline points="17 6 23 6 23 12"/>
</svg>
</div>
<span style="font-size: 18px; font-weight: 800; color: #e0eaff; letter-spacing: -0.02em;
             font-family: Inter, sans-serif;">SalesIQ Hub</span>
</div>
</div>
<h2 style="color: #f0f6ff; font-size: 32px; font-weight: 800; margin: 0 0 0.4rem 0;
           letter-spacing: -0.04em; line-height: 1.1; font-family: Inter, sans-serif;">
Welcome back
</h2>
<p style="color: #4a5e82; font-size: 15px; margin: 0 0 2.2rem 0; font-family: Inter, sans-serif;
          font-weight: 400; line-height: 1.5;">
Sign in to access your sales intelligence dashboard
</p>
""")

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

            st.html("""
<div style="text-align: right; margin-top: -10px; margin-bottom: 12px;">
<a href="#" style="color: #4f7cff; font-size: 13px; text-decoration: none; font-weight: 600;
                   font-family: Inter, sans-serif;">Forgot password?</a>
</div>
""")

            st.checkbox("Keep me signed in", key="login_remember")
            submitted = st.form_submit_button("SIGN IN →", use_container_width=True)

            st.html("""
<div style="text-align: center; margin-top: 1.8rem;">
<p style="color: #3a4d6e; font-size: 13px; font-family: Inter, sans-serif;">
Don't have access?
<a href="#" style="color: #4f7cff; font-weight: 700; text-decoration: none;">Contact Administrator</a>
</p>
</div>
""")

            if submitted:
                user = check_login(username.strip(), password.strip())
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.status_message = "Welcome back!"
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please check your username and password.")

    with col2:
        st.html("""
<div style="position: relative; height: 100%; min-height: 620px; overflow: hidden;
            background: linear-gradient(145deg, #0d1b4e 0%, #1a0a3e 50%, #0d1b4e 100%);
            display: flex; align-items: center; justify-content: center;">
<div style="position: absolute; width: 300px; height: 300px; border-radius: 50%;
            background: radial-gradient(circle, rgba(79,124,255,0.15) 0%, transparent 70%);
            top: -60px; right: -60px;"></div>
<div style="position: absolute; width: 200px; height: 200px; border-radius: 50%;
            background: radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%);
            bottom: 40px; left: -40px;"></div>
<div style="position: absolute; inset: 0; opacity: 0.04;
            background-image: linear-gradient(rgba(79,124,255,0.5) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(79,124,255,0.5) 1px, transparent 1px);
            background-size: 40px 40px;"></div>
<div style="position: relative; z-index: 10; width: 85%; text-align: center; padding: 50px 30px;">
<div style="width: 80px; height: 80px; margin: 0 auto 28px;
            background: linear-gradient(135deg, rgba(79,124,255,0.2), rgba(124,58,237,0.2));
            border: 1px solid rgba(79,124,255,0.3); border-radius: 20px;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 8px 32px rgba(79,124,255,0.2);">
<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#4f7cff" stroke-width="1.8"
     stroke-linecap="round" stroke-linejoin="round">
<line x1="18" y1="20" x2="18" y2="10"/>
<line x1="12" y1="20" x2="12" y2="4"/>
<line x1="6" y1="20" x2="6" y2="14"/>
</svg>
</div>
<h3 style="color: #e8f0ff; font-size: 26px; font-weight: 800; letter-spacing: -0.04em;
           margin: 0 0 16px; font-family: Inter, sans-serif; line-height: 1.2;">
Sales Intelligence Hub
</h3>
<p style="color: rgba(180,200,240,0.65); font-size: 14px; line-height: 1.7;
          font-family: Inter, sans-serif; font-weight: 400; margin: 0 0 36px;">
Transforming raw data into actionable intelligence. Centralized. Real-time. Precise.
</p>
<div style="display: flex; flex-direction: column; gap: 10px; text-align: left;">
<div style="background: rgba(79,124,255,0.08); border: 1px solid rgba(79,124,255,0.18);
            border-radius: 10px; padding: 12px 18px; display: flex; align-items: center; gap: 12px;">
<div style="width: 32px; height: 32px; background: rgba(79,124,255,0.15); border-radius: 8px;
            display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4f7cff" stroke-width="2.5" stroke-linecap="round">
<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
</svg>
</div>
<span style="color: #a0b4e8; font-size: 13px; font-weight: 600; font-family: Inter, sans-serif;">Real-time KPI Monitoring</span>
</div>
<div style="background: rgba(124,58,237,0.08); border: 1px solid rgba(124,58,237,0.18);
            border-radius: 10px; padding: 12px 18px; display: flex; align-items: center; gap: 12px;">
<div style="width: 32px; height: 32px; background: rgba(124,58,237,0.15); border-radius: 8px;
            display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2.5" stroke-linecap="round">
<rect x="3" y="3" width="18" height="18" rx="2"/><rect x="9" y="9" width="6" height="6"/>
</svg>
</div>
<span style="color: #a0b4e8; font-size: 13px; font-weight: 600; font-family: Inter, sans-serif;">Multi-Branch Analytics</span>
</div>
<div style="background: rgba(6,214,160,0.06); border: 1px solid rgba(6,214,160,0.15);
            border-radius: 10px; padding: 12px 18px; display: flex; align-items: center; gap: 12px;">
<div style="width: 32px; height: 32px; background: rgba(6,214,160,0.12); border-radius: 8px;
            display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#06d6a0" stroke-width="2.5" stroke-linecap="round">
<polyline points="20 6 9 17 4 12"/>
</svg>
</div>
<span style="color: #a0b4e8; font-size: 13px; font-weight: 600; font-family: Inter, sans-serif;">Smart Payment Tracking</span>
</div>
</div>
</div>
</div>
""")


def show_logout():
    st.sidebar.html("""
<div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(79,124,255,0.2), transparent); margin: 1rem 0;"></div>
""")
    if st.sidebar.button("⎋  Sign Out", use_container_width=True, type="secondary"):
        st.session_state.clear()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  DASHBOARD HEADER
# ─────────────────────────────────────────────────────────────────────────────
def display_header(user):
    role_badge_color = "#4f7cff" if user['role'] == "super_admin" else "#06d6a0"
    role_badge_bg = "rgba(79,124,255,0.12)" if user['role'] == "super_admin" else "rgba(6,214,160,0.1)"
    role_text = user['role'].replace('_', ' ')

    st.html(f"""
<div style="background: linear-gradient(135deg, #0d1629 0%, #111827 100%);
            border: 1px solid rgba(79,124,255,0.15); border-radius: 20px;
            padding: 28px 36px; margin-bottom: 28px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);
            display: flex; justify-content: space-between; align-items: center;
            position: relative; overflow: hidden;">
<div style="position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, #4f7cff, #a78bfa, #06d6a0);"></div>
<div style="display: flex; align-items: center; gap: 14px;">
<div style="width: 44px; height: 44px; background: linear-gradient(135deg, #4f7cff, #7c3aed);
            border-radius: 12px; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(79,124,255,0.4); flex-shrink: 0;">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white"
     stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
<polyline points="17 6 23 6 23 12"/>
</svg>
</div>
<div>
<h1 style="margin: 0; font-size: 26px; color: #f0f6ff; font-weight: 800;
           letter-spacing: -0.04em; font-family: Inter, sans-serif; line-height: 1;">
Sales Intelligence Hub
</h1>
<p style="margin: 4px 0 0; color: #4a5e82; font-size: 13px; font-weight: 400; font-family: Inter, sans-serif;">
Centralized sales monitoring &amp; analytics platform
</p>
</div>
</div>
<div style="display: flex; align-items: center; gap: 12px; flex-shrink: 0;">
<div style="background: {role_badge_bg}; border: 1px solid {role_badge_color}40;
            border-radius: 20px; padding: 6px 14px; font-size: 12px; font-weight: 700;
            color: {role_badge_color}; font-family: Inter, sans-serif;
            letter-spacing: 0.04em; text-transform: uppercase;">
{role_text}
</div>
<div style="background: rgba(6,214,160,0.08); border: 1px solid rgba(6,214,160,0.2);
            border-radius: 20px; padding: 6px 14px; font-size: 12px;
            color: #06d6a0; font-family: Inter, sans-serif; font-weight: 600;
            display: flex; align-items: center; gap: 6px;">
<span style="display: inline-block; width: 7px; height: 7px; background: #06d6a0;
             border-radius: 50%; box-shadow: 0 0 6px #06d6a0;"></span>
Live
</div>
</div>
</div>
""")

    col1, col2, col3 = st.columns([1, 1, 1.5])
    with col1:
        st.metric("Logged in as", f"{user['username']}")
    with col2:
        display_role = st.session_state.user['role']
        st.metric("System Role", f"{display_role.replace('_', ' ').title()}")
    with col3:
        if st.session_state.user["role"] == "super_admin":
            scope_label = "All Branches"
        else:
            if "branch_name" in user and user["branch_name"]:
                scope_label = user["branch_name"]
            else:
                branches = get_branch_list()
                found_name = next((b["branch_name"] for b in branches if b["branch_id"] == user["branch_id"]), None)
                scope_label = found_name if found_name else f"Branch {user.get('branch_id')}"
                st.session_state.user["branch_name"] = scope_label
        st.metric("Access Scope", scope_label)

    if st.session_state.status_message:
        st.success(st.session_state.status_message)
        st.session_state.status_message = ""


# ─────────────────────────────────────────────────────────────────────────────
#  CHART STYLE
# ─────────────────────────────────────────────────────────────────────────────
def apply_chart_style(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        font_color="#c0d0f0",
        margin=dict(l=60, r=20, t=50, b=90),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.42,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#8a9bc0"),
            bgcolor="rgba(0,0,0,0)"
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=13,
            font_family="Inter",
            bordercolor="#4f7cff"
        )
    )
    fig.update_yaxes(
        title_standoff=25,
        showgrid=True,
        gridcolor="rgba(79,124,255,0.08)",
        zeroline=False,
        tickfont=dict(color="#5a6e94", size=11),
        title_font=dict(color="#5a6e94")
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        tickangle=-45,
        categoryorder="category ascending",
        tickfont=dict(color="#5a6e94", size=11),
        title_font=dict(color="#5a6e94")
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION HEADER HELPER
# ─────────────────────────────────────────────────────────────────────────────
def section_header(icon, title, subtitle=""):
    sub_html = f'<p style="margin: 2px 0 0; font-size: 13px; color: #4a5e82; font-family: Inter, sans-serif;">{subtitle}</p>' if subtitle else ""
    st.html(f"""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 22px; margin-top: 8px;">
<div style="width: 38px; height: 38px; background: linear-gradient(135deg, rgba(79,124,255,0.2), rgba(124,58,237,0.2));
            border: 1px solid rgba(79,124,255,0.25); border-radius: 10px;
            display: flex; align-items: center; justify-content: center; font-size: 18px;
            box-shadow: 0 4px 12px rgba(79,124,255,0.1); flex-shrink: 0;">
{icon}
</div>
<div>
<h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #e0eaff;
           letter-spacing: -0.02em; font-family: Inter, sans-serif;">{title}</h3>
{sub_html}
</div>
</div>
""")


# ─────────────────────────────────────────────────────────────────────────────
#  OVERVIEW TAB
# ─────────────────────────────────────────────────────────────────────────────
def render_overview(user, start_date=None, end_date=None, product_filter=None):
    section_header("📊", "Executive Summary", "Real-time performance metrics across your scope")

    total_sales, total_received, total_pending, sale_count = get_kpis(user, start_date, end_date, product_filter)

    collection_rate = (total_received / total_sales * 100) if total_sales > 0 else 0
    aov = (total_sales / sale_count) if sale_count > 0 else 0

    metric_cols = st.columns(5)
    metric_cols[0].metric("Total Revenue", format_currency(total_sales))
    metric_cols[1].metric("Amount Collected", format_currency(total_received))
    metric_cols[2].metric("Pending Amount", format_currency(total_pending), delta=f"-{format_currency(total_pending)}", delta_color="inverse")
    metric_cols[3].metric("Collection Rate", f"{collection_rate:.1f}%")
    metric_cols[4].metric("Avg Order Value", format_currency(aov))

    st.html("<div style='height: 28px'></div>")

    main_col, activity_col = st.columns([2.5, 1])

    with main_col:
        st.html("""
<div style="font-weight: 700; color: #c0d0f0; font-size: 15px; margin-bottom: 14px; font-family: Inter, sans-serif;">
📈 Revenue Trend
</div>
""")
        df_trend = get_sales_trend(user, start_date, end_date, product_filter)
        if not df_trend.empty:
            fig_trend = px.area(
                df_trend,
                x="sale_date",
                y="daily_sales",
                color_discrete_sequence=["#4f7cff"],
                labels={"sale_date": "Date", "daily_sales": "Revenue (₹)"}
            )
            fig_trend.update_traces(
                line_width=2.5,
                fillcolor="rgba(79,124,255,0.1)",
                hovertemplate="<b>Date:</b> %{x}<br><b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
            )
            apply_chart_style(fig_trend)
            fig_trend.update_xaxes(type='category')
            st.plotly_chart(fig_trend, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No trend data available for this range.")

    with activity_col:
        st.html("""
<div style="font-weight: 700; color: #c0d0f0; font-size: 15px; margin-bottom: 14px; font-family: Inter, sans-serif;">
⚡ Recent Activity
</div>
""")
        df_activity = get_recent_activity(user)
        if not df_activity.empty:
            for _, row in df_activity.iterrows():
                with st.container():
                    st.html(f"""
<div style="background: rgba(255,255,255,0.025); border: 1px solid rgba(79,124,255,0.12);
            border-left: 3px solid #4f7cff; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;">
<div style="font-size: 10px; color: #3a4d6e; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.08em; margin-bottom: 5px; font-family: Inter, sans-serif;">
{row['date']}
</div>
<div style="font-size: 14px; font-weight: 700; color: #c0d0f0; margin-bottom: 8px;
            font-family: Inter, sans-serif; letter-spacing: -0.01em;">
{row['customer']}
</div>
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 11px; color: #4f7cff; font-weight: 700;
             background: rgba(79,124,255,0.1); padding: 3px 8px; border-radius: 6px; font-family: Inter, sans-serif;">
{row['product']}
</span>
<span style="font-size: 13px; font-weight: 800; color: #06d6a0; font-family: Inter, sans-serif; letter-spacing: -0.01em;">
&#8377;{row['gross_sales']:,.0f}
</span>
</div>
</div>
""")
        else:
            st.info("No recent activity.")

    st.html("<div style='height: 20px'></div>")

    chart_cols = st.columns(3)

    with chart_cols[0]:
        if user["role"] == "super_admin":
            st.html("""<div style="font-weight: 700; color: #c0d0f0; font-size: 14px; margin-bottom: 14px; font-family: Inter, sans-serif;">🏢 Sales by Branch</div>""")
            df_branch = get_branch_sales(user, start_date, end_date, product_filter)
            if not df_branch.empty:
                fig_branch = px.bar(
                    df_branch, x="branch_name", y="total_sales",
                    color="total_sales", color_continuous_scale=["#1a2a5e", "#4f7cff"],
                    labels={"branch_name": "Branch", "total_sales": "Sales"}
                )
                apply_chart_style(fig_branch)
                fig_branch.update_coloraxes(showscale=False)
                fig_branch.update_traces(
                    marker_line_width=0, marker_pattern_shape="",
                    hovertemplate="<b>%{x}</b><br>Sales: ₹%{y:,.2f}<extra></extra>"
                )
                st.plotly_chart(fig_branch, use_container_width=True, theme=None, config={'displayModeBar': False})
            else:
                st.info("No branch sales data.")
        else:
            st.html("""<div style="font-weight: 700; color: #c0d0f0; font-size: 14px; margin-bottom: 14px; font-family: Inter, sans-serif;">📊 Status Breakdown</div>""")
            df_status = get_status_analysis(user, start_date, end_date, product_filter)
            if not df_status.empty:
                fig_status = px.pie(
                    df_status, names="status", values="total_value", hole=0.68,
                    color="status",
                    color_discrete_map={"Open": "#f59e0b", "Close": "#06d6a0"},
                    labels={"status": "Status", "total_value": "Revenue"}
                )
                apply_chart_style(fig_status)
                fig_status.update_traces(
                    textposition='inside', textinfo='percent',
                    marker=dict(line=dict(color='#0a0e1a', width=3)),
                    hovertemplate="<b>%{label}</b><br>Value: ₹%{value:,.2f}<br>Count: %{customdata[0]}<extra></extra>",
                    customdata=df_status[['count']]
                )
                st.plotly_chart(fig_status, use_container_width=True, theme=None, config={'displayModeBar': False})
            else:
                st.info("No status data.")

    with chart_cols[1]:
        st.html("""<div style="font-weight: 700; color: #c0d0f0; font-size: 14px; margin-bottom: 14px; font-family: Inter, sans-serif;">📦 Product Mix</div>""")
        df_prod = get_product_performance(user, start_date, end_date, product_filter)
        if not df_prod.empty:
            fig_prod = px.pie(
                df_prod, names="product_name", values="total_sales", hole=0.68,
                color_discrete_sequence=["#4f7cff", "#a78bfa", "#06d6a0", "#f59e0b"]
            )
            apply_chart_style(fig_prod)
            fig_prod.update_traces(
                textposition='inside', textinfo='percent',
                marker=dict(line=dict(color='#0a0e1a', width=3)),
                hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>"
            )
            st.plotly_chart(fig_prod, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No product data for this range.")

    with chart_cols[2]:
        st.html("""<div style="font-weight: 700; color: #c0d0f0; font-size: 14px; margin-bottom: 14px; font-family: Inter, sans-serif;">💳 Payment Channels</div>""")
        df_payment = get_payment_analysis(user, start_date, end_date, product_filter)
        if not df_payment.empty:
            fig_payment = px.pie(
                df_payment, names="payment_method", values="total", hole=0.68,
                color_discrete_sequence=["#06d6a0", "#f59e0b", "#a78bfa", "#f43f5e"]
            )
            apply_chart_style(fig_payment)
            fig_payment.update_traces(
                textposition='inside', textinfo='percent',
                marker=dict(line=dict(color='#0a0e1a', width=3)),
                hovertemplate="<b>%{label}</b><br>Volume: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>"
            )
            st.plotly_chart(fig_payment, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No payment data for this range.")


# ─────────────────────────────────────────────────────────────────────────────
#  SALES TABLE TAB
# ─────────────────────────────────────────────────────────────────────────────
def render_sales_table(user, start_date=None, end_date=None, product_filter=None):
    section_header("🗃️", "Sales Records", "View, edit and manage all sales entries")

    st.html("""
<div style="background: rgba(79,124,255,0.06); border: 1px solid rgba(79,124,255,0.15);
            border-left: 3px solid #4f7cff; border-radius: 10px; padding: 12px 18px;
            margin-bottom: 20px; font-size: 13px; color: #7c8db5; font-family: Inter, sans-serif;">
💡 <strong style="color: #a0b4e8;">Pro Tip:</strong>
Double-click any cell to edit inline. Select a row and press Delete to remove. All changes are saved instantly.
</div>
""")

    df = get_sales(user, start_date, end_date, product_filter)
    if df.empty:
        st.info("No sales records found for the selected filters.")
        return

    df = df.set_index("sale_id")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="sales_data_editor"
    )

    st.html("<div style='height: 12px'></div>")

    col_csv, col_excel, col_json, col_pdf = st.columns(4)

    csv = df.to_csv(index=True).encode('utf-8')
    col_csv.download_button(label="⬇ Export CSV", data=csv, file_name='sales_records.csv', mime='text/csv', type="secondary", use_container_width=True)

    import io
    excel_buffer = io.BytesIO()
    with __import__('pandas').ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=True)
    col_excel.download_button(label="⬇ Export Excel", data=excel_buffer.getvalue(), file_name='sales_records.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', type="secondary", use_container_width=True)

    json_data = df.reset_index().to_json(orient="records").encode('utf-8')
    col_json.download_button(label="⬇ Export JSON", data=json_data, file_name='sales_records.json', mime='application/json', type="secondary", use_container_width=True)

    from fpdf import FPDF
    def generate_pdf(dataframe):
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("helvetica", style="B", size=14)
        pdf.cell(0, 10, "Sales Records Export", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("helvetica", style="B", size=8)
        df_pdf = dataframe.reset_index()
        columns = df_pdf.columns.tolist()
        col_width = pdf.epw / len(columns)
        for col in columns:
            pdf.cell(col_width, 8, str(col)[:20].replace("_", " ").title(), border=1, align="C")
        pdf.ln()
        pdf.set_font("helvetica", size=7)
        for i in range(len(df_pdf)):
            row = df_pdf.iloc[i]
            for col in columns:
                val = str(row[col]).encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(col_width, 6, val[:20], border=1, align="C")
            pdf.ln()
        return bytes(pdf.output())

    col_pdf.download_button(label="⬇ Export PDF", data=generate_pdf(df), file_name='sales_records.pdf', mime='application/pdf', type="secondary", use_container_width=True)

    changes = st.session_state.get("sales_data_editor")
    if changes:
        has_changed = False
        for row_idx, updates in changes.get("edited_rows", {}).items():
            sale_id = int(df.index[row_idx])
            update_sale(sale_id, updates)
            has_changed = True
        for row_idx in changes.get("deleted_rows", []):
            sale_id = int(df.index[row_idx])
            delete_sale(sale_id)
            has_changed = True
        if has_changed:
            st.success("✅ Database updated successfully!")
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  ADD PAYMENT TAB
# ─────────────────────────────────────────────────────────────────────────────
def render_add_payment(user):
    section_header("💰", "Record Payment", "Add a new payment against an existing sale")

    st.html("""
<div style="background: rgba(79,124,255,0.06); border: 1px solid rgba(79,124,255,0.15);
            border-left: 3px solid #a78bfa; border-radius: 10px; padding: 12px 18px;
            margin-bottom: 20px; font-size: 13px; color: #7c8db5; font-family: Inter, sans-serif;">
🔍 Enter the <strong style="color: #a0b4e8;">Sale ID</strong> to look up the sale and record a payment.
</div>
""")

    search_id = st.number_input("Enter Sale ID to Search", min_value=1, step=1, key="payment_search_id")

    if search_id:
        df = get_sale_by_id(search_id, user)
        if df.empty:
            st.warning(f"No active sale found with ID **{search_id}** in your accessible branch.")
        else:
            sale = df.iloc[0]
            status_bg = "rgba(239,68,68,0.12)" if sale['status'] == 'Open' else "rgba(6,214,160,0.1)"
            status_color = "#f87171" if sale['status'] == 'Open' else "#06d6a0"
            status_border = "rgba(239,68,68,0.3)" if sale['status'] == 'Open' else "rgba(6,214,160,0.3)"

            st.html(f"""
<div style="background: linear-gradient(135deg, #0d1629, #111827);
            border: 1px solid rgba(79,124,255,0.2); border-radius: 16px;
            padding: 24px 28px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
<div style="font-size: 10px; font-weight: 800; text-transform: uppercase;
            letter-spacing: 0.1em; color: #3a4d6e; margin-bottom: 16px; font-family: Inter, sans-serif;">
Sale Overview &middot; ID #{search_id}
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
<div>
<div style="font-size: 11px; color: #4a5e82; font-weight: 600; margin-bottom: 4px; font-family: Inter, sans-serif; text-transform: uppercase; letter-spacing: 0.06em;">Customer</div>
<div style="font-size: 16px; font-weight: 700; color: #e0eaff; font-family: Inter, sans-serif;">{sale['name']}</div>
</div>
<div>
<div style="font-size: 11px; color: #4a5e82; font-weight: 600; margin-bottom: 4px; font-family: Inter, sans-serif; text-transform: uppercase; letter-spacing: 0.06em;">Product</div>
<div style="font-size: 16px; font-weight: 700; color: #a78bfa; font-family: Inter, sans-serif;">{sale['product_name']}</div>
</div>
<div>
<div style="font-size: 11px; color: #4a5e82; font-weight: 600; margin-bottom: 4px; font-family: Inter, sans-serif; text-transform: uppercase; letter-spacing: 0.06em;">Status</div>
<span style="background: {status_bg}; color: {status_color}; border: 1px solid {status_border};
             padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; font-family: Inter, sans-serif;">
{sale['status']}
</span>
</div>
<div>
<div style="font-size: 11px; color: #4a5e82; font-weight: 600; margin-bottom: 4px; font-family: Inter, sans-serif; text-transform: uppercase; letter-spacing: 0.06em;">Total Sale</div>
<div style="font-size: 16px; font-weight: 800; color: #e0eaff; font-family: Inter, sans-serif; letter-spacing: -0.02em;">{format_currency(sale['gross_sales'])}</div>
</div>
<div>
<div style="font-size: 11px; color: #4a5e82; font-weight: 600; margin-bottom: 4px; font-family: Inter, sans-serif; text-transform: uppercase; letter-spacing: 0.06em;">Collected</div>
<div style="font-size: 16px; font-weight: 800; color: #06d6a0; font-family: Inter, sans-serif; letter-spacing: -0.02em;">{format_currency(sale['received_amount'])}</div>
</div>
<div>
<div style="font-size: 11px; color: #4a5e82; font-weight: 600; margin-bottom: 4px; font-family: Inter, sans-serif; text-transform: uppercase; letter-spacing: 0.06em;">Pending</div>
<div style="font-size: 16px; font-weight: 800; color: #f87171; font-family: Inter, sans-serif; letter-spacing: -0.02em;">{format_currency(sale['pending_amount'])}</div>
</div>
</div>
</div>
""")

            if sale['status'] == 'Close':
                st.error("🔒 This sale is **CLOSED**. No further payments can be recorded against it.")
            else:
                with st.form("payment_form"):
                    pay_date = st.date_input("Payment Date", value=date.today())
                    pay_amount = st.number_input("Payment Amount (₹)", min_value=0.0, max_value=float(sale['pending_amount']), format="%.2f")
                    pay_method = st.selectbox("Payment Method", ["Cash", "UPI", "Bank Transfer", "Card"])

                    if st.form_submit_button("✅ Record Payment", use_container_width=True):
                        if pay_amount <= 0:
                            st.error("Please enter a valid payment amount greater than zero.")
                        else:
                            record_payment(search_id, pay_amount, pay_method, pay_date)
                            st.success(f"✅ Payment of **{format_currency(pay_amount)}** recorded for Sale ID **{search_id}**")
                            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  ADD SALE TAB
# ─────────────────────────────────────────────────────────────────────────────
def render_add_sale(user):
    section_header("➕", "New Sale Entry", "Create a new sales record with initial payment")

    branch_id = user["branch_id"]
    if user["role"] == "super_admin":
        branches = get_branch_list()
        options = [f"{branch['branch_id']} - {branch['branch_name']}" for branch in branches]
        selected = st.selectbox("Select Branch", options)
        branch_id = int(selected.split(" - ")[0]) if selected else branch_id

    with st.form("sale_form"):
        st.html("""
<div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
            color: #3a4d6e; margin-bottom: 16px; font-family: Inter, sans-serif;">
Customer &amp; Sale Details
</div>
""")
        sale_date = st.date_input("Sale Date", value=date.today(), help="Select the date of the sale")
        customer_name = st.text_input("Customer Name", placeholder="Enter the customer's full name", help="Full name of the purchasing customer")
        mobile_number = st.text_input("Mobile Number", placeholder="Enter 10-digit mobile number", help="Customer contact number")
        product_name = st.selectbox("Product", ["DS", "DA", "BA", "FSD"], help="Select the product purchased")

        st.html("""
<div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
            color: #3a4d6e; margin: 20px 0 14px; font-family: Inter, sans-serif;">
Financial Details
</div>
""")
        col_amt, col_pay = st.columns(2)
        with col_amt:
            gross_amt = st.number_input("Total Sale Amount (₹)", min_value=0.0, format="%.2f", help="Full price of the product")
            received_amt = st.number_input("Initial Payment Received (₹)", min_value=0.0, format="%.2f", help="Upfront payment collected")
        with col_pay:
            pay_method = st.selectbox("Payment Method", ["N/A", "Cash", "UPI", "Bank Transfer", "Card"])

        st.html("<div style='height: 8px'></div>")
        submitted = st.form_submit_button("🚀 Create Sale Record", use_container_width=True)

        if submitted:
            if not customer_name or not mobile_number or gross_amt <= 0:
                st.error("⚠️ Please provide Customer Name, Mobile Number, and a valid Sale Amount.")
            elif received_amt > gross_amt:
                st.error("⚠️ Received amount cannot exceed the total sale amount.")
            else:
                new_id = add_sale(branch_id, sale_date, customer_name, mobile_number, product_name, gross_amt, received_amt, pay_method)
                st.success(f"🎊 Sale created successfully! Sale ID assigned: **#{new_id}**")
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  QUERY REPORTS TAB
# ─────────────────────────────────────────────────────────────────────────────
def parse_sql_queries(file_path):
    queries = {}
    current_name = None
    current_query = []

    if not os.path.exists(file_path):
        return queries

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("#"):
                if current_name and current_query:
                    queries[current_name] = " \n".join(current_query)
                current_name = line_str[1:].strip()
                current_query = []
            else:
                current_query.append(line_str)
        if current_name and current_query:
            queries[current_name] = " \n".join(current_query)
    return queries


def render_query_reports():
    section_header("🔬", "SQL Query Reports", "Execute predefined analytical queries and export results")

    reports_file = os.path.join(os.path.dirname(__file__), '..', 'reports', 'sql_queries.sql')
    queries = parse_sql_queries(reports_file)

    if not queries:
        st.warning("⚠️ Could not find any SQL queries in `reports/sql_queries.sql`")
        return

    selected_report = st.selectbox("Select Report to Generate", list(queries.keys()))

    if selected_report:
        sql = queries[selected_report]
        st.html("""<div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #3a4d6e; margin-bottom: 10px; font-family: Inter, sans-serif;">Query Logic</div>""")
        st.code(sql, language="sql")

        if st.button("▶  Execute Report", type="primary"):
            with st.spinner("Running query…"):
                df = execute_custom_query(sql)
                if 'Error' in df.columns and len(df) == 1:
                    st.error(f"Execution error: {df.iloc[0]['Error']}")
                else:
                    st.success(f"✅ Report generated — **{len(df)} rows** returned.")
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇ Download as CSV",
                        data=csv,
                        file_name=f"{selected_report.replace(' ', '_').lower()}.csv",
                        mime="text/csv",
                    )


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────
def main():
    init_page()
    init_session_state()

    if not st.session_state.logged_in:
        show_login()
        st.stop()

    inject_dashboard_css()

    user = st.session_state.user
    user_context = dict(user)

    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    if user["role"] == "super_admin":
        col_bf_l, col_bf_r = st.sidebar.columns([5, 1])
        with col_bf_l:
            st.html("""<div class="sidebar-section-label">Branch Filter</div>""")

        branches = get_branch_list()
        options = ["All Branches"] + [f"{branch['branch_id']} - {branch['branch_name']}" for branch in branches]

        def reset_branch_callback():
            st.session_state["filter_branch"] = "All Branches"

        with col_bf_r:
            st.button("↻", key="reset_branch", on_click=reset_branch_callback, use_container_width=True, help="Reset Branch Filter")

        selected_branch = st.sidebar.selectbox("Select Branch", options, key="filter_branch", label_visibility="collapsed")

        if selected_branch != "All Branches":
            branch_id_selected = int(selected_branch.split(" - ")[0])
            branch_name_selected = selected_branch.split(" - ")[1]
            user_context["role"] = "admin"
            user_context["branch_id"] = branch_id_selected
            user_context["branch_name"] = branch_name_selected

        active_scope = "All Branches"
    else:
        active_scope = user.get("branch_name")
        if not active_scope:
            branches = get_branch_list()
            found_name = next((b["branch_name"] for b in branches if b["branch_id"] == user["branch_id"]), None)
            active_scope = found_name if found_name else f"Branch {user.get('branch_id')}"
            user_context["branch_name"] = active_scope

    # Sidebar user card
    role_color = "#4f7cff" if user["role"] == "super_admin" else "#06d6a0"
    avatar_letter = user["username"][0].upper()
    role_title = user["role"].replace('_', ' ').title()

    st.sidebar.html(f"""
<div style="background: linear-gradient(145deg, #0d1b3e, #0a1228);
            border: 1px solid rgba(79,124,255,0.2); border-radius: 16px;
            padding: 20px 18px; margin-bottom: 8px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);">
<div style="display: flex; align-items: center; gap: 13px; margin-bottom: 18px;">
<div style="width: 42px; height: 42px; flex-shrink: 0;
            background: linear-gradient(135deg, #4f7cff, #7c3aed); border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 17px; font-weight: 900; color: white; text-transform: uppercase;
            box-shadow: 0 4px 14px rgba(79,124,255,0.35); font-family: Inter, sans-serif;">
{avatar_letter}
</div>
<div>
<p style="margin: 0; font-size: 10px; color: #3a4d6e; text-transform: uppercase;
          font-weight: 700; letter-spacing: 0.08em; font-family: Inter, sans-serif;">Signed in as</p>
<h3 style="margin: 3px 0 0; font-size: 15px; font-weight: 700; color: #e0eaff;
           font-family: Inter, sans-serif; letter-spacing: -0.02em;">{user["username"]}</h3>
</div>
</div>
<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
            border-radius: 10px; padding: 13px 14px;">
<div style="margin-bottom: 10px;">
<span style="font-size: 10px; color: #3a4d6e; font-weight: 700; text-transform: uppercase;
             letter-spacing: 0.08em; display: block; margin-bottom: 3px; font-family: Inter, sans-serif;">Role</span>
<span style="font-size: 13px; font-weight: 700; color: {role_color}; font-family: Inter, sans-serif;">{role_title}</span>
</div>
<div>
<span style="font-size: 10px; color: #3a4d6e; font-weight: 700; text-transform: uppercase;
             letter-spacing: 0.08em; display: block; margin-bottom: 3px; font-family: Inter, sans-serif;">Access Scope</span>
<span style="font-size: 13px; font-weight: 600; color: #8a9bc0; font-family: Inter, sans-serif;">{active_scope}</span>
</div>
</div>
</div>
""")

    st.sidebar.html("""<div class="sidebar-section-label" style="margin-top: 8px;">Dashboard Filters</div>""")

    with st.sidebar:
        col_time, col_time_btn = st.columns([5, 1])
        with col_time:
            st.html("""<span style="font-size: 12px; font-weight: 600; color: #5a6e94; margin-left: 3px; font-family: Inter, sans-serif;">Time Period</span>""")

        def reset_time_callback():
            if "filter_start" in st.session_state: del st.session_state["filter_start"]
            if "filter_end" in st.session_state: del st.session_state["filter_end"]

        with col_time_btn:
            st.button("↻", key="reset_time", on_click=reset_time_callback, use_container_width=True, help="Reset Time Filter")

        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start Date", value=None, key="filter_start", label_visibility="collapsed")
        with col_end:
            end_date = st.date_input("End Date", value=None, key="filter_end", label_visibility="collapsed")

        st.html("<div style='height: 10px'></div>")

        col_prod, col_prod_btn = st.columns([5, 1])
        with col_prod:
            st.html("""<span style="font-size: 12px; font-weight: 600; color: #5a6e94; margin-left: 3px; font-family: Inter, sans-serif;">Product Type</span>""")

        def reset_prod_callback():
            st.session_state["filter_product"] = "All Products"

        with col_prod_btn:
            st.button("↻", key="reset_prod", on_click=reset_prod_callback, use_container_width=True, help="Reset Product Filter")

        product_filter_str = st.selectbox("Product", ["All Products", "DS", "DA", "BA", "FSD"], key="filter_product", label_visibility="collapsed")
        product_filter = None if product_filter_str == "All Products" else product_filter_str

        def clear_all_filters_callback():
            if st.session_state.user["role"] == "super_admin":
                st.session_state["filter_branch"] = "All Branches"
            st.session_state["filter_product"] = "All Products"
            if "filter_start" in st.session_state: del st.session_state["filter_start"]
            if "filter_end" in st.session_state: del st.session_state["filter_end"]

        st.html("<div style='height: 8px'></div>")
        st.button("🗑  Clear All Filters", on_click=clear_all_filters_callback, use_container_width=True, type="secondary")

    st.sidebar.html("""<div class="sidebar-section-label" style="margin-top: 4px;">Session</div>""")
    show_logout()

    # ── MAIN CONTENT ─────────────────────────────────────────────────────────
    display_header(user_context)

    tab_titles = ["📊  Overview", "🗃  Sales", "➕  Add Sale", "💰  Add Payment"]
    if user["role"] == "super_admin":
        tab_titles.append("🔬  Reports")

    tabs = st.tabs(tab_titles, key="main_navigation_tabs")

    with tabs[0]:
        render_overview(user_context, start_date, end_date, product_filter)

    with tabs[1]:
        render_sales_table(user_context, start_date, end_date, product_filter)

    with tabs[2]:
        render_add_sale(user_context)

    with tabs[3]:
        render_add_payment(user_context)

    if user["role"] == "super_admin":
        with tabs[4]:
            render_query_reports()


if __name__ == "__main__":
    main()
