import plotly.express as px
import pandas as pd

def create_globe_chart(df: pd.DataFrame):
    if df.empty:
        # Return an empty globe if no data
        fig = px.scatter_geo(projection="orthographic")
    else:
        # Define a custom color map for Awards
        color_discrete_map = {
            '3 Stars': '#E53935',          # Deep Red
            '2 Stars': '#FB8C00',          # Orange
            '1 Star': '#FDD835',           # Yellow
            'Bib Gourmand': '#43A047',     # Green
            'Selected Restaurants': '#8E24AA' # Purple
        }

        # Create interactive 3D globe
        fig = px.scatter_geo(
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
            projection="orthographic",
            title="Michelin Guide Restaurants on 3D Globe",
            color_discrete_map=color_discrete_map
        )

    # Styling the globe for better look
    fig.update_layout(
        height=800,
        margin={"r":0,"t":40,"l":0,"b":0},
        geo=dict(
            showland=True,
            showcountries=True,
            showocean=True,
            countrywidth=0.5,
            landcolor="rgb(243, 243, 243)",
            oceancolor="rgb(204, 229, 255)",
            projection_type="orthographic"
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

    # Increase marker size and add a subtle border to make them easier to see and click
    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(width=1, color='rgba(255, 255, 255, 0.5)')
        )
    )

    return fig
