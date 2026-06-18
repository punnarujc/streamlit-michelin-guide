import os
import sys
import streamlit as st

# Add project root to sys.path to allow importing from the 'app' package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)



# Set global page configuration
st.set_page_config(
    page_title="Michelin Guide Globe",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define pages relative to this entrypoint script (app/app.py)
michelin_guide_page = st.Page("michelin_guide.py", title="Michelin Guide")
trip_planner_page = st.Page("trip_planner.py", title="Trip Planner")
ai_assistant_page = st.Page("ai_assistant.py", title="AI Assistant")


# Setup navigation structure
pg = st.navigation([michelin_guide_page, trip_planner_page, ai_assistant_page])
# Inject premium custom CSS for the sidebar and header
st.sidebar.markdown("""
<style>
header, [data-testid="stHeader"], .stAppHeader {
    background-color: #050505 !important;
    background: #050505 !important;
    border-bottom: 1px solid #101010 !important;
}
header *, [data-testid="stHeader"] *, .stAppHeader * {
    color: #ffffff !important;
}
header svg, [data-testid="stHeader"] svg, .stAppHeader svg {
    fill: #ffffff !important;
}

/* Sidebar container background & border */
[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid #1a1a1a !important;
}

/* Sidebar navigation container background override */
[data-testid="stSidebarNav"] {
    background-color: transparent !important;
    padding-top: 10px !important;
}

/* Sidebar navigation links */
[data-testid="stSidebarNav"] ul li a {
    background-color: transparent !important;
    color: #cccccc !important;
    font-size: 12px !important;
    font-weight: 100 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    padding: 12px 16px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    margin-bottom: 4px !important;
}

/* Hover state on navigation link */
[data-testid="stSidebarNav"] ul li a:hover {
    background-color: #161616 !important;
    color: #D4AF37 !important;
}

/* Active navigation link */
[data-testid="stSidebarNav"] ul li a[aria-current="page"] {
    background-color: #BD1B21 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(189, 27, 33, 0.4) !important;
}

/* Sidebar markdown text styling */
[data-testid="stSidebar"] .element-container p,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #888888 !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
}

/* Custom separator line */
[data-testid="stSidebar"] hr {
    border-color: #1a1a1a !important;
    margin: 20px 0 !important;
}

/* About Section Title */
.sidebar-section-title {
    color: #ffffff !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    margin-top: 15px;
    margin-bottom: 8px;
}

/* Luxury border button styling */
.sidebar-btn {
    display: block;
    width: 100%;
    text-align: center;
    background-color: #000000 !important; /* black background */
    color: #ff0000 !important;           /* red text */
    border: 1px solid #ff0000 !important;/* red border */
    border-radius: 6px !important;
    padding: 8px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
    margin-top: 15px;
}
.sidebar-btn:hover {
    background-color: #000000 !important; /* black hover */
    color: #ff0000 !important;           /* red text */
    border-color: #ff0000 !important;
    box-shadow: 0 0 10px rgba(255,0,0,0.3) !important; /* subtle red glow */
}

/* Sidebar bold white text for data updated */
.sidebar-data-updated,
.sidebar-data-updated * {
    color: #ffffff !important;
    font-weight: thin !important;
}
.sidebar-footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px;
    color: #fafafa !important;
}

/* Ensure all text inside the footer is white */
.sidebar-footer p,
.sidebar-footer span,
.sidebar-footer div {
    color: #ffffff !important;
}

/* Sidebar Database Status CSS */
[data-testid="stSidebar"] > div:first-child {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}
/* Make the inner wrapper a flex container to allow pushing items to the bottom */
[data-testid="stSidebarUserContent"] {
    overflow-y: auto;
    overflow-x: hidden;
    flex: 1;
    padding-bottom: 1rem;
}
[data-testid="stSidebarUserContent"] > div {
    display: flex;
    flex-direction: column;
    height: 100%;
}
/* Push the db-divider and everything after it to the bottom */
.element-container:has(.db-divider) {
    margin-top: auto !important;
}
.db-status-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 15px;
    margin-bottom: 25px;
    width: 100%;
}
.db-status-card {
    background-color: #0c0c0c;
    border: 1px solid rgba(212, 175, 55, 0.15);
    border-radius: 10px;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    font-family: inherit !important;
}
.db-status-card:hover {
    border-color: rgba(212, 175, 55, 0.35) !important;
    box-shadow: 0 4px 16px rgba(212, 175, 55, 0.1);
}
.db-status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.db-status-name {
    font-family: inherit !important;
    font-size: 13px;
    color: #ffffff;
    font-weight: 500;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
}
.db-status-badge {
    font-family: inherit !important;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    line-height: 1.2;
}
.badge-success {
    background-color: rgba(76, 175, 80, 0.1) !important;
    color: #4CAF50 !important;
    border: 1px solid rgba(76, 175, 80, 0.3) !important;
}
.badge-failed {
    background-color: rgba(189, 27, 33, 0.1) !important;
    color: #FF4F55 !important;
    border: 1px solid rgba(189, 27, 33, 0.3) !important;
}
.badge-idle {
    background-color: rgba(136, 136, 136, 0.1) !important;
    color: #888888 !important;
    border: 1px solid rgba(136, 136, 136, 0.2) !important;
}
.db-status-info {
    font-size: 12px;
    color: #cccccc;
    margin-top: 2px;
    font-family: inherit !important;
}
.db-status-error {
    font-size: 10px;
    color: #FF8A8F;
    margin-top: 6px;
    line-height: 1.3;
    font-style: italic;
    background-color: rgba(0, 0, 0, 0.3);
    padding: 6px;
    border-radius: 4px;
    border-left: 2px solid #BD1B21;
    max-height: 70px;
    overflow-y: auto;
    font-family: monospace;
    white-space: pre-wrap;
    word-break: break-all;
}
</style>
""", unsafe_allow_html=True)

# Show database warning banner if in mock mode
if st.session_state.get("using_mock_data", False):
    st.sidebar.markdown(
        f"<div style='border: 1px solid rgba(255, 170, 0, 0.3); border-radius: 8px; padding: 12px; background-color: rgba(255, 170, 0, 0.05); margin: 10px 0 20px 0;'>"
        f"<div style='font-size: 11px; font-weight: 700; color: #FFaa00; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;'>⚠️ Fallback Active</div>"
        f"<div style='font-size: 11px; color: #cccccc; line-height: 1.4; margin-bottom: 8px;'>Using fallback data. "
        f"{st.session_state.get('db_error_message', '')}</div>"
        f"<div style='font-size: 10px; color: #888888; font-style: italic;'>Please configure your database credentials in <code>.streamlit/secrets.toml</code> and restart the application.</div>"
        f"</div>",
        unsafe_allow_html=True
    )

# Additional sidebar components rendered before page load so they appear immediately
st.sidebar.markdown("<div class='sidebar-section-title'>About</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "This is an interactive 2D map visualizing the **Michelin Guide Restaurants 2021** dataset from Kaggle. "
    "Built with **Streamlit**, **DuckDB**, and **Plotly**."
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div class="sidebar-data-updated">
    <div style="font-size: 11px; font-weight: 300; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px;">Data Updated</div>
    <div style="font-size: 11px; font-weight: 100;">June 2026</div>
</div>
""", unsafe_allow_html=True)

# Database Integration sidebar section
st.sidebar.markdown("<hr class='db-divider' style='margin: 15px 0;' />", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-section-title db-section-title'>Database Integration</div>", unsafe_allow_html=True)

# Create placeholders for real-time status updates
db_status_container = st.sidebar.empty()
st.session_state.db_status_container = db_status_container

db_warning_container = st.sidebar.empty()
st.session_state.db_warning_container = db_warning_container

# Initial render of the database status (reads from st.session_state or defaults to idle).
# On a cold start, Streamlit's first script run can race the import machinery and leave the
# `data` module partially initialized, so retry the import once before giving up.
try:
    from data import update_db_status_ui
except ImportError:
    # Drop any partially-initialized module left by the race, then re-import cleanly.
    sys.modules.pop("data", None)
    from data import update_db_status_ui
update_db_status_ui()

# Run the navigation router
pg.run()
