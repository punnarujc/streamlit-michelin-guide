# Project Context: Michelin Guide Globe Webapp

> [!NOTE]
> **Task Completed:** Integrated OpenRouter with the Michelin database to create a premium, AI-curated trip planning page. Users can select any city, define trip duration, and receive a customized gastronomic travel itinerary detailing Michelin-starred restaurants.

## Overview

This repository contains a premium, interactive Streamlit-based web application that visualizes Michelin Guide restaurants on a global 2D darkmatter map with advanced filtering, analytics, and dynamic database backends.

## Architecture & Tech Stack

- **Framework:** Streamlit (Frontend/Backend unified, structured with page navigation)
- **In-Memory DB / Query Engine:** DuckDB (Used to perform fast, cached SQL-based analytical querying, filtering, and standardizing data logic on-the-fly)
- **Dynamic Data Sources:** Supports simultaneous multi-backend fetching, merging, and deduplicating data across MySQL, MongoDB, and Snowflake.
  - **MySQL** (using `pymysql`)
  - **MongoDB** (using `pymongo`)
  - **Snowflake** (using `snowflake-connector-python`)
- **Fallback Source:** Kagglehub (automatically downloads the `ngshiheng/michelin-guide-restaurants-2021` CSV dataset if all active database connections fail)
- **Visualization:** Plotly Express (Mapbox WebGL scatter projection for mapping; bar and pie charts for distribution analytics)
- **Environment & Dependency Management:** Python `uv`

## Design Principles & Data Pipelines

1.  **Separation of Concerns:** Keep raw database extraction and processing logic (managed by scripts in `scripts/` and helper database-fetching methods in `app/data.py`) separate from client-side UI rendering (`app/michelin_guide.py`).
2.  **Performance & Caching:** Heavy utilization of `@st.cache_data` and `@st.cache_resource` for connection pooling, raw database loading (based on credential hash), SQL queries, and scraping to prevent redundant round-trips and I/O.
3.  **Resilience & Graceful Degradation:** The application attempts to connect to all configured database backends, fetching specific column slices from each database (MySQL, MongoDB, Snowflake) and merging them column-wise via an outer-join on `Url`. If any individual backend fails, its columns are recovered from another successfully loaded database, and its connection error is displayed in the sidebar status panel. If all database connections fail, it falls back to the Kagglehub dataset.
4.  **Premium Aesthetics:** A unified, dark luxury-themed design utilizing custom CSS. Text features gold/red/white palettes, styled select chips, custom metric summaries, styled datatables, and a dedicated database connection status dashboard panel in the sidebar.

## Codebase Structure

- **`app/app.py`:** Main multi-page entrypoint setting global configurations, premium styling, custom navigation structure, and database fallback banners.
- **`app/michelin_guide.py`:** Main UI logic housing the map dashboard, filters, charts, metrics, and details view.
- **`app/trip_planner.py`:** Trip planning UI logic integrating OpenRouter to construct custom itineraries with local Michelin restaurants.
- **`app/data.py`:** Backend interface handling connection pooling, standardization/normalization, multi-backend fetching, Kagglehub fallback, and DuckDB table instantiation.
- **`scripts/`:** Automated ETL pipeline scripts (`import_mysql.py`, `import_mongodb.py`, `import_snowflake.py`, and `utils.py`) to parse Location fields (into City/State/Country), extract Districts, clean nulls, and batch-upload processed data to the respective database system.
- **`Makefile`:** Orchestrates project environment configuration (`setup`, `run`, `clean`) with `uv`.

## Current State & Features

- **Advanced Filtering Controls:** Gold-bordered filtering panel featuring nested multiselects (Country, City, District, Award, Price Level, and search by Name) that dynamically narrow down options.
- **Interactive Map (Plotly Mapbox):** Configured with darkmatter style, scroll zoom, and a Reset Map View button. Employs hierarchical marker scaling and opacities based on awards (Stars are larger and more prominent than Bib Gourmands/Selected Restaurants).
- **Dynamic Summary Panel:** Custom-designed luxury counters displaying the total filtered counts of restaurants, countries, cities, and awards.
- **On-Select Detail Card:** Clicking map points isolates the restaurant, displays key metadata (Address, Cuisine, Price, URL), and dynamically scrapes the restaurant's actual photo from the Michelin Guide URL via OpenGraph tags.
- **Distribution Analytics:** Dynamic Plotly dashboards displaying distribution charts for countries, cities, awards, price levels, and cuisines.
- **OpenRouter AI Trip Planner:** Interactive page with dropdown city selections, itinerary duration sliders, and customized AI itinerary generation using Michelin Guide restaurants as hyperlinked items.

## Next Implementation Steps

1.  **Direct Database Write-backs:** Support user-generated reviews or bookmarks stored directly back to the database.
2.  **User Authentication:** Add login capabilities to customize guide views.
