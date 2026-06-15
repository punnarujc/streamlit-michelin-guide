import streamlit as st

# Set global page configuration
st.set_page_config(
    page_title="Michelin Guide Globe",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define pages relative to this entrypoint script (app/app.py)
map_page = st.Page("map.py", title="Michelin Guide Map", default=True)
michelin_guide_page = st.Page("michelin_guide.py", title="Michelin Guide")
#


# Setup navigation structure
pg = st.navigation([map_page, michelin_guide_page])
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
</style>
""", unsafe_allow_html=True)

# Run the navigation router
pg.run()

# Additional sidebar components rendered after page load
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
