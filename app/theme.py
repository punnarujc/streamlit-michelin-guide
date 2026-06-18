"""Shared luxury colour theme, extracted from the Michelin Guide page so the
Trip Planner and AI Assistant pages use the exact same palette.

Palette:
  background  #050505      cards/inputs  #0c0c0c
  gold accent #D4AF37      michelin red  #BD1B21 (hover #e60028, dark #991014)
  text        #ffffff      secondary     #cccccc / muted #888888
"""

THEME_CSS = """
<style>
/* ---- base ---- */
.stApp { background: #050505; }
.block-container { max-width: 1500px; }

/* ---- top header bar ---- */
header, [data-testid="stHeader"], .stAppHeader {
    background-color: #050505 !important;
    background: #050505 !important;
    border-bottom: 1px solid #101010 !important;
}
header *, [data-testid="stHeader"] *, .stAppHeader * { color: #ffffff !important; }
header svg, [data-testid="stHeader"] svg, .stAppHeader svg { fill: #ffffff !important; }

/* ---- headings ---- */
h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
.section-title {
    font-weight: 700;
    color: #ffffff !important;
    margin: 15px 0;
    font-family: 'Georgia', serif !important;
}

/* ---- bordered containers (gold) ---- */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 12px !important;
}

/* ---- widget labels ---- */
.stMultiSelect label, .stSelectbox label, .stSlider label, .stTextInput label {
    color: #cccccc !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    margin-bottom: 6px !important;
}

/* ---- select / multiselect ---- */
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
div[data-baseweb="select"] * { color: #ffffff !important; }
div[data-baseweb="select"] svg { fill: #ffffff !important; }

/* selected chips/tags (michelin red) */
span[data-baseweb="tag"] { background-color: #BD1B21 !important; border-radius: 6px !important; }
span[data-baseweb="tag"] span { color: #ffffff !important; }

/* ---- buttons (michelin red) ---- */
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
</style>
"""


def apply_theme():
    """Inject the shared theme CSS. Call once near the top of a page."""
    import streamlit as st
    st.markdown(THEME_CSS, unsafe_allow_html=True)
