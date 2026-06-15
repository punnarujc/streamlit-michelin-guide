import plotly.express as px
import pandas as pd

def create_globe_chart(df: pd.DataFrame):
    if df.empty:
        # Return an empty map if no data
        import plotly.graph_objects as go
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(mapbox_style="carto-darkmatter")
    else:
        # Define a custom color map for Awards
        color_discrete_map = {
            '3 Stars': '#BD1B21',        # Premium Michelin Red
            '2 Stars': '#FF6F00',        # Warm Orange
            '1 Star': '#FBC02D',         # Golden Yellow
            'Bib Gourmand': '#4CAF50',   # Vibrant Green
            'Selected Restaurants': '#7B1FA2' # Deep Violet/Purple
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
            mapbox_style="carto-darkmatter",
            category_orders={
                "Award": ["Selected Restaurants", "Bib Gourmand", "1 Star", "2 Stars", "3 Stars"]
            },
            zoom=1,
            title="Michelin Guide Restaurants on Map",
            color_discrete_map=color_discrete_map
        )

    # Styling the map for better look
    fig.update_layout(
        height=800,
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor="#050505",
        plot_bgcolor="#050505",
        font_color="#ffffff",
        mapbox=dict(
            style="carto-darkmatter",
            zoom=1.5
        ),
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

    # Apply custom sizes and opacities per trace to create a clear visual depth
    sizes = {
        '3 Stars': 16,
        '2 Stars': 12,
        '1 Star': 9,
        'Bib Gourmand': 6.5,
        'Selected Restaurants': 4.5
    }
    for trace in fig.data:
        award_name = trace.name
        if award_name in sizes:
            trace.marker.size = sizes[award_name]
            if award_name == 'Selected Restaurants':
                trace.marker.opacity = 0.55
            elif award_name == 'Bib Gourmand':
                trace.marker.opacity = 0.70
            elif award_name == '1 Star':
                trace.marker.opacity = 0.85
            else: # 2 Stars and 3 Stars
                trace.marker.opacity = 0.95

    return fig
