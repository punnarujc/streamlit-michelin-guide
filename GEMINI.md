# Project Context: Michelin Guide Globe Webapp

## Overview
This repository contains a Streamlit-based web application that visualizes Michelin Guide restaurants on an interactive 2D map.

## Architecture & Tech Stack
*   **Framework:** Streamlit (Frontend/Backend unified)
*   **Data Processing:** DuckDB (In-memory analytical SQL engine)
*   **Visualization:** Plotly Express (Mapbox WebGL scatter projection)
*   **Environment Management:** Python `uv`

## Design Principles
1.  **Separation of Concerns:** Keep data extraction/transformation logic (DuckDB) separate from the UI rendering logic (Streamlit/Plotly).
2.  **Performance:** Utilize `@st.cache_data` heavily for DuckDB queries to prevent redundant I/O and re-computations on UI state changes.
3.  **Resilience:** The application must handle missing data gracefully and provide a robust default state.

## Current State
*   Landing page implemented with a full-width, interactive Plotly map chart (height expanded).
*   Application is functional with DuckDB backend, Plotly charts, and Streamlit frontend.
*   Makefile added for easier project setup and running.
*   Integrated real Michelin Guide 2021 dataset using `kagglehub`.
*   Codebase restructured by moving the Streamlit files into an `app/` directory.
*   Map chart features interactive point selection that filters and displays restaurant details in a data table.
*   Map points styled with larger markers to enhance selectability.
*   Map explicitly configured with scroll zoom and a display modebar for easier navigation.
*   Filter by Award control moved from the sidebar to the main content area (middle).

## Next Implementation Steps
1.  **Advanced Filtering:** Add more interactive filters (e.g., filter by Country, City, Cuisine type).
