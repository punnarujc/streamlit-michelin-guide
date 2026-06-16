# Michelin Guide Globe — Interactive Web App

A premium, interactive **Streamlit** web application that visualizes Michelin Guide restaurants on a global dark-map, with advanced filtering, distribution analytics, and an AI-powered gastronomic trip planner.

---

## Features at a Glance

| Feature | Description |
|---|---|
| **Interactive World Map** | Plotly Mapbox (darkmatter) scatter map of all Michelin-selected restaurants |
| **Advanced Filters** | Country → City → District → Award → Price → Name cascading multiselects |
| **Distribution Analytics** | Bar & pie charts for countries, cities, awards, prices, and cuisines |
| **Styled Data Table** | Sortable restaurant table with direct Michelin Guide URL links |
| **AI Trip Planner** | OpenRouter-powered itinerary generator using local Michelin restaurants |
| **Multi-Backend Data** | Merges MySQL, MongoDB, and Snowflake; falls back to Kaggle CSV |
| **DuckDB Query Engine** | Fast in-memory SQL caching for all filter and aggregation queries |

---

## Architecture & Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Streamlit (unified frontend + backend) |
| **Query Engine** | DuckDB (in-memory, cached SQL analytics) |
| **Databases** | MySQL (`pymysql`), MongoDB (`pymongo`), Snowflake (`snowflake-connector-python`) |
| **Fallback** | Kagglehub — `ngshiheng/michelin-guide-restaurants-2021` |
| **Visualization** | Plotly Express (Mapbox scatter, bar, pie charts) |
| **AI Integration** | OpenRouter API (configurable model, default: `google/gemini-2.5-flash`) |
| **Env Manager** | Python `uv` |

---

## Project Structure

```
.
├── app/
│   ├── app.py              # Multi-page entrypoint, global styling, navigation
│   ├── michelin_guide.py   # Landing page — map, filters, analytics
│   ├── trip_planner.py     # AI Trip Planner page
│   └── data.py             # Backend interface: DB connections, caching, DuckDB
├── scripts/
│   ├── import_mysql.py     # ETL: parse & upload to MySQL
│   ├── import_mongodb.py   # ETL: parse & upload to MongoDB
│   ├── import_snowflake.py # ETL: parse & upload to Snowflake
│   └── utils.py            # Shared ETL helpers
├── Makefile                # setup / run / clean
└── README.md
```

---

## Pages

### 1. Landing Page — Michelin Guide Dashboard (`michelin_guide.py`)

The main landing page is a luxury-themed, full-featured restaurant explorer.

#### Hero Section
A full-width cinematic banner styled in dark luxury aesthetics (Michelin red `#BD1B21` and gold `#D4AF37`), featuring the **MICHELIN GUIDE** brand mark, a 3-star separator, bilingual English/Thai subtitle, and contextual pills highlighting new entries (e.g., *Thailand 2026*).

#### Summary Panel
Four bespoke metric counters — **Restaurants**, **Countries**, **Cities**, and **Award Categories** — rendered as gold-accented cards. All values update dynamically as filters are applied.

#### Filter Panel (gold-bordered container)
A cascading, 2-row multiselect panel with **6 filter dimensions**:

| Row | Filters |
|---|---|
| Row 1 | Country → City → District |
| Row 2 | Award → Price Level → Restaurant Name |

- City options narrow automatically when a country is selected.
- District options narrow further based on country + city.
- Restaurant names narrow based on all active filters above.
- A **Clear All Filters** button resets everything instantly.

#### Interactive Plotly Map
A Plotly Mapbox `carto-darkmatter` scatter map with:
- **Colour-coded award markers**: 3 Stars (red), 2 Stars (orange), 1 Star (gold), Bib Gourmand (green), Selected Restaurants (violet)
- **Hierarchical opacity/size** — starred restaurants are more prominent
- **Auto-fit zoom** — when a country/city filter is active, the map re-centres and zooms to the selection; otherwise defaults to a global view
- **Reset Map View** button to snap back to the auto-fit default
- **Click-to-select** mode — clicking a point opens a detail card showing name, award, cuisine, location, price, a direct Michelin Guide link, and a **live-scraped restaurant photo** (via OpenGraph tags)

#### Filterable Data Table
A styled dark-themed `st.dataframe` listing up to 9 columns (`Name`, `City`, `District`, `Country`, `Award`, `Cuisine`, `Price`, `Location`, `Url`). The Michelin URL column is rendered as a clickable link.

#### Visualizations
Four Plotly charts presented in a 2×2 grid (dark luxury theme):
1. **Top 15 Countries by Number of Restaurants** — bar chart
2. **Top 15 Cities by Number of Restaurants** — bar chart
3. **Award Distribution** — pie chart
4. **Price Level Distribution** — pie chart

---

### 2. Trip Planner Page — AI Gastronomic Itinerary (`trip_planner.py`)

An AI-driven travel planner that generates customised, day-by-day gastronomic itineraries for any Michelin-covered city.

#### Hero Section
Shares the same luxury dark aesthetic with a different background (fine-dining photography), styled with the sub-title **"Trip Itinerary Creator"** in Michelin red italic.

#### Journey Configuration Panel (gold-bordered container)
Three controls in a single row:

| Control | Description |
|---|---|
| **Select Country** | Dropdown of all countries in the dataset (defaults to Thailand) |
| **Select City** | Dropdown filtered to the selected country (defaults to Bangkok) |
| **Trip Duration** | Slider — 1 to 7 days (default 3) |

- If no `OPENROUTER_API_KEY` is set in secrets/env, an inline password field appears for ad-hoc key entry.

#### Restaurant Context Card
Displays the count of Michelin-selected restaurants found in the chosen city so the user can verify coverage before generating.

#### Generate Travel Itinerary (button)
On click:
1. Samples up to **40 restaurants** from the city's data.
2. Formats a rich restaurant context list (name, award, cuisine, price, district, URL).
3. Sends a structured prompt to the **OpenRouter API** using the configured model.
4. The **system prompt** instructs the model to act as an elite gourmet travel curator and to only suggest restaurants from the provided list, always hyperlinked to their Michelin Guide URL.
5. The **user prompt** requests a premium, day-structured itinerary with morning activity → Michelin lunch → afternoon activity → Michelin dinner, plus a "Curator's Note" about the city's culinary signature.
6. The generated markdown is rendered inside a gold-bordered **itinerary container** card.

---

## Data Sources & Column Mapping

| Column | Source |
|---|---|
| `Name`, `Location`, `Cuisine`, `Price`, `Award`, `Url`, `Latitude`, `Longitude` | MySQL |
| `Address`, `PhoneNumber`, `Description` | MongoDB |
| `City`, `State`, `Country`, `District` | Snowflake |
| All columns (fallback) | Kagglehub CSV |

Records from all active sources are merged via outer join on `Url`. Missing columns from a failed backend are recovered from whichever backend succeeded.

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/punnarujc/streamlit-michelin-guide.git
cd streamlit-michelin-guide
make setup
```

### 2. Configure Environment

Create a `.env` file or set `st.secrets` with the following keys (all optional — the app falls back gracefully):

```env
# MySQL
MYSQL_HOST=...
MYSQL_PORT=3306
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DATABASE=...

# MongoDB
MONGO_URI=...
MONGO_DATABASE=...
MONGO_COLLECTION=...

# Snowflake
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=...
SNOWFLAKE_SCHEMA=...

# OpenRouter (Trip Planner)
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=google/gemini-2.5-flash
```

### 3. Run

```bash
make run
# or
uv run streamlit run app/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ETL Scripts

To populate your databases from the Kaggle dataset:

```bash
uv run python scripts/import_mysql.py
uv run python scripts/import_mongodb.py
uv run python scripts/import_snowflake.py
```

Each script parses `Location` into `City`/`State`/`Country`, extracts `District`, cleans nulls, and batch-uploads to the respective database.

---

## Design System

| Token | Value | Usage |
|---|---|---|
| Background | `#050505` | Page base |
| Surface | `#0a0a0a / #0c0c0c` | Cards, panels |
| Gold | `#D4AF37` | Accents, borders, icons |
| Michelin Red | `#BD1B21` | CTAs, pills, selected chips |
| Text Primary | `#ffffff` | Headings, values |
| Text Secondary | `#cccccc / #888888` | Labels, subtitles |
| Font — Display | Georgia, serif | Hero headings, metric values |
| Font — UI | Arial / system-ui | Labels, body |

---

## Roadmap

1. **Direct Database Write-backs** — user-generated reviews and bookmarks stored back to the database
2. **User Authentication** — personalised guide views with login support
