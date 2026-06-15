import streamlit as st
import pandas as pd
import plotly.express as px

from data import load_kaggle_data, get_restaurants
# ===== LUXURY THEME ADDITION =====
st.set_page_config(
    page_title="Michelin Luxury Guide",
    page_icon="⭐",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background:#050505;
}
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
.block-container{
    max-width:1500px;
}
.metric-card{
    background:#0F0F0F;
    border:1px solid #2A2A2A;
    border-radius:16px;
    padding:20px;
    text-align:center;
}
.metric-number{
    font-size:42px;
    color:#D4AF37;
    font-weight:bold;
}
.metric-label{
    color:white;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)
# ===== END THEME =====


import streamlit as st
import plotly.express as px
import pandas as pd
import urllib.request
import re
from data import load_kaggle_data, get_restaurants, get_unique_awards


if 'country_filter' not in st.session_state:
    st.session_state.country_filter = []
if 'city_filter' not in st.session_state:
    st.session_state.city_filter = []
if 'district_filter' not in st.session_state:
    st.session_state.district_filter = []
if 'award_filter' not in st.session_state:
    st.session_state.award_filter = []
if 'price_filter' not in st.session_state:
    st.session_state.price_filter = []
if 'name_filter' not in st.session_state:
    st.session_state.name_filter = []
def clear_filters():
    st.session_state.country_filter = []
    st.session_state.city_filter = []
    st.session_state.district_filter = []
    st.session_state.award_filter = []
    st.session_state.price_filter = []
    st.session_state.name_filter = []

@st.cache_data(show_spinner=False)
def fetch_michelin_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

# --------------------
# HERO & STYLES
# --------------------
st.markdown("""
<style>
.michelin-hero {
    position: relative;
    padding: 60px 50px;
    border-radius: 20px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0.92) 35%, rgba(0, 0, 0, 0.05) 80%), url('https://images.unsplash.com/photo-1611520175743-30ff00129621?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
    background-size: auto 150% !important;
    background-repeat: no-repeat !important;
    background-position: right center !important;
    color: white;
    margin-bottom: 35px;
    min-height: 480px;
    display: flex;
    align-items: center;
    overflow: hidden;
    border: 1px solid #1a1a1a;
}
.michelin-hero-content {
    position: relative;
    z-index: 2;
    max-width: 600px;
}
.michelin-hero-meta {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #ffffff;
    margin-bottom: 25px;
    text-transform: uppercase;
}
.michelin-hero-brand {
    margin-bottom: 15px;
}
.brand-michelin {
    font-family: 'Georgia', serif !important;
    font-size: 72px !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    line-height: 1.0 !important;
    color: #ffffff !important;
    margin: 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.brand-guide {
    font-family: 'Georgia', serif !important;
    font-size: 56px !important;
    font-weight: 400 !important;
    font-style: italic !important;
    letter-spacing: 4px !important;
    line-height: 1.0 !important;
    color: #BD1B21 !important;
    margin: 5px 0 0 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.michelin-hero-stars {
    display: flex;
    align-items: center;
    margin: 20px 0;
}
.stars-gold {
    color: #D4AF37 !important;
    font-size: 20px !important;
    margin: 0 15px;
    letter-spacing: 5px;
}
.star-line {
    flex-grow: 0;
    width: 60px;
    height: 1px;
    background-color: #D4AF37;
}
.michelin-hero-subtitle {
    margin-bottom: 35px;
}
.sub-en {
    font-size: 18px !important;
    color: #cccccc !important;
    margin: 0 0 5px 0 !important;
}
.sub-th {
    font-size: 14px !important;
    color: #888888 !important;
    margin: 0 !important;
    font-weight: 300;
}
.michelin-hero-pills {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}
.hero-pill {
    padding: 8px 16px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    border-radius: 6px;
}
.pill-red {
    background-color: #BD1B21 !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(189, 27, 33, 0.4);
}
.pill-outline {
    background-color: rgba(0, 0, 0, 0.6) !important;
    color: #cccccc !important;
    border: 1px solid #333333 !important;
}
.section-title {
    font-weight: 700;
    color:  #ffffff;
    margin-bottom: 15px;
    margin-top: 15px;
}
.section-title.filter-data{
    color:#ffffff !important;
}
h1, h2, h3, h4, h5, h6{
    color:#ffffff !important;
}
/* Luxury styled multiselect labels */
.stMultiSelect label {
    color: #cccccc !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    margin-bottom: 6px !important;
}

/* Big Filter Box Container Border - Luxury Gold */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 12px !important;
}

/* Multiselect container background & border */
div[data-baseweb="select"] > div {
    background-color: #0c0c0c !important;
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 8px !important;
    box-shadow: 0 0 6px rgba(212, 175, 55, 0.08) !important;
    transition: all 0.3s ease !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: #ffffff !important;
    box-shadow: 0 0 12px rgba(212, 175, 55, 0.45) !important;
}

/* Selected chips/tags */
span[data-baseweb="tag"] {
    background-color: #BD1B21 !important;
    border-radius: 6px !important;
}
span[data-baseweb="tag"] span {
    color: #ffffff !important;
}

/* Dropdown icons */
div[data-baseweb="select"] svg {
    fill: #ffffff !important;
}

/* Text in select input */
div[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* Clear Filters Button Styling */
div.stButton > button {
    background-color: #BD1B21 !important;
    color: #ffffff !important;
    border: 1px solid #991014 !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    background-color: #e60028 !important;
    border-color: #BD1B21 !important;
    box-shadow: 0 4px 15px rgba(189, 27, 33, 0.4) !important;
    color: #ffffff !important;
}
[data-testid="stMetric"] {
    background-color: #BD1B21 !important;
    border: 1px solid #991014 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    text-align: left !important;
}
[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: #ffffff !important;
    justify-content: flex-start !important;
    text-align: left !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    opacity: 1.0 !important;
    margin-bottom: 4px !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    text-align: left !important;
    font-size: 38px !important;
    font-weight: 300 !important;
    line-height: 1.1 !important;
}
[data-testid="stMetric"] div {
    justify-content: flex-start !important;
}
</style>
""", unsafe_allow_html=True)
import base64
import os

st.markdown("""<div class="michelin-hero"><div class="michelin-hero-content"><div class="michelin-hero-meta">THE WORLD'S GREATEST RESTAURANTS <span style="color: #BD1B21;">• 2026 EDITION</span></div><div class="michelin-hero-brand"><h1 class="brand-michelin">MICHELIN</h1><h1 class="brand-guide">GUIDE</h1></div><div class="michelin-hero-stars"><span class="star-line"></span><span class="stars-gold">★ ★ ★</span><span class="star-line"></span></div><div class="michelin-hero-subtitle"><p class="sub-en">Excellence across 40+ countries</p><p class="sub-th">ความเป็นเลิศทางคุณค่าอาหารระดับโลก</p></div><div class="michelin-hero-pills"><div class="hero-pill pill-red">🇹🇭 THAILAND 2026 NEW</div><div class="hero-pill pill-outline">2 THREE-STAR RESTAURANTS</div><div class="hero-pill pill-outline">475 TOTAL SELECTIONS</div></div></div></div>""", unsafe_allow_html=True)

# Load Data
with st.spinner("Loading Michelin Guide Dataset..."):
    load_kaggle_data()
    # Fetch all data by passing all awards
    all_awards = get_unique_awards()
    df = get_restaurants(awards=all_awards)

if df.empty:
    st.error("No data found or failed to load data.")
else:
    # Data preprocessing
    # Split Location into City and Country. Handle cases where there might not be a comma
    location_split = df['Location'].str.split(', ', n=1, expand=True)
    df['City'] = location_split[0]
    df['Country'] = location_split[1].fillna('Unknown')
    
    # Extract District from Address
    def get_district(row):
        parts = [p.strip() for p in str(row['Address']).split(',')]
        try:
            idx = parts.index(row['City'])
            return parts[idx-1] if idx > 0 else 'Unknown'
        except ValueError:
            return 'Unknown'
            
    df['District'] = df.apply(get_district, axis=1)
    
    # Read selections from st.session_state (populated on page load or on rerun)
    selected_countries = st.session_state.get('country_filter', [])
    selected_cities = st.session_state.get('city_filter', [])
    selected_districts = st.session_state.get('district_filter', [])
    selected_awards = st.session_state.get('award_filter', [])
    selected_prices = st.session_state.get('price_filter', [])
    selected_names = st.session_state.get('name_filter', [])

    # Pre-calculate filtered_df based on current selections
    filtered_df = df.copy()
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    if selected_districts:
        filtered_df = filtered_df[filtered_df['District'].isin(selected_districts)]
    if selected_awards:
        filtered_df = filtered_df[filtered_df['Award'].isin(selected_awards)]
    if selected_prices:
        filtered_df = filtered_df[filtered_df['Price'].isin(selected_prices)]
    if selected_names:
        filtered_df = filtered_df[filtered_df['Name'].isin(selected_names)]

    # ------------------
    # Dynamic Metrics (Summary Panel)
    # ------------------
    st.markdown("<h2 class='section-title'> Summary</h2>", unsafe_allow_html=True)
    
    num_restaurants = f"{len(filtered_df):,}"
    num_countries = f"{filtered_df['Country'].nunique():,}" if 'Country' in filtered_df.columns else "0"
    num_cities = f"{filtered_df['City'].nunique():,}" if 'City' in filtered_df.columns else "0"
    num_awards = f"{filtered_df['Award'].nunique():,}" if 'Award' in filtered_df.columns else "0"

    metrics_html = f"""<style>
.luxury-summary-container {{
    display: flex;
    align-items: center;
    justify-content: space-around;
    background-color: #0a0a0a;
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 12px;
    padding: 24px 16px;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}}
.summary-item {{
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    justify-content: center;
}}
.summary-icon-circle {{
    width: 54px;
    height: 54px;
    border-radius: 50%;
    border: 1px solid #4A3B2C;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(20, 20, 20, 0.4);
    flex-shrink: 0;
}}
.summary-text {{
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.summary-value {{
    font-family: 'Georgia', serif;
    font-size: 34px;
    color: #ffffff;
    line-height: 1.1;
    font-weight: 500;
}}
.summary-label {{
    font-family: 'Arial', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #A9927D;
    letter-spacing: 1.5px;
    margin-top: 4px;
    text-transform: uppercase;
}}
.summary-sublabel {{
    font-family: 'Georgia', serif;
    font-size: 11px;
    color: #888888;
    font-style: italic;
    margin-top: 2px;
}}
.summary-divider {{
    width: 1px;
    height: 45px;
    background-color: #1a1a1a;
    flex-shrink: 0;
}}
</style>
<div class="luxury-summary-container">
    <div class="summary-item">
        <div class="summary-icon-circle">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 3.5v5.5a2.5 2.5 0 0 0 5 0v-5.5" stroke="#D4AF37" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8.5 3.5v5.5" stroke="#D4AF37" stroke-width="2.2" stroke-linecap="round"/>
                <path d="M8.5 11.5v9" stroke="#D4AF37" stroke-width="2.2" stroke-linecap="round"/>
                <path d="M16 11v9.5" stroke="#BD1B21" stroke-width="2.2" stroke-linecap="round"/>
                <path d="M16 3.5c-1.8 0 -3.2 1.5 -3.2 3.8s1.4 3.8 3.2 3.8s3.2 -1.5 3.2 -3.8s-1.4 -3.8 -3.2 -3.8z" fill="#BD1B21" stroke="#BD1B21" stroke-width="0.8"/>
            </svg>
        </div>
        <div class="summary-text">
            <div class="summary-value">{num_restaurants}</div>
            <div class="summary-label">RESTAURANTS</div>
            <div class="summary-sublabel">Worldwide</div>
        </div>
    </div>
    <div class="summary-divider"></div>
    <div class="summary-item">
        <div class="summary-icon-circle">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" />
                <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
            </svg>
        </div>
        <div class="summary-text">
            <div class="summary-value">{num_countries}</div>
            <div class="summary-label">COUNTRIES</div>
        </div>
    </div>
    <div class="summary-divider"></div>
    <div class="summary-item">
        <div class="summary-icon-circle">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 21V9a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v12" />
                <path d="M10 21V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v17" />
                <path d="M16 21V12a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v9" />
                <path d="M2 21h20" />
                <path d="M7 11h1M7 15h1M13 7h1M13 11h1M13 15h1M19 15h1" stroke="#D4AF37" stroke-width="1.5" />
            </svg>
        </div>
        <div class="summary-text">
            <div class="summary-value">{num_cities}</div>
            <div class="summary-label">CITIES</div>
        </div>
    </div>
    <div class="summary-divider"></div>
    <div class="summary-item">
        <div class="summary-icon-circle">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3.2" fill="#BD1B21" />
                <path d="M12 12C9.5 10 9.5 6 12 3C14.5 6 14.5 10 12 12Z" fill="#BD1B21" />
                <path d="M12 12C9.5 14 9.5 18 12 21C14.5 18 14.5 14 12 12Z" fill="#BD1B21" />
                <g transform="rotate(60, 12, 12)">
                    <path d="M12 12C9.5 10 9.5 6 12 3C14.5 6 14.5 10 12 12Z" fill="#BD1B21" />
                    <path d="M12 12C9.5 14 9.5 18 12 21C14.5 18 14.5 14 12 12Z" fill="#BD1B21" />
                </g>
                <g transform="rotate(120, 12, 12)">
                    <path d="M12 12C9.5 10 9.5 6 12 3C14.5 6 14.5 10 12 12Z" fill="#BD1B21" />
                    <path d="M12 12C9.5 14 9.5 18 12 21C14.5 18 14.5 14 12 12Z" fill="#BD1B21" />
                </g>
            </svg>
        </div>
        <div class="summary-text">
            <div class="summary-value">{num_awards}</div>
            <div class="summary-label">AWARD</div>
            <div class="summary-sublabel">CATEGORIES</div>
        </div>
    </div>
</div>"""
    st.markdown(metrics_html, unsafe_allow_html=True)

    # ------------------
    # 6. Table Filters
    # ------------------
    st.markdown("<h2 class='section-title filter-data'> Filter Data</h2>", unsafe_allow_html=True)

    # Preset filter buttons removed (moved to interactive hero pills)
    
    with st.container(border=True):
        row1_cols = st.columns(3)
        row2_cols = st.columns(3)
        countries = sorted(df['Country'].dropna().unique().tolist())
        selected_countries = row1_cols[0].multiselect("Country", options=countries, placeholder="Choose countries...", key='country_filter')
            
        # Filter cities based on selected country
        if selected_countries:
            cities = sorted(df[df['Country'].isin(selected_countries)]['City'].dropna().unique().tolist())
        else:
            cities = sorted(df['City'].dropna().unique().tolist())
        
        selected_cities = row1_cols[1].multiselect("City", options=cities, placeholder="Choose cities...", key='city_filter')
        
        # Filter districts based on selected city/country
        temp_df = df.copy()
        if selected_countries: temp_df = temp_df[temp_df['Country'].isin(selected_countries)]
        if selected_cities: temp_df = temp_df[temp_df['City'].isin(selected_cities)]
        districts = sorted(temp_df[temp_df['District'] != 'Unknown']['District'].dropna().unique().tolist())
        
        selected_districts = row1_cols[2].multiselect("District", options=districts, placeholder="Choose districts... (e.g. Sathon)", key='district_filter')
            
        awards = sorted(df['Award'].dropna().unique().tolist())
        selected_awards = row2_cols[0].multiselect("Award", options=awards, placeholder="Choose awards...", key='award_filter')
            
        price_levels = sorted(df['Price'].dropna().unique().tolist())
        selected_prices = row2_cols[1].multiselect("Price", options=price_levels, placeholder="Choose price levels...", key='price_filter')

        # Filter names dynamically based on the above filters to make it easier to search
        temp_df2 = temp_df.copy()
        if selected_districts: temp_df2 = temp_df2[temp_df2['District'].isin(selected_districts)]
        if selected_awards: temp_df2 = temp_df2[temp_df2['Award'].isin(selected_awards)]
        if selected_prices: temp_df2 = temp_df2[temp_df2['Price'].isin(selected_prices)]
        names = sorted(temp_df2['Name'].dropna().unique().tolist())
        
        selected_names = row2_cols[2].multiselect("Name", options=names, placeholder="Search restaurant name...", key='name_filter')

        # Clear filters button
        st.button("Clear All Filters", on_click=clear_filters)

    # ------------------
    # Display Map
    # ------------------
    st.markdown("---")
    
    col_map_title, col_map_btn = st.columns([8, 2])
    with col_map_title:
        st.markdown("<h2 class='section-title'> Michelin Restaurants Map</h2>", unsafe_allow_html=True)
    with col_map_btn:
        # A simple button that triggers a rerun, which reapplies the mapbox bounds 
        # to effectively reset the zoom/pan back to auto-fit the data.
        st.button("Reset Map View (Auto-Fit)")
        
    if not filtered_df.empty:
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat="Latitude",
            lon="Longitude",
            color="Award",
            hover_name="Name",
            hover_data={"City": True, "District": True, "Cuisine": True, "Price": True, "Latitude": False, "Longitude": False},
            custom_data=["Url"],
            mapbox_style="carto-darkmatter",
            category_orders={
                "Award": ["Selected Restaurants", "Bib Gourmand", "1 Star", "2 Stars", "3 Stars"]
            },
            color_discrete_map={
                '3 Stars': '#BD1B21',        # Premium Michelin Red
                '2 Stars': '#FF6F00',        # Warm Orange
                '1 Star': '#FBC02D',         # Golden Yellow
                'Bib Gourmand': '#4CAF50',   # Vibrant Green
                'Selected Restaurants': '#7B1FA2' # Deep Violet/Purple
            }
        )
        fig_map.update_layout(
            paper_bgcolor="#050505",
            plot_bgcolor="#050505",
            font_color="#ffffff",
            legend=dict(
                bgcolor="rgba(10, 10, 10, 0.75)",
                bordercolor="rgba(212, 175, 55, 0.25)",
                borderwidth=1,
                font=dict(color="#ffffff", size=11),
                yanchor="bottom",
                y=0.08,
                xanchor="left",
                x=0.03
            )
        )
        if not selected_countries and not selected_cities and not selected_districts:
            # If no specific geography is selected, show the whole world
            fig_map.update_layout(
                height=600, 
                margin={"r":0,"t":0,"l":0,"b":0},
                mapbox=dict(zoom=1, center=dict(lat=20, lon=0))
            )
        else:
            # Calculate dynamic bounds for auto-zoom when specific places are selected
            lat_min, lat_max = filtered_df['Latitude'].astype(float).min(), filtered_df['Latitude'].astype(float).max()
            lon_min, lon_max = filtered_df['Longitude'].astype(float).min(), filtered_df['Longitude'].astype(float).max()
            
            center_lat = (lat_min + lat_max) / 2
            center_lon = (lon_min + lon_max) / 2
            
            import math
            max_bound = max(lat_max - lat_min, lon_max - lon_min)
            if max_bound == 0:
                zoom_level = 10
            else:
                zoom_level = max(1, math.log2(360 / max_bound) - 0.5)
            
            fig_map.update_layout(
                height=600, 
                margin={"r":0,"t":0,"l":0,"b":0},
                mapbox=dict(
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=zoom_level
                )
            )
            
        # Define hierarchical marker sizes for each award level to create a clear visual depth
        sizes = {
            '3 Stars': 7,
            '2 Stars': 7,
            '1 Star': 7,
            'Bib Gourmand': 5,
            'Selected Restaurants': 5
        }
        
        # Apply custom sizes and opacities per trace to replicate the reference image's density look
        for trace in fig_map.data:
            award_name = trace.name
            if award_name in sizes:
                trace.marker.size = sizes[award_name]
                if award_name == 'Selected Restaurants':
                    trace.marker.opacity = 0.3
                elif award_name == 'Bib Gourmand':
                    trace.marker.opacity = 0.3
                elif award_name == '1 Star':
                    trace.marker.opacity = 0.5
                else: # 2 Stars and 3 Stars
                    trace.marker.opacity = 0.5
        
        # Render map with click events enabled
        event = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun", selection_mode="points")
        
        # Display selected restaurant links and images
        if event and event.selection.points:
            selected_urls = [point["customdata"][0] for point in event.selection.points]
            selected_df_map = filtered_df[filtered_df["Url"].isin(selected_urls)]
            
            if not selected_df_map.empty:
                st.markdown("<h2 class='section-title'> Selected Restaurant Details</h2>", unsafe_allow_html=True)
                for _, row in selected_df_map.iterrows():
                    col_info, col_img = st.columns([2, 1])
                    with col_info:
                        st.info(
                            f"🍽️ **{row['Name']}** ({row['Award']}) - {row['Cuisine']}  \n"
                            f"📍 {row['Location']} (District: {row['District']}) | 💰 {row['Price']}  \n"
                            f"🔗 **[Click to view full details on Michelin Guide]({row['Url']})**"
                        )
                    with col_img:
                        with st.spinner("Fetching image..."):
                            img_url = fetch_michelin_image(row['Url'])
                            if img_url:
                                st.image(img_url, use_container_width=True)
                            else:
                                st.markdown("*(No image available)*")

    else:
        st.info("No restaurants found based on current filters.")

    # ------------------
    # Display Filtered Table
    # ------------------
    st.markdown("---")
    st.markdown(f"<h2 class='section-title'> Showing {len(filtered_df):,} Restaurants</h2>", unsafe_allow_html=True)
    st.markdown("""<style>
    .stDataFrame {background-color:#000000;color:#fafafa;}
    .stDataFrame thead th {background-color:#1a1a1a;color:#D4AF37;}
    .stDataFrame tbody tr:nth-child(even) {background-color:#111111;}
    .stDataFrame tbody tr:hover {background-color:#2a2a2a;}
    </style>""", unsafe_allow_html=True)
    st.dataframe(
        filtered_df[['Name', 'City', 'District', 'Country', 'Award', 'Cuisine', 'Price', 'Location', 'Url']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Url": st.column_config.LinkColumn("Michelin URL")
        }
    )

    # ------------------
    # Visualizations
    # ------------------
    st.markdown("---")
    st.markdown("<h2 class='section-title'> Visualizations</h2>", unsafe_allow_html=True)

    if not filtered_df.empty:
        # Visualizations Layout
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            # 1. จำนวนร้านตามประเทศ (Number of restaurants by country)
            country_counts = filtered_df['Country'].value_counts().reset_index()
            country_counts.columns = ['Country', 'Count']
            # Take top 15 for better visualization if there are many
            fig_country = px.bar(
                country_counts.head(15),
                x='Country',
                y='Count',
                title='Top 15 Countries by Number of Restaurants',
                color='Count',
                color_continuous_scale='Reds'
            )
            # Luxury dark theme for the chart
            fig_country.update_layout(
                paper_bgcolor='#050505',
                plot_bgcolor='#050505',
                font_color='#fafafa',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                title=dict(font=dict(color='#fafafa')),
                xaxis=dict(title_font=dict(color='#fafafa'), tickfont=dict(color='#fafafa')),
                yaxis=dict(title_font=dict(color='#fafafa'), tickfont=dict(color='#fafafa'))
            )
            # Show values with commas outside bars
            fig_country.update_traces(
                texttemplate='%{y:,}',
                textposition='outside',
                textfont=dict(color='#fafafa', size=14)
            )
            # Rotate x‑axis labels so the first character faces the viewer and the tail points forward
            fig_country.update_xaxes(tickangle=-90, visible=True)
            fig_country.update_yaxes(visible=False)
            st.plotly_chart(fig_country, use_container_width=True)

        with row1_col2:
            # 2. Top Cities
            city_counts = filtered_df['City'].value_counts().reset_index()
            city_counts.columns = ['City', 'Count']
            fig_city = px.bar(
                city_counts.head(15),
                x='City',
                y='Count',
                title='Top 15 Cities by Number of Restaurants',
                color='Count',
                color_continuous_scale='Reds'
            )
            # Luxury dark theme for the chart
            fig_city.update_layout(
                paper_bgcolor='#050505',
                plot_bgcolor='#050505',
                font_color='#ffffff',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                title=dict(font=dict(color='#ffffff')),
                xaxis=dict(title_font=dict(color='#ffffff'), tickfont=dict(color='#ffffff')),
                yaxis=dict(title_font=dict(color='#ffffff'), tickfont=dict(color='#ffffff')),
            )
            # Show values with commas outside bars
            fig_city.update_traces(
                texttemplate='%{y:,}',
                textposition='outside',
                textfont=dict(color='#fafafa', size=14)
            )
            fig_city.update_xaxes(tickangle=-90, visible=True)
            fig_city.update_yaxes(visible=False)
            st.plotly_chart(fig_city, use_container_width=True)

        row2_col1, row2_col2 = st.columns(2)
        
        with row2_col1:
            # 3. Star Distribution
            # ---- New Pie Chart: Award Distribution ----
            #st.markdown("#### Award Distribution")
            award_counts = filtered_df['Award'].value_counts().reset_index()
            award_counts.columns = ['Award', 'Count']
            fig_award = px.pie(
                award_counts,
                names='Award',
                values='Count',
                title='Michelin Award Distribution',
                color='Award',
                color_discrete_sequence=['#4B0000', '#800000', '#B22222', '#FF4500', '#FF7F7F']
            )
            # Apply luxury dark theme to pie
            fig_award.update_layout(
                paper_bgcolor='#050505',
                plot_bgcolor='#050505',
                font_color='#fafafa',
                title=dict(font=dict(color='#fafafa')),
                xaxis=dict(title_font=dict(color='#fafafa'), tickfont=dict(color='#fafafa')),
                yaxis=dict(title_font=dict(color='#fafafa'), tickfont=dict(color='#fafafa')),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#fafafa'))
            )
            # Show percentages and labels on slices with white text
            fig_award.update_traces(textinfo='percent+label', pull=0.02, textfont=dict(color='#ffffff'))
            st.plotly_chart(fig_award, use_container_width=True)

        with row2_col2:
            # 5. Price Level Distribution
            price_counts = filtered_df['Price'].value_counts().reset_index()
            price_counts.columns = ['Price Level', 'Count']
            fig_price = px.bar(
                price_counts,
                x='Price Level',
                y='Count',
                title='Price Level Distribution',
                color='Count',
                color_continuous_scale='Reds'
            )
            # Luxury dark theme for the chart
            fig_price.update_layout(
                paper_bgcolor='#050505',
                plot_bgcolor='#050505',
                font_color='#fafafa',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                title=dict(font=dict(color='#fafafa')),
                xaxis=dict(title_font=dict(color='#fafafa'), tickfont=dict(color='#fafafa')),
                yaxis=dict(title_font=dict(color='#fafafa'), tickfont=dict(color='#fafafa')),
            )
            # Show values with commas outside bars
            fig_price.update_traces(
                texttemplate='%{y:,}',
                textposition='outside',
                textfont=dict(color='#fafafa', size=14)
            )
            fig_price.update_xaxes(tickangle=-90, visible=True)
            fig_price.update_yaxes(visible=False)    
            st.plotly_chart(fig_price, use_container_width=True)

        # 4. Cuisine Distribution
        #st.markdown("#### Top 20 Cuisines")
        cuisine_counts = filtered_df['Cuisine'].value_counts().reset_index()
        cuisine_counts.columns = ['Cuisine', 'Count']
        fig_cuisine = px.bar(
            cuisine_counts.head(20),
            x='Count',
            y='Cuisine',
            orientation='h',
            title='Top 20 Cuisines',
            color='Count',
            color_continuous_scale='OrRd'
        )
        # Luxury dark theme for the chart (horizontal bar)
        fig_cuisine.update_layout(
            paper_bgcolor='#050505',
            plot_bgcolor='#050505',
            font_color='#fafafa',
            yaxis=dict(categoryorder='total ascending', tickfont=dict(color='#fafafa')),
            height=600,
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            title=dict(font=dict(color='#fafafa')),
            xaxis=dict(tickfont=dict(color='#fafafa')),
        
        )
        # Show values with commas outside bars (horizontal bars use x values)
        fig_cuisine.update_traces(
            texttemplate='%{x:,}',
            textposition='outside',
            textfont=dict(color='#fafafa')
        )
        fig_cuisine.update_xaxes(tickangle=-90)
        fig_cuisine.update_xaxes(visible=False)    
        st.plotly_chart(fig_cuisine, use_container_width=True)

       
