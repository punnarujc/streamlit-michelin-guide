import duckdb
import pandas as pd
import streamlit as st
import kagglehub
import os

@st.cache_resource
def get_db_connection():
    # Using an in-memory DuckDB database
    conn = duckdb.connect(':memory:')
    return conn

@st.cache_data
def load_kaggle_data():
    conn = get_db_connection()

    # Download dataset from Kaggle
    path = kagglehub.dataset_download("ngshiheng/michelin-guide-restaurants-2021")
    csv_file = os.path.join(path, "michelin_my_maps.csv")

    # Create table and load data directly from CSV using DuckDB
    # Use auto-inference for columns
    conn.execute(f"CREATE OR REPLACE TABLE restaurants AS SELECT * FROM read_csv_auto('{csv_file}')")

    return True

@st.cache_data
def get_restaurants(awards=None):
    """
    Fetch restaurants based on Award filter.
    awards: List of strings (e.g., ['3 Stars', '2 Stars'])
    """
    conn = get_db_connection()

    if awards and len(awards) > 0:
        # Format list for SQL IN clause
        awards_str = ", ".join([f"'{a}'" for a in awards])
        query = f"SELECT * FROM restaurants WHERE Award IN ({awards_str})"
    else:
        # Return none if no awards selected to prevent massive rendering
        query = "SELECT * FROM restaurants WHERE 1=0"

    return conn.execute(query).df()

@st.cache_data
def get_unique_awards():
    conn = get_db_connection()
    query = "SELECT DISTINCT Award FROM restaurants WHERE Award IS NOT NULL"
    df = conn.execute(query).df()
    return df['Award'].tolist()
