import streamlit as st
from data import load_kaggle_data, get_restaurants, get_unique_awards
from charts import create_globe_chart

st.set_page_config(
    page_title="Michelin Guide Globe",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling (premium look)
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    h1 {
        color: #E53935;
        font-family: 'Inter', sans-serif;
        text-align: center;
        padding: 20px;
    }
    .stSelectbox label, .stMultiSelect label {
        color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

st.title("Michelin Guide 2021 on a 3D Globe 🌍")

# Initialize and load data
with st.spinner("Downloading and Loading Michelin Guide Dataset..."):
    load_kaggle_data()

# Fetch unique awards for the filter
all_awards = get_unique_awards()
default_awards = [a for a in all_awards if 'Star' in a] # Default to showing starred restaurants

# Sidebar for filters
st.sidebar.header("Filters")
selected_awards = st.sidebar.multiselect(
    "Filter by Award",
    options=all_awards,
    default=default_awards
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### About
    This is an interactive 3D globe visualizing the **Michelin Guide Restaurants 2021** dataset from Kaggle.
    Built with **Streamlit**, **DuckDB**, and **Plotly**.
    """
)

# Get data
df = get_restaurants(awards=selected_awards)

# Render Chart
st.subheader(f"Showing {len(df)} Restaurants")
fig = create_globe_chart(df)
event = st.plotly_chart(fig, width="stretch", on_select="rerun", selection_mode="points")

# Show Details Table on Selection
if event and event.selection.points:
    selected_urls = [point["customdata"][0] for point in event.selection.points]
    selected_df = df[df["Url"].isin(selected_urls)]

    st.markdown("### 🍽️ Selected Restaurant Details")
    # Display the selected data nicely
    st.dataframe(
        selected_df[["Name", "Award", "Location", "Price", "Cuisine", "FacilitiesAndServices", "Url"]],
        width="stretch",
        hide_index=True
    )
