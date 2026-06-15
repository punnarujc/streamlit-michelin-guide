import streamlit as st
from data import load_kaggle_data, get_restaurants, get_unique_awards
from charts import create_globe_chart

st.title("Michelin Guide 2021 Map 🗺️")

# Initialize and load data
with st.spinner("Downloading and Loading Michelin Guide Dataset..."):
    load_kaggle_data()

# Fetch unique awards for the filter
all_awards = get_unique_awards()
default_awards = [a for a in all_awards if 'Star' in a] # Default to showing starred restaurants

# Filters in main area
selected_awards = st.multiselect(
    "Filter by Award",
    options=all_awards,
    default=default_awards
)

# Get data
df = get_restaurants(awards=selected_awards)

# Render Chart
st.subheader(f"Showing {len(df)} Restaurants")
fig = create_globe_chart(df)
event = st.plotly_chart(
    fig,
    width="stretch",
    on_select="rerun",
    selection_mode="points",
    config={"scrollZoom": True, "displayModeBar": True}
)

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
