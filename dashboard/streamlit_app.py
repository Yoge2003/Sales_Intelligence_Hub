import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from datetime import date

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


def inject_dashboard_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global App Background */
        .stApp {
            background-color: #f8fafc;
        }

        /* General block padding */
        .block-container {
            padding: 2.5rem 4rem !important;
            max-width: 1400px !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
            box-shadow: 2px 0 10px rgba(0,0,0,0.02);
        }
        
        [data-testid="stSidebarNav"] span {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        [data-testid="stMetric"]:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
            transform: translateY(-4px);
            border-color: #3b82f6;
        }
        [data-testid="stMetricValue"] {
            color: #0f172a;
            font-weight: 800;
            font-size: 28px;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.02em;
        }
        [data-testid="stMetricLabel"] {
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
            font-family: 'Inter', sans-serif;
        }
        
        /* Accent strip to metrics */
        [data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        }

        /* Buttons */
        .stButton > button {
            border-radius: 8px !important;
            border: 1px solid #cbd5e1 !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            transition: all 0.2s ease;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
        }
        .stButton > button:hover {
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1) !important;
        }

        /* Form Submit Buttons */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
            padding: 0.75rem 2rem !important;
            transition: all 0.2s ease !important;
            letter-spacing: 0.025em;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
            transform: translateY(-2px);
        }

        /* Inputs */
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stDateInput input {
            border-radius: 8px !important;
            border: 1px solid #cbd5e1 !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
            padding: 0.6rem 1rem;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
            font-size: 15px;
        }
        
        /* Force dropdown text and options to black */
        .stSelectbox div[data-baseweb="select"] div, div[data-baseweb="popover"] ul li {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        
        .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus, .stNumberInput input:focus, .stDateInput input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* Tabs Styling */
        [data-testid="stTabs"] button {
            border-radius: 8px 8px 0 0;
            padding-bottom: 1rem;
            padding-top: 1rem;
            font-weight: 600;
            color: #64748b;
            font-family: 'Inter', sans-serif;
            font-size: 15px;
        }
        [data-testid="stTabs"] button[aria-selected="true"] {
            border-bottom: 3px solid #3b82f6 !important;
            color: #2563eb !important;
        }
        
        /* Data Editor background */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            background: white;
        }

        /* Headings and generic text */
        h1, h2, h3, h4, h5, h6, label, p, span, div {
            font-family: 'Inter', sans-serif !important;
            color: #000000 !important;
        }
        h3 {
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Chart backgrounds */
        .js-plotly-plot {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""


def format_currency(value):
    return f"₹ {value:,.2f}" if value is not None else "₹ 0.00"


def show_login():
    css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Hide sidebar and top header completely for login page */
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { display: none; }

/* App Background */
.stApp {
    background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Position container to center */
.block-container {
    padding: 0 !important;
    max-width: 1000px !important;
    margin-top: 8vh !important;
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.5) inset !important;
    border-radius: 20px !important;
    overflow: hidden !important;
}

/* Column padding */
[data-testid="stColumn"]:nth-of-type(1), [data-testid="column"]:nth-of-type(1) {
    padding: 4.5rem 5rem !important;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
[data-testid="stColumn"]:nth-of-type(2), [data-testid="column"]:nth-of-type(2) {
    padding: 0 !important;
}

/* Remove default stForm styling */
[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: auto;
}

/* Typography */
h2.login-text {
    color: #0f172a !important;
    font-weight: 800;
    margin-bottom: 2.5rem !important;
    font-family: 'Inter', sans-serif;
    font-size: 34px !important;
    letter-spacing: -0.025em;
}

/* Input boxes */
[data-testid="stTextInput"] div div input {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
    padding: 14px 16px !important;
    box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02) !important;
    font-size: 15px;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s ease;
}

[data-testid="stTextInput"] div div {
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] div div:focus-within input {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    background-color: #ffffff !important;
}

/* Submit Button */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    border-radius: 10px !important;
    width: 100% !important;
    padding: 0.9rem 1rem !important;
    border: none !important;
    margin-top: 2rem !important;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3), 0 2px 4px -1px rgba(37, 99, 235, 0.15) !important;
}

[data-testid="stFormSubmitButton"] button p {
    color: white !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 0.03em;
    font-family: 'Inter', sans-serif;
}

[data-testid="stFormSubmitButton"] button:hover {
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4), 0 4px 6px -2px rgba(37, 99, 235, 0.2) !important;
    transform: translateY(-2px);
}

/* Placeholder text */
::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important; 
}

/* Reset Markdown p color */
[data-testid="stMarkdownContainer"] p {
    color: #64748b;
    font-size: 14px;
    font-family: 'Inter', sans-serif;
}
</style>
"""
    st.markdown(css_code, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        with st.form("login_form"):
            st.markdown("<h2 class='login-text'>Login</h2>", unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Email or UserName", key="login_username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", key="login_password", label_visibility="collapsed")
            
            forgot_pwd_html = "<div style='text-align: right; margin-top: -12px; margin-bottom: 5px;'><a href='#' style='color: #3b82f6; font-size: 13px; text-decoration: none; font-weight: 500;'>Forgot Password?</a></div>"
            st.markdown(forgot_pwd_html, unsafe_allow_html=True)
            
            st.checkbox("Remember me", key="login_remember")

            submitted = st.form_submit_button("LOGIN", use_container_width=True)
            
            signup_html = "<div style='text-align: center; margin-top: 25px; font-size: 14px; color: #64748b;'>New Member? <a href='#' style='color: #3b82f6; text-decoration: none; font-weight: 600;'>Sign up Now</a></div>"
            st.markdown(signup_html, unsafe_allow_html=True)

            if submitted:
                user = check_login(username.strip(), password.strip())
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.status_message = "Welcome back!"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
    with col2:
        right_panel_html = '<div style="position: relative; height: 100%; min-height: 600px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); overflow: hidden;"><div style="position: absolute; right: -15%; top: -15%; width: 60vw; height: 60vw; background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%); border-radius: 50%;"></div><div style="position: absolute; left: -10%; bottom: -10%; width: 40vw; height: 40vw; background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%); border-radius: 50%;"></div><div style="position: relative; z-index: 10; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.2); padding: 50px 40px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); border-radius: 20px; width: 80%; text-align: center;"><svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 25px; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1));"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg><h3 style="color: white; margin: 0 0 15px 0; font-family: \'Inter\', sans-serif; font-size: 28px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.2;">Sales Intelligence Hub</h3><p style="color: rgba(255,255,255,0.9); font-size: 15px; line-height: 1.6; margin: 0; font-weight: 400;">Transforming data into actionable insights with smarter business tracking and centralized management.</p></div><div style="position: absolute; bottom: 40px; z-index: 10; display: flex; gap: 10px;"><div style="width: 32px; height: 6px; background: white; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div><div style="width: 32px; height: 6px; background: rgba(255,255,255,0.3); border-radius: 3px;"></div></div></div>'
        st.markdown(right_panel_html, unsafe_allow_html=True)


def show_logout():
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 Secure Logout", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()


def display_header(user):
    st.markdown(f"""
    <div style='background: white; padding: 30px 40px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03); margin-bottom: 35px; border-left: 6px solid #3b82f6; display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='margin:0 0 8px 0; font-size: 32px; color: #0f172a; font-weight: 800; letter-spacing: -0.03em; font-family: "Inter", sans-serif;'>Sales Intelligence Hub</h1>
            <p style='margin: 0; color: #64748b; font-size: 16px; font-weight: 400; font-family: "Inter", sans-serif;'>Smarter sales monitoring for branches and payments system</p>
        </div>
        <div style='background: #f0fdf4; color: #166534; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 14px; border: 1px solid #bbf7d0; font-family: "Inter", sans-serif;'>
            <span style='display:inline-block; width:8px; height:8px; background:#22c55e; border-radius:50%; margin-right:6px;'></span> System Active
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1.5])

    with col1:
        st.metric("User Profile", f"{user['username']}")
    with col2:
        display_role = st.session_state.user['role']
        st.metric("System Role", f"{display_role.replace('_', ' ').title()}")
    with col3:
        if user["role"] == "super_admin":
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


def apply_chart_style(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        font_color="#0f172a",
        margin=dict(l=80, r=20, t=50, b=100),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter",
            bordercolor="#e2e8f0"
        )
    )
    fig.update_yaxes(
        title_standoff=25,
        showgrid=True, 
        gridcolor="#f1f5f9", 
        zeroline=False
    )
    fig.update_xaxes(
        showgrid=False, 
        zeroline=False, 
        tickangle=-45,
        categoryorder="category ascending"
    )
    return fig


def render_overview(user, start_date=None, end_date=None, product_filter=None):
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
            <div style='width: 4px; height: 24px; background: #3b82f6; border-radius: 2px;'></div>
            <h3 style='margin: 0;'>Executive Summary</h3>
        </div>
    """, unsafe_allow_html=True)

    total_sales, total_received, total_pending, sale_count = get_kpis(user, start_date, end_date, product_filter)
    
    # Advanced KPIs
    collection_rate = (total_received / total_sales * 100) if total_sales > 0 else 0
    aov = (total_sales / sale_count) if sale_count > 0 else 0

    metric_cols = st.columns(5)
    metric_cols[0].metric("Total Sales", format_currency(total_sales))
    metric_cols[1].metric("Total Received", format_currency(total_received))
    metric_cols[2].metric("Total Pending", format_currency(total_pending), delta=f"-{format_currency(total_pending)}", delta_color="inverse")
    metric_cols[3].metric("Collection Rate", f"{collection_rate:.1f}%")
    metric_cols[4].metric("Avg Order Value", format_currency(aov))

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Dashboard Body
    main_col, activity_col = st.columns([2.5, 1])

    with main_col:
        # 1. Sales Trend Area Chart
        st.markdown("#### 📈 Sales Revenue Trend")
        df_trend = get_sales_trend(user, start_date, end_date, product_filter)
        if not df_trend.empty:
            fig_trend = px.area(
                df_trend, 
                x="sale_date", 
                y="daily_sales",
                color_discrete_sequence=["#3b82f6"],
                labels={"sale_date": "Date", "daily_sales": "Revenue (₹)"}
            )
            fig_trend.update_traces(
                line_width=3, 
                fillcolor="rgba(59, 130, 246, 0.1)",
                hovertemplate="<b>Date:</b> %{x}<br><b>Revenue:</b> ₹%{y:,.2f}<extra></extra>"
            )
            apply_chart_style(fig_trend)
            fig_trend.update_xaxes(type='category')
            st.plotly_chart(fig_trend, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No trend data available for this range.")

    with activity_col:
        st.markdown("#### ⚡ Recent Activity")
        df_activity = get_recent_activity(user)
        if not df_activity.empty:
            for _, row in df_activity.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div style='background: white; padding: 12px; border-radius: 8px; border: 1px solid #f1f5f9; margin-bottom: 10px; border-left: 3px solid #3b82f6;'>
                            <div style='font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase;'>{row['date']}</div>
                            <div style='font-size: 14px; font-weight: 700; color: #0f172a; margin: 2px 0;'>{row['customer']}</div>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='font-size: 12px; color: #3b82f6; font-weight: 600;'>{row['product']}</span>
                                <span style='font-size: 13px; font-weight: 700; color: #10b981;'>₹{row['gross_sales']:,.0f}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No recent activity.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Key Performance Breakdowns
    chart_cols = st.columns(3)
    
    with chart_cols[0]:
        if user["role"] == "super_admin":
            st.markdown("#### 🏢 Sales by Branch")
            df_branch = get_branch_sales(user, start_date, end_date, product_filter)
            if not df_branch.empty:
                fig_branch = px.bar(
                    df_branch, 
                    x="branch_name", 
                    y="total_sales",
                    color="total_sales",
                    color_continuous_scale=["#93c5fd", "#3b82f6"],
                    labels={"branch_name": "Branch", "total_sales": "Sales"}
                )
                apply_chart_style(fig_branch)
                fig_branch.update_coloraxes(showscale=False)
                fig_branch.update_traces(
                    marker_line_width=0, 
                    marker_pattern_shape="",
                    hovertemplate="<b>%{x}</b><br>Sales: ₹%{y:,.2f}<extra></extra>"
                )
                st.plotly_chart(fig_branch, use_container_width=True, theme=None, config={'displayModeBar': False})
            else:
                st.info("No branch sales data.")
        else:
            st.markdown("#### 📈 Sales Status Analysis")
            df_status = get_status_analysis(user, start_date, end_date, product_filter)
            if not df_status.empty:
                fig_status = px.pie(
                    df_status, 
                    names="status", 
                    values="total_value",
                    hole=0.7,
                    color="status",
                    color_discrete_map={"Open": "#f59e0b", "Close": "#10b981"},
                    labels={"status": "Status", "total_value": "Revenue"}
                )
                apply_chart_style(fig_status)
                fig_status.update_traces(
                    textposition='inside', 
                    textinfo='percent',
                    marker=dict(line=dict(color='#FFFFFF', width=2)),
                    hovertemplate="<b>%{label}</b><br>Value: ₹%{value:,.2f}<br>Count: %{customdata[0]}<extra></extra>",
                    customdata=df_status[['count']]
                )
                st.plotly_chart(fig_status, use_container_width=True, theme=None, config={'displayModeBar': False})
            else:
                st.info("No status data.")

    with chart_cols[1]:
        st.markdown("#### 📦 Product Mix")
        df_prod = get_product_performance(user, start_date, end_date, product_filter)
        if not df_prod.empty:
            fig_prod = px.pie(
                df_prod, 
                names="product_name", 
                values="total_sales",
                hole=0.7,
                color_discrete_sequence=["#3b82f6", "#8b5cf6", "#6366f1", "#06b6d4"]
            )
            apply_chart_style(fig_prod)
            fig_prod.update_traces(
                textposition='inside', 
                textinfo='percent',
                marker=dict(line=dict(color='#FFFFFF', width=2)),
                hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.2f}<br>Percentage: %{percent}<extra></extra>"
            )
            st.plotly_chart(fig_prod, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No product data for this range.")

    with chart_cols[2]:
        st.markdown("#### 💳 Payment Channels")
        df_payment = get_payment_analysis(user, start_date, end_date, product_filter)
        if not df_payment.empty:
            fig_payment = px.pie(
                df_payment, 
                names="payment_method", 
                values="total", 
                hole=0.7,
                color_discrete_sequence=["#10b981", "#f59e0b", "#64748b", "#f43f5e"]
            )
            apply_chart_style(fig_payment)
            fig_payment.update_traces(
                textposition='inside', 
                textinfo='percent',
                marker=dict(line=dict(color='#FFFFFF', width=2)),
                hovertemplate="<b>%{label}</b><br>Volume: ₹%{value:,.2f}<br>Percentage: %{percent}<extra></extra>"
            )
            st.plotly_chart(fig_payment, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No payment data for this range.")


def render_sales_table(user, start_date=None, end_date=None, product_filter=None):
    st.subheader("Sales Records Management")
    st.info("Double-click any cell to edit. Select a row and press delete to remove it. Changes save automatically!")
    
    df = get_sales(user, start_date, end_date, product_filter)
    if df.empty:
        st.info("No sales records found.")
        return
        
    # Set index to sale_id so we can reference it securely when editing
    df = df.set_index("sale_id")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="sales_data_editor"
    )

    # Export Buttons
    col_csv, col_excel, col_json, col_pdf = st.columns(4)
    
    # 1. CSV
    csv = df.to_csv(index=True).encode('utf-8')
    col_csv.download_button(
        label="📥 CSV",
        data=csv,
        file_name='sales_records.csv',
        mime='text/csv',
        type="secondary",
        use_container_width=True
    )
    
    # 2. Excel
    import io
    excel_buffer = io.BytesIO()
    with __import__('pandas').ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=True)
    col_excel.download_button(
        label="📥 Excel",
        data=excel_buffer.getvalue(),
        file_name='sales_records.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        type="secondary",
        use_container_width=True
    )
    
    # 3. JSON
    json_data = df.reset_index().to_json(orient="records").encode('utf-8')
    col_json.download_button(
        label="📥 JSON",
        data=json_data,
        file_name='sales_records.json',
        mime='application/json',
        type="secondary",
        use_container_width=True
    )
    
    # 4. PDF
    from fpdf import FPDF
    def generate_pdf(dataframe):
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        
        # Add Title
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
                # Need to encode correctly or ignore errors if non-latin names
                val = str(row[col]).encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(col_width, 6, val[:20], border=1, align="C")
            pdf.ln()
            
        return bytes(pdf.output())

    col_pdf.download_button(
        label="📥 PDF",
        data=generate_pdf(df),
        file_name='sales_records.pdf',
        mime='application/pdf',
        type="secondary",
        use_container_width=True
    )

    # Detect modifications
    changes = st.session_state.get("sales_data_editor")
    if changes:
        has_changed = False
        
        # Handle edits
        for row_idx, updates in changes.get("edited_rows", {}).items():
            sale_id = int(df.index[row_idx])
            update_sale(sale_id, updates)
            has_changed = True
            
        # Handle deletions
        for row_idx in changes.get("deleted_rows", []):
            sale_id = int(df.index[row_idx])
            delete_sale(sale_id)
            has_changed = True
            
        if has_changed:
            st.success("Database updated successfully!")
            st.rerun()


def render_add_payment(user):
    st.subheader("Add Additional Payment")
    st.info("Search for an existing sale by ID to record a new payment.")

    search_id = st.number_input("Enter Sale ID to Search", min_value=1, step=1, key="payment_search_id")
    
    if search_id:
        df = get_sale_by_id(search_id, user)
        if df.empty:
            st.warning(f"No active sale found with ID {search_id} in your accessible branch.")
        else:
            sale = df.iloc[0]
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Customer:** {sale['name']}")
                st.write(f"**Product:** {sale['product_name']}")
                st.write(f"**Status:** {sale['status']}")
            with c2:
                st.write(f"**Gross Sales:** {format_currency(sale['gross_sales'])}")
                st.write(f"**Total Received:** {format_currency(sale['received_amount'])}")
                st.write(f"**Pending Amount:** :red[{format_currency(sale['pending_amount'])}]")

            if sale['status'] == 'Close':
                st.error("🔒 This sale is already CLOSED. No further payments can be recorded.")
            else:
                with st.form("payment_form"):
                    pay_date = st.date_input("Payment Date", value=date.today())
                    pay_amount = st.number_input("Payment Amount", min_value=0.0, max_value=float(sale['pending_amount']), format="%.2f")
                    pay_method = st.selectbox("Payment Method", ["Cash", "UPI", "Bank Transfer", "Card"])
                    
                    if st.form_submit_button("Record Payment"):
                        if pay_amount <= 0:
                            st.error("Please enter a valid payment amount.")
                        else:
                            record_payment(search_id, pay_amount, pay_method, pay_date)
                            st.success(f"Successfully recorded payment of {format_currency(pay_amount)} for Sale ID {search_id}")
                            st.rerun()

def render_add_sale(user):
    st.subheader("Add New Sale")
    st.info("Create a new sale record. You can record the initial down payment here.")

    branch_id = user["branch_id"]
    if user["role"] == "super_admin":
        branches = get_branch_list()
        options = [f"{branch['branch_id']} - {branch['branch_name']}" for branch in branches]
        selected = st.selectbox("Select Branch", options)
        branch_id = int(selected.split(" - ")[0]) if selected else branch_id

    with st.form("sale_form"):
        sale_date = st.date_input("Sale Date", value=date.today(), help="Select the date of the sale")
        customer_name = st.text_input("Customer Name", placeholder="Enter the customer's full name", help="Enter the name of the purchasing customer")
        mobile_number = st.text_input("Mobile Number", placeholder="Enter 10-digit mobile number", help="Enter the customer's contact number")
        product_name = st.selectbox("Product", ["DS", "DA", "BA", "FSD"], help="Select the product purchased")
        
        col_amt, col_pay = st.columns(2)
        with col_amt:
            gross_amt = st.number_input("Total Sale Amount", min_value=0.0, format="%.2f", help="The full price of the product")
            received_amt = st.number_input("Initial Amount Received", min_value=0.0, format="%.2f", help="Check if the customer paid anything upfront")
        with col_pay:
            pay_method = st.selectbox("Initial Payment Method", ["N/A", "Cash", "UPI", "Bank Transfer", "Card"])
        
        submitted = st.form_submit_button("Create Sale Record")

        if submitted:
            if not customer_name or not mobile_number or gross_amt <= 0:
                st.error("Please provide Customer Name and a valid Sale Amount.")
            elif received_amt > gross_amt:
                st.error("Received amount cannot exceed the total sale amount.")
            else:
                new_id = add_sale(branch_id, sale_date, customer_name, mobile_number, product_name, gross_amt, received_amt, pay_method)
                st.success(f"🎊 Sale record created successfully! Assigned Sale ID: {new_id}")
                st.rerun()


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
    st.subheader("Predefined SQL Queries")
    st.info("Select a predefined analytical report from the database to generate custom exports.")
    
    reports_file = os.path.join(os.path.dirname(__file__), '..', 'reports', 'sql_queries.sql')
    queries = parse_sql_queries(reports_file)
    
    if not queries:
        st.warning("Could not find any SQL queries in reports/sql_queries.sql")
        return
        
    selected_report = st.selectbox("Select Report to Generate", list(queries.keys()))
    
    if selected_report:
        sql = queries[selected_report]
        st.markdown("**Query Logic:**")
        st.code(sql, language="sql")
        
        if st.button("Execute Query", type="primary"):
            with st.spinner("Processing report..."):
                df = execute_custom_query(sql)
                if 'Error' in df.columns and len(df) == 1:
                    st.error(f"Execution Error: {df.iloc[0]['Error']}")
                else:
                    st.success(f"Report Generated! Found {len(df)} rows.")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Data as CSV",
                        data=csv,
                        file_name=f"{selected_report.replace(' ', '_').lower()}.csv",
                        mime="text/csv",
                    )


def main():
    init_page()
    init_session_state()

    if not st.session_state.logged_in:
        show_login()
        st.stop()

    inject_dashboard_css()
    
    user = st.session_state.user
    user_context = dict(user)
    
    # Dynamically determine the active scope for display
    if user["role"] == "super_admin":
        col_bf_l, col_bf_r = st.sidebar.columns([5, 1])
        with col_bf_l:
            st.markdown("<h4 style='color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0px; padding-left: 5px; margin-top: 5px;'>Branch Filter</h4>", unsafe_allow_html=True)
            
        branches = get_branch_list()
        options = ["All Branches"] + [f"{branch['branch_id']} - {branch['branch_name']}" for branch in branches]
        
        with col_bf_r:
            if st.button("↻", key="reset_branch", use_container_width=True, help="Reset Branch Filter"):
                st.session_state["filter_branch"] = options[0]
                st.rerun()
                
        selected_branch = st.sidebar.selectbox("Select Branch", options, label_visibility="collapsed", key="filter_branch")
        
        if selected_branch != "All Branches":
            branch_id_selected = int(selected_branch.split(" - ")[0])
            branch_name_selected = selected_branch.split(" - ")[1]
            user_context["role"] = "admin"
            user_context["branch_id"] = branch_id_selected
            user_context["branch_name"] = branch_name_selected
            active_scope = branch_name_selected
        else:
            active_scope = "All Branches"
    else:
        active_scope = user.get("branch_name")
        if not active_scope:
            branches = get_branch_list()
            found_name = next((b["branch_name"] for b in branches if b["branch_id"] == user["branch_id"]), None)
            active_scope = found_name if found_name else f"Branch {user.get('branch_id')}"
            user_context["branch_name"] = active_scope

    sidebar_html = f"""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 25px 20px; border-radius: 12px; color: white; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3), 0 2px 4px -1px rgba(59, 130, 246, 0.15);">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
            <div style="width: 45px; height: 45px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 800; border: 2px solid rgba(255,255,255,0.5); text-transform: uppercase;">
                {user["username"][0]}
            </div>
            <div>
                <p style="margin: 0; font-size: 11px; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Welcome back</p>
                <h3 style="margin: 0; font-size: 16px; font-weight: 700; letter-spacing: -0.02em; color: white;">{user["username"]}</h3>
            </div>
        </div>
        <div style="background: rgba(0,0,0,0.15); padding: 12px 15px; border-radius: 8px; font-size: 13px; font-weight: 500; border: 1px solid rgba(255,255,255,0.1);">
            <div style="margin-bottom: 8px;">
                <span style="opacity: 0.7; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 2px;">Role</span>
                <span style="font-weight: 600;">{user["role"].replace('_', ' ').title()}</span>
            </div>
            <div>
                <span style="opacity: 0.7; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 2px;">Access Scope</span>
                <span style="font-weight: 600;">{active_scope}</span>
            </div>
        </div>
    </div>
    """
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
    
    st.sidebar.markdown("<h4 style='color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; padding-left: 5px;'>Dashboard Filters</h4>", unsafe_allow_html=True)
    with st.sidebar:
        col_time, col_time_btn = st.columns([5, 1])
        with col_time:
            st.markdown("<span style='font-size: 13px; font-weight: 600; color: #334155; margin-left: 5px;'>Time Period</span>", unsafe_allow_html=True)
        with col_time_btn:
            if st.button("↻", key="reset_time", use_container_width=True, help="Reset Time Filter"):
                if "filter_start" in st.session_state: del st.session_state["filter_start"]
                if "filter_end" in st.session_state: del st.session_state["filter_end"]
                st.rerun()
                
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start Date", value=None, key="filter_start", label_visibility="collapsed")
        with col_end:
            end_date = st.date_input("End Date", value=None, key="filter_end", label_visibility="collapsed")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_prod, col_prod_btn = st.columns([5, 1])
        with col_prod:
            st.markdown("<span style='font-size: 13px; font-weight: 600; color: #334155; margin-left: 5px;'>Product Type</span>", unsafe_allow_html=True)
        with col_prod_btn:
            if st.button("↻", key="reset_prod", use_container_width=True, help="Reset Product Filter"):
                st.session_state["filter_product"] = "All Products"
                st.rerun()
                
        product_filter_str = st.selectbox("Product", ["All Products", "DS", "DA", "BA", "FSD"], key="filter_product", label_visibility="collapsed")
        product_filter = None if product_filter_str == "All Products" else product_filter_str

    st.sidebar.markdown("<h4 style='color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-top: 20px; margin-bottom: 10px; padding-left: 5px;'>Actions & Settings</h4>", unsafe_allow_html=True)
    show_logout()

    display_header(user_context)

    tab_titles = ["Overview", "Sales", "Add Sale", "Add Payment"]
    if user["role"] == "super_admin":
        tab_titles.append("Query Reports")

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
