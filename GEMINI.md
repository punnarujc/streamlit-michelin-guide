# Project Context: Michelin Guide Globe Webapp

## Overview
This repository contains a Streamlit-based web application that visualizes Michelin Guide restaurants on an interactive 3D globe.

## Architecture & Tech Stack
*   **Framework:** Streamlit (Frontend/Backend unified)
*   **Data Processing:** DuckDB (In-memory analytical SQL engine)
*   **Visualization:** Plotly Express (Orthographic scatter geo projection)
*   **Environment Management:** Python `uv`

## Design Principles
1.  **Separation of Concerns:** Keep data extraction/transformation logic (DuckDB) separate from the UI rendering logic (Streamlit/Plotly).
2.  **Performance:** Utilize `@st.cache_data` heavily for DuckDB queries to prevent redundant I/O and re-computations on UI state changes.
3.  **Resilience:** The application must handle missing data gracefully and provide a robust default state.

## Current State
*   Landing page implemented with a full-width, interactive Plotly globe chart (height expanded).
*   Application is functional with DuckDB backend, Plotly charts, and Streamlit frontend.
*   Makefile added for easier project setup and running.
*   Integrated real Michelin Guide 2021 dataset using `kagglehub`.
*   Codebase restructured by moving the Streamlit files into an `app/` directory.
*   Globe chart features interactive point selection that filters and displays restaurant details in a data table.
*   Globe points styled with larger markers and borders to enhance selectability.

## Next Implementation Steps
1.  **Advanced Filtering:** Add more interactive filters to the Streamlit sidebar (e.g., filter by Country, City, Cuisine type).
