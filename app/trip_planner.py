import os
import requests
import streamlit as st
from app.data import load_data, get_restaurants, get_unique_awards

# Re-apply the luxury dark theme for the page contents
st.markdown("""
<style>
.stApp {
    background: #050505;
}
.block-container {
    max-width: 1500px;
}
.michelin-hero {
    position: relative;
    padding: 60px 50px;
    border-radius: 20px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0.92) 35%, rgba(0, 0, 0, 0.05) 80%), url('https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.1.0');
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    color: white;
    margin-bottom: 35px;
    min-height: 300px;
    display: flex;
    align-items: center;
    overflow: hidden;
    border: 1px solid #1a1a1a;
}
.michelin-hero-content {
    position: relative;
    z-index: 2;
    max-width: 700px;
}
.michelin-hero-meta {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #ffffff;
    margin-bottom: 15px;
    text-transform: uppercase;
}
.brand-michelin {
    font-family: 'Georgia', serif !important;
    font-size: 48px !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    line-height: 1.1 !important;
    color: #ffffff !important;
    margin: 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.brand-guide {
    font-family: 'Georgia', serif !important;
    font-size: 38px !important;
    font-weight: 400 !important;
    font-style: italic !important;
    letter-spacing: 4px !important;
    line-height: 1.1 !important;
    color: #BD1B21 !important;
    margin: 5px 0 0 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.stars-gold {
    color: #D4AF37 !important;
    font-size: 18px !important;
    margin-top: 10px;
    letter-spacing: 5px;
}
.section-title {
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 15px;
    margin-top: 15px;
    font-family: 'Georgia', serif !important;
}
/* Luxury styled input boxes */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 12px !important;
}
div[data-baseweb="select"] > div {
    background-color: #0c0c0c !important;
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 8px !important;
    box-shadow: 0 0 6px rgba(212, 175, 55, 0.08) !important;
}
div[data-baseweb="select"] * {
    color: #ffffff !important;
}
/* Luxury styled button */
div.stButton > button {
    background-color: #BD1B21 !important;
    color: #ffffff !important;
    border: 1px solid #991014 !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #e60028 !important;
    border-color: #BD1B21 !important;
    box-shadow: 0 4px 15px rgba(189, 27, 33, 0.4) !important;
    color: #ffffff !important;
}
.itinerary-container {
    background-color: #0c0c0c;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
    border-radius: 14px;
    padding: 30px;
    margin-top: 25px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="michelin-hero">
    <div class="michelin-hero-content">
        <div class="michelin-hero-meta">GASTRONOMIC ROUTE PLANNER <span style="color: #BD1B21;">• OPENROUTER AI</span></div>
        <h1 class="brand-michelin">MICHELIN GUIDE</h1>
        <h1 class="brand-guide">Trip Itinerary Creator</h1>
        <div class="stars-gold">★ ★ ★</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load Data
sf_passcode = st.session_state.get("snowflake_passcode")
if not st.session_state.get("data_loaded", False):
    with st.spinner("Loading Michelin Guide Dataset..."):
        load_data(snowflake_passcode=sf_passcode)
else:
    load_data(snowflake_passcode=sf_passcode)

# Fetch all data by passing all awards
all_awards = get_unique_awards()
df = get_restaurants(awards=all_awards)

if df.empty:
    st.error("No data found or failed to load data.")
else:
    # Basic data preprocessing to extract City/Country if empty
    if 'City' not in df.columns or df['City'].isnull().all() or 'Country' not in df.columns or df['Country'].isnull().all():
        location_split = df['Location'].str.split(', ', n=1, expand=True)
        df['City'] = location_split[0]
        df['Country'] = location_split[1].fillna('Unknown')
    else:
        df['City'] = df['City'].fillna('Unknown')
        df['Country'] = df['Country'].fillna('Unknown')

    if 'District' not in df.columns or df['District'].isnull().all():
        def get_district(row):
            parts = [p.strip() for p in str(row['Address']).split(',')]
            try:
                idx = parts.index(row['City'])
                return parts[idx-1] if idx > 0 else 'Unknown'
            except ValueError:
                return 'Unknown'
        df['District'] = df.apply(get_district, axis=1)
    else:
        df['District'] = df['District'].fillna('Unknown')

    # Build dropdown selections
    countries = sorted(df['Country'].dropna().unique().tolist())

    st.markdown("<h3 class='section-title'>Plan Your Journey</h3>", unsafe_allow_html=True)

    # Check env variables
    env_api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
    env_model = st.secrets.get("OPENROUTER_MODEL", os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash"))

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_country = st.selectbox("Select Country", options=countries, index=countries.index("Thailand") if "Thailand" in countries else 0)

        # Filter cities based on selected country
        filtered_cities = sorted(df[df['Country'] == selected_country]['City'].dropna().unique().tolist())

        with col2:
            selected_city = st.selectbox("Select City", options=filtered_cities, index=filtered_cities.index("Bangkok") if "Bangkok" in filtered_cities else 0)
        with col3:
            duration_days = st.slider("Trip Duration (Days)", min_value=1, max_value=7, value=3)

        # API Key management
        api_key = env_api_key
        if not env_api_key:
            api_key = st.text_input("Enter OpenRouter API Key", type="password", help="Sign up at openrouter.ai to get a key.")

    # Filter restaurants for the selected city
    city_df = df[df['City'] == selected_city]

    if city_df.empty:
        st.warning(f"No Michelin Guide restaurants found for {selected_city}.")
    else:
        st.info(f"Found {len(city_df)} Michelin-selected restaurants in {selected_city}.")

        # Action button
        if st.button("Generate Travel Itinerary"):
            if not api_key:
                st.error("Please provide an OpenRouter API Key either in your .env file or the input field above.")
            else:
                with st.spinner("Our AI Gastronomy Planner is crafting your exquisite itinerary..."):
                    # Format restaurant context
                    # Limit number of restaurants to keep context payload reasonable
                    sample_size = min(len(city_df), 40)
                    selected_restaurants = city_df.sample(n=sample_size)

                    restaurant_list = []
                    for _, row in selected_restaurants.iterrows():
                        restaurant_list.append(
                            f"- {row['Name']} ({row['Award']}) | Cuisine: {row['Cuisine']} | Price: {row['Price']} | District: {row['District']} | URL: {row['Url']}"
                        )
                    restaurant_context = "\n".join(restaurant_list)

                    # Construct query
                    system_prompt = (
                        "You are an elite gourmet travel guide curator. You design stunning, high-end travel itineraries "
                        "centered around fine dining experiences. Ensure you only suggest restaurants provided in the context list. "
                        "Always list the restaurant names as hyperlinked text pointing to their exact Michelin Guide URL."
                    )

                    user_prompt = (
                        f"Please plan a premium {duration_days}-day travel itinerary for a visitor in {selected_city}.\n\n"
                        f"Here are the available Michelin-starred and selected restaurants in {selected_city}:\n"
                        f"{restaurant_context}\n\n"
                        "For each day:\n"
                        "- Suggest a themed morning activity (sightseeing, culture, local history).\n"
                        "- Recommend one of the listed Michelin restaurants for Lunch (matching the geographic district of the activity if possible).\n"
                        "- Suggest a relaxing afternoon activity.\n"
                        "- Recommend another listed Michelin restaurant for Dinner.\n\n"
                        "Requirements:\n"
                        "1. Ensure ALL suggested restaurants are from the provided list.\n"
                        "2. Every restaurant mentioned MUST be hyperlinked using markdown format: [Restaurant Name](URL).\n"
                        "3. Design the layout to be extremely premium, organized by Day 1, Day 2, etc., using headers and clean bullet points.\n"
                        "4. Add a quick 'Curator's Note' at the start highlighting the culinary signature of the city."
                    )

                    # API call
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/punnarujc/streamlit-michelin-guide",
                        "X-Title": "Michelin Guide Globe"
                    }

                    payload = {
                        "model": env_model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    }

                    try:
                        response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=payload,
                            timeout=60
                        )

                        if response.status_code == 200:
                            result = response.json()
                            content = result['choices'][0]['message']['content']

                            st.markdown("<h3 class='section-title'>Your Curated Culinary Itinerary</h3>", unsafe_allow_html=True)
                            st.markdown(f"<div class='itinerary-container'>{content}</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"OpenRouter API returned error code {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"Failed to generate itinerary. Exception details: {str(e)}")
