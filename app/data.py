import os
import duckdb
import pandas as pd
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize session state for mock data alerts if not already set
if st.runtime.exists():
    if 'using_mock_data' not in st.session_state:
        st.session_state.using_mock_data = False
    if 'db_error_message' not in st.session_state:
        st.session_state.db_error_message = None

def get_config(key, default=None):
    """Retrieves configuration from st.secrets first, then environment variables."""
    if st.runtime.exists():
        try:
            if key in st.secrets:
                return st.secrets[key]
        except StreamlitSecretNotFoundError:
            pass
    return os.getenv(key, default)



@st.cache_resource
def get_db_connection():
    """Returns an in-memory DuckDB connection."""
    conn = duckdb.connect(':memory:')
    return conn

def normalize_columns(df):
    """Ensures DataFrame column headers match standard PascalCase Michelin Guide schema."""
    if df is None or df.empty:
        return df

    standard_cols = {
        'name': 'Name',
        'address': 'Address',
        'location': 'Location',
        'minprice': 'MinPrice',
        'maxprice': 'MaxPrice',
        'currency': 'Currency',
        'cuisine': 'Cuisine',
        'longitude': 'Longitude',
        'latitude': 'Latitude',
        'phonenumber': 'PhoneNumber',
        'url': 'Url',
        'award': 'Award',
        'price': 'Price',
        'facilitiesandservices': 'FacilitiesAndServices',
        'city': 'City',
        'state': 'State',
        'country': 'Country',
        'district': 'District',
        'pricelevel': 'PriceLevel',
        'stars': 'Stars'
    }

    df = df.copy()
    new_cols = {}
    for col in df.columns:
        col_lower = str(col).lower().replace('_', '').replace(' ', '')
        if col_lower in standard_cols:
            new_cols[col] = standard_cols[col_lower]

    df.rename(columns=new_cols, inplace=True)

    # Ensure all standard columns are present
    for col in standard_cols.values():
        if col not in df.columns:
            df[col] = None

    return df

def fetch_mysql():
    """Connects to MySQL and queries the restaurants table."""
    import pymysql

    host = get_config("MYSQL_HOST")
    port = int(get_config("MYSQL_PORT", 3306))
    user = get_config("MYSQL_USER")
    password = get_config("MYSQL_PASSWORD")
    database = get_config("MYSQL_DATABASE")
    table = get_config("MYSQL_TABLE", "restaurants")

    if not user or user == "your_mysql_user" or "placeholder" in user:
        raise ValueError("MySQL credentials are not configured or contain placeholder values.")

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=3
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            return pd.DataFrame(rows)
    finally:
        conn.close()

def fetch_mongodb():
    """Connects to MongoDB and queries the restaurants collection."""
    from pymongo import MongoClient

    uri = get_config("MONGODB_URI")
    db_name = get_config("MONGODB_DATABASE")
    collection_name = get_config("MONGODB_COLLECTION", "restaurants")

    if not uri or "localhost:27017" in uri and not db_name:
        raise ValueError("MongoDB collection/database is not configured.")

    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    try:
        client.server_info() # Check connection
        db = client[db_name]
        collection = db[collection_name]
        cursor = collection.find({}, {"_id": 0})
        rows = list(cursor)
        return pd.DataFrame(rows)
    finally:
        client.close()

def fetch_snowflake(passcode=None):
    """Connects to Snowflake and queries the restaurants table."""
    import snowflake.connector

    user = get_config("SNOWFLAKE_USER")
    password = get_config("SNOWFLAKE_PASSWORD")
    account = get_config("SNOWFLAKE_ACCOUNT")
    warehouse = get_config("SNOWFLAKE_WAREHOUSE")
    database = get_config("SNOWFLAKE_DATABASE")
    schema = get_config("SNOWFLAKE_SCHEMA", "public")
    table = get_config("SNOWFLAKE_TABLE", "restaurants")

    role = get_config("SNOWFLAKE_ROLE")

    if not user or user == "your_snowflake_user" or "placeholder" in user:
        raise ValueError("Snowflake credentials are not configured or contain placeholder values.")

    authenticator = get_config("SNOWFLAKE_AUTHENTICATOR")

    conn_params = {
        "user": user,
        "password": password,
        "account": account,
        "warehouse": warehouse,
        "database": database,
        "schema": schema,
        "login_timeout": 5
    }
    if authenticator:
        conn_params["authenticator"] = authenticator
    if passcode:
        conn_params["passcode"] = passcode
    elif get_config("SNOWFLAKE_PASSCODE"):
        conn_params["passcode"] = get_config("SNOWFLAKE_PASSCODE")
    if role:
        conn_params["role"] = role

    conn = snowflake.connector.connect(**conn_params)
    try:
        cursor = conn.cursor()
        if role:
            cursor.execute(f"USE ROLE {role}")
        if warehouse:
            cursor.execute(f"USE WAREHOUSE {warehouse}")
        if database:
            cursor.execute(f"USE DATABASE {database}")
        if schema:
            cursor.execute(f"USE SCHEMA {schema}")
        cursor.execute(f"SELECT * FROM {table}")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()

def get_credentials_hash(db_type):
    """Generates a hash of the environment variables to handle cache invalidation."""
    if db_type == 'mysql':
        keys = ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE", "MYSQL_TABLE"]
    elif db_type == 'mongodb':
        keys = ["MONGODB_URI", "MONGODB_DATABASE", "MONGODB_COLLECTION"]
    elif db_type == 'snowflake':
        keys = ["SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD", "SNOWFLAKE_ACCOUNT", "SNOWFLAKE_WAREHOUSE", "SNOWFLAKE_DATABASE", "SNOWFLAKE_SCHEMA", "SNOWFLAKE_TABLE", "SNOWFLAKE_ROLE"]
    else:
        return ""
    return "|".join([str(get_config(k, "")) for k in keys])

@st.cache_data(show_spinner=False)
def fetch_raw_data(db_type, credentials_hash, passcode=None):
    """Cached raw database fetching based on selected db_type."""
    if db_type == "mysql":
        return fetch_mysql()
    elif db_type == "mongodb":
        return fetch_mongodb()
    elif db_type == "snowflake":
        return fetch_snowflake(passcode=passcode)
    else:
        raise ValueError(f"Unsupported DB_TYPE: '{db_type}'")

@st.cache_data(show_spinner=False)
def fetch_kagglehub_data():
    """Downloads and reads the Kagglehub dataset, caching the result."""
    import kagglehub
    path = kagglehub.dataset_download("ngshiheng/michelin-guide-restaurants-2021")
    csv_file = os.path.join(path, "michelin_my_maps.csv")
    return pd.read_csv(csv_file)

def load_data(snowflake_passcode=None):
    """
    Primary data loading function. Fetches data from all configured databases
    (MySQL, MongoDB, Snowflake), merges and deduplicates the results,
    and registers the resulting dataset into DuckDB. Stores status of each DB.
    """
    # Reload environment variables from .env to pick up any changes without restarting Streamlit
    load_dotenv(override=True)
    conn = get_db_connection()
    in_streamlit = st.runtime.exists()

    # Generate hashes for cache validation
    mysql_hash = get_credentials_hash('mysql')
    mongodb_hash = get_credentials_hash('mongodb')
    snowflake_hash = get_credentials_hash('snowflake')
    if snowflake_passcode:
        snowflake_hash += f"|{snowflake_passcode}"

    # Combined hash to check if we can reuse already loaded data
    combined_hash = f"{mysql_hash}|{mongodb_hash}|{snowflake_hash}"

    if in_streamlit and st.session_state.get('data_loaded') and st.session_state.get('loaded_credentials_hash') == combined_hash:
        try:
            tables = conn.execute("SHOW TABLES").fetchall()
            if any(t[0] == 'restaurants' for t in tables):
                return True
        except Exception:
            pass

    # Initialize status dict and update UI to loading all databases in parallel
    db_statuses = {
        'mysql': {'status': 'loading', 'rows': 0, 'error': None},
        'mongodb': {'status': 'loading', 'rows': 0, 'error': None},
        'snowflake': {'status': 'loading', 'rows': 0, 'error': None},
        'kagglehub': {'status': 'idle', 'rows': 0, 'error': None}
    }
    if in_streamlit:
        st.session_state.db_statuses = db_statuses
        update_db_status_ui()

    successful_dfs = {}

    # Fetch data sources in parallel using ThreadPoolExecutor
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(fetch_raw_data, 'mysql', mysql_hash): 'mysql',
            executor.submit(fetch_raw_data, 'mongodb', mongodb_hash): 'mongodb',
            executor.submit(fetch_raw_data, 'snowflake', snowflake_hash, passcode=snowflake_passcode): 'snowflake'
        }

        for future in concurrent.futures.as_completed(futures):
            db_key = futures[future]
            try:
                df = future.result()
                if df is not None and not df.empty:
                    df = normalize_columns(df)
                    df['SourceDB'] = db_key.capitalize() if db_key != 'mongodb' else 'MongoDB'
                    successful_dfs[db_key] = df
                    db_statuses[db_key] = {'status': 'success', 'rows': len(df), 'error': None}
                else:
                    db_statuses[db_key] = {'status': 'failed', 'rows': 0, 'error': "Returned empty dataset"}
            except Exception as e:
                db_statuses[db_key] = {'status': 'failed', 'rows': 0, 'error': str(e)}

            # Update UI immediately after each datasource finishes its job
            if in_streamlit:
                st.session_state.db_statuses = db_statuses
                update_db_status_ui()

    # Check if any database connection failed
    any_db_failed = any(db_statuses[db_key]['status'] == 'failed' for db_key in ['mysql', 'mongodb', 'snowflake'])

    # Merge successful dataframes only if all databases succeeded
    df = None
    if not any_db_failed and successful_dfs:
        try:
            # Select column groups for each database
            mysql_cols = ['Url', 'Name', 'Address', 'Location', 'Price', 'Cuisine', 'Longitude', 'Latitude', 'Award']
            mongodb_cols = ['Url', 'PhoneNumber', 'FacilitiesAndServices']
            snowflake_cols = ['Url', 'City', 'State', 'Country', 'District', 'Currency', 'PriceLevel', 'Stars']

            # Find all unique URLs across successful dataframes
            urls = pd.concat([sdf[['Url']] for sdf in successful_dfs.values()], ignore_index=True).drop_duplicates()
            df = urls.copy()

            # 1. MySQL Column Group
            df_mysql_part = None
            if 'mysql' in successful_dfs:
                # Retrieve from MySQL dataframe
                df_mysql_part = successful_dfs['mysql'][[c for c in mysql_cols if c in successful_dfs['mysql'].columns]]
            else:
                # Fallback: recover MySQL columns from MongoDB or Snowflake
                for alt_key in ['mongodb', 'snowflake']:
                    if alt_key in successful_dfs:
                        df_mysql_part = successful_dfs[alt_key][[c for c in mysql_cols if c in successful_dfs[alt_key].columns]]
                        break
            if df_mysql_part is not None:
                df = pd.merge(df, df_mysql_part.drop_duplicates(subset=['Url']), on='Url', how='left')

            # 2. MongoDB Column Group
            df_mongo_part = None
            if 'mongodb' in successful_dfs:
                # Retrieve from MongoDB dataframe
                df_mongo_part = successful_dfs['mongodb'][[c for c in mongodb_cols if c in successful_dfs['mongodb'].columns]]
            else:
                # Fallback: recover MongoDB columns from MySQL or Snowflake
                for alt_key in ['mysql', 'snowflake']:
                    if alt_key in successful_dfs:
                        df_mongo_part = successful_dfs[alt_key][[c for c in mongodb_cols if c in successful_dfs[alt_key].columns]]
                        break
            if df_mongo_part is not None:
                df = pd.merge(df, df_mongo_part.drop_duplicates(subset=['Url']), on='Url', how='left')

            # 3. Snowflake Column Group
            df_snowflake_part = None
            if 'snowflake' in successful_dfs:
                # Retrieve from Snowflake dataframe
                df_snowflake_part = successful_dfs['snowflake'][[c for c in snowflake_cols if c in successful_dfs['snowflake'].columns]]
            else:
                # Fallback: recover Snowflake columns from MySQL or MongoDB
                for alt_key in ['mysql', 'mongodb']:
                    if alt_key in successful_dfs:
                        df_snowflake_part = successful_dfs[alt_key][[c for c in snowflake_cols if c in successful_dfs[alt_key].columns]]
                        break
            if df_snowflake_part is not None:
                df = pd.merge(df, df_snowflake_part.drop_duplicates(subset=['Url']), on='Url', how='left')

            # Combine SourceDB indicator (indicates all successful backends where the record existed)
            # Since data is merged column-wise, this represents the integration status
            successful_sources = sorted([display_name.capitalize() if display_name != 'mongodb' else 'MongoDB' for display_name in successful_dfs.keys()])
            df['SourceDB'] = ", ".join(successful_sources)

            if in_streamlit:
                st.session_state.using_mock_data = False
                st.session_state.db_error_message = None
        except Exception as merge_err:
            db_statuses['merge_error'] = str(merge_err)

    # Fallback if no databases succeeded or any database failed
    if df is None or df.empty:
        # Update kagglehub to loading status
        db_statuses['kagglehub'] = {'status': 'loading', 'rows': 0, 'error': None}
        if in_streamlit:
            st.session_state.db_statuses = db_statuses
            update_db_status_ui()

        try:
            df = fetch_kagglehub_data()
            df = normalize_columns(df)
            df['SourceDB'] = 'Kagglehub (Fallback)'
            db_statuses['kagglehub'] = {'status': 'success', 'rows': len(df), 'error': None}
            if in_streamlit:
                st.session_state.using_mock_data = True
                failed_dbs = [name for name, info in db_statuses.items() if info['status'] == 'failed' and name != 'kagglehub']
                st.session_state.db_error_message = f"Database connection error or failure ({', '.join(failed_dbs)}). Loaded fallback Kagglehub data."
        except Exception as kh_err:
            db_statuses['kagglehub'] = {'status': 'failed', 'rows': 0, 'error': str(kh_err)}
            if in_streamlit:
                st.session_state.using_mock_data = True
                st.session_state.db_error_message = f"All databases and Kagglehub fallback failed. {str(kh_err)}"
            raise RuntimeError(f"All databases and Kagglehub fallback failed: {str(kh_err)}") from kh_err
        finally:
            if in_streamlit:
                st.session_state.db_statuses = db_statuses
                update_db_status_ui()

    # Cast coordinate columns to float
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')

    # Load into in-memory DuckDB table
    conn.register('df_view', df)
    conn.execute("CREATE OR REPLACE TABLE restaurants AS SELECT * FROM df_view")

    # Set loaded state flags
    if in_streamlit:
        st.session_state.data_loaded = True
        st.session_state.loaded_credentials_hash = combined_hash
        st.session_state.db_statuses = db_statuses
    return True

@st.cache_data
def get_restaurants(awards=None):
    """Fetch restaurants based on Award filter from DuckDB."""
    conn = get_db_connection()
    if awards and len(awards) > 0:
        awards_str = ", ".join([f"'{a}'" for a in awards])
        query = f"SELECT * FROM restaurants WHERE Award IN ({awards_str})"
    else:
        query = "SELECT * FROM restaurants WHERE 1=0"
    return conn.execute(query).df()

@st.cache_data
def get_unique_awards():
    """Fetch unique awards present in the database from DuckDB."""
    conn = get_db_connection()
    query = "SELECT DISTINCT Award FROM restaurants WHERE Award IS NOT NULL"
    df = conn.execute(query).df()
    return df['Award'].tolist()

def update_db_status_ui():
    """Renders and updates the database integration status panel in real-time."""
    if not st.runtime.exists():
        return

    db_statuses = st.session_state.get('db_statuses', {
        'mysql': {'status': 'idle', 'rows': 0, 'error': None},
        'mongodb': {'status': 'idle', 'rows': 0, 'error': None},
        'snowflake': {'status': 'idle', 'rows': 0, 'error': None},
        'kagglehub': {'status': 'idle', 'rows': 0, 'error': None}
    })

    # Official brand icons (colored SVGs) from Simple Icons
    db_details = {
        'mysql': {
            'name': 'MySQL',
            'icon': '<img src="https://cdn.simpleicons.org/mysql/4479A1" width="16" style="margin-right: 8px;" />'
        },
        'mongodb': {
            'name': 'MongoDB',
            'icon': '<img src="https://cdn.simpleicons.org/mongodb/47A248" width="16" style="margin-right: 8px;" />'
        },
        'snowflake': {
            'name': 'Snowflake',
            'icon': '<img src="https://cdn.simpleicons.org/snowflake/29B5E8" width="16" style="margin-right: 8px;" />'
        },
        'kagglehub': {
            'name': 'Kagglehub',
            'icon': '<img src="https://cdn.simpleicons.org/kaggle/20BEFF" width="16" style="margin-right: 8px;" />'
        }
    }

    status_html = '<div class="db-status-container">'

    for db_key, display in db_details.items():
        info = db_statuses.get(db_key, {'status': 'idle', 'rows': 0, 'error': None})
        status = info['status']
        error = info['error']

        if status == 'success':
            badge_class = 'badge-success'
            badge_text = 'Connected'
            if db_key == 'kagglehub':
                badge_text = 'Active Fallback'
        elif status == 'failed':
            badge_class = 'badge-failed'
            badge_text = 'Offline'
        elif status == 'loading':
            badge_class = 'badge-idle'
            badge_text = 'Connecting...'
        else:
            badge_class = 'badge-idle'
            badge_text = 'Idle'

        status_html += f"""
        <div class="db-status-card">
            <div class="db-status-header">
                <span class="db-status-name">{display['icon']} {display['name']}</span>
                <span class="db-status-badge {badge_class}">{badge_text}</span>
            </div>
        """
        if error:
            clean_error = str(error).replace('<', '&lt;').replace('>', '&gt;')
            status_html += f'<div class="db-status-error" title="{clean_error}">{clean_error}</div>'

        status_html += '</div>'

    status_html += '</div>'

    # Write to container if it exists in session state
    container = st.session_state.get('db_status_container')
    if container:
        container.markdown(status_html, unsafe_allow_html=True)

    # Check if Snowflake has a TOTP/MFA error and render warning/input in warning container
    warning_container = st.session_state.get('db_warning_container')
    if warning_container:
        warning_container.empty()
        sf_status = db_statuses.get('snowflake', {})
        sf_error = sf_status.get('error', '') if sf_status else ''
        if sf_error and ("TOTP" in str(sf_error) or "MFA" in str(sf_error) or "passcode" in str(sf_error).lower()):
            with warning_container.container():
                st.warning("❄️ Snowflake requires a TOTP passcode.")
                totp_input = st.text_input("Enter Snowflake TOTP Passcode", type="password", key="sf_totp_widget")
                if st.button("Connect with TOTP", key="sf_totp_submit"):
                    if totp_input:
                        st.session_state.snowflake_passcode = totp_input
                        st.session_state.data_loaded = False
                        st.rerun()
