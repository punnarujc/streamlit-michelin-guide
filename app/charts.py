import plotly.express as px
import pandas as pd

def create_globe_chart(df: pd.DataFrame):
    if df.empty:
        # Return an empty map if no data
        import plotly.graph_objects as go
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(mapbox_style="carto-positron")
    else:
        # Define a custom color map for Awards
        color_discrete_map = {
            '3 Stars': '#E53935',          # Deep Red
            '2 Stars': '#FB8C00',          # Orange
            '1 Star': '#FDD835',           # Yellow
            'Bib Gourmand': '#43A047',     # Green
            'Selected Restaurants': '#8E24AA' # Purple
        }

        # Create interactive map
        fig = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            color="Award",
            hover_name="Name",
            custom_data=["Url"],
            hover_data={
                "Award": True,
                "Location": True,
                "Cuisine": True,
                "Price": True,
                "Latitude": False,
                "Longitude": False
            },
            mapbox_style="carto-positron",
            zoom=1,
            title="Michelin Guide Restaurants on Map",
            color_discrete_map=color_discrete_map
        )

    # Styling the map for better look
    fig.update_layout(
        height=800,
        margin={"r":0,"t":40,"l":0,"b":0},
        mapbox=dict(
            style="carto-positron",
            zoom=1.5
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=""
        )
    )

    # Increase marker size to make them easier to see and click
    fig.update_traces(
        marker=dict(
            size=10
        )
    )

    return fig
