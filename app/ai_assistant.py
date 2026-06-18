import os
import json
import re

import requests
import pandas as pd
import plotly.express as px
import streamlit as st

from data import (
    load_data,
    get_restaurants,
    get_unique_awards,
    get_db_connection,
    get_config,
)
from theme import apply_theme

# Shared Michelin Guide colour palette (applied first; page CSS below refines it)
apply_theme()

# ============================================================
#  Luxury dark theme (shared with the other pages)
# ============================================================
st.markdown("""
<style>
.stApp { background: #050505; }
.block-container { max-width: 1500px; }
.michelin-hero {
    position: relative;
    padding: 60px 50px;
    border-radius: 20px;
    background-image: linear-gradient(to right, rgba(0,0,0,0.92) 35%, rgba(0,0,0,0.05) 80%), url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1470&auto=format&fit=crop');
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    color: white;
    margin-bottom: 35px;
    min-height: 260px;
    display: flex;
    align-items: center;
    overflow: hidden;
    border: 1px solid #1a1a1a;
}
.michelin-hero-content { position: relative; z-index: 2; max-width: 760px; }
.michelin-hero-meta {
    font-size: 11px; font-weight: 700; letter-spacing: 2px;
    color: #ffffff; margin-bottom: 15px; text-transform: uppercase;
}
.brand-michelin {
    font-family: 'Georgia', serif !important; font-size: 48px !important;
    font-weight: 900 !important; letter-spacing: 2px !important;
    line-height: 1.1 !important; color: #ffffff !important; margin: 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.brand-guide {
    font-family: 'Georgia', serif !important; font-size: 36px !important;
    font-weight: 400 !important; font-style: italic !important;
    letter-spacing: 4px !important; line-height: 1.1 !important;
    color: #BD1B21 !important; margin: 5px 0 0 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.stars-gold { color: #D4AF37 !important; font-size: 18px !important; margin-top: 10px; letter-spacing: 5px; }
.section-title {
    font-weight: 700; color: #ffffff; margin: 15px 0; font-family: 'Georgia', serif !important;
}
div.stButton > button {
    background-color: #BD1B21 !important; color: #ffffff !important;
    border: 1px solid #991014 !important; border-radius: 8px !important;
    padding: 8px 18px !important; font-weight: 600 !important;
    letter-spacing: 1px !important; transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    background-color: #e60028 !important; box-shadow: 0 4px 15px rgba(189,27,33,0.4) !important;
}
[data-testid="stChatMessage"] {
    background-color: #0c0c0c !important;
    border: 1px solid rgba(212,175,55,0.18) !important;
    border-radius: 14px !important;
}
/* Readable light text on the dark background (Streamlit defaults to dark slate) */
[data-testid="stChatMessage"],
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] td,
[data-testid="stChatMessage"] th,
[data-testid="stChatMessage"] blockquote {
    color: #ededed !important;
}
[data-testid="stChatMessage"] strong { color: #ffffff !important; }
[data-testid="stChatMessage"] a { color: #6db4ff !important; text-decoration: underline; }
[data-testid="stChatMessage"] a:hover { color: #9fd0ff !important; }
/* Caption / helper text and table borders */
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {
    color: #b8b8b8 !important;
}
[data-testid="stChatMessage"] th, [data-testid="stChatMessage"] td {
    border-color: rgba(255,255,255,0.15) !important;
}
/* Chat input — keep the dark theme and make typed text readable */
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
    background-color: #050505 !important;
}
[data-testid="stChatInput"] {
    background-color: #050505 !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    background-color: #0c0c0c !important;
    border: 1px solid rgba(212, 175, 55, 0.25) !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    padding-left: 14px !important;
    padding-right: 6px !important;
}
[data-testid="stChatInput"] textarea {
    color: #ededed !important;
    -webkit-text-fill-color: #ededed !important;
    background-color: transparent !important;
    caret-color: #ededed !important;
    padding: 12px 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #8a8a8a !important;
    -webkit-text-fill-color: #8a8a8a !important;
}
/* Send button */
[data-testid="stChatInput"] button {
    background-color: transparent !important;
    color: #D4AF37 !important;
}
[data-testid="stChatInput"] button svg { fill: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  Hero
# ============================================================
st.markdown("""
<div class="michelin-hero">
    <div class="michelin-hero-content">
        <div class="michelin-hero-meta">DATA-GROUNDED CULINARY ASSISTANT <span style="color:#BD1B21;">• GOOGLE GEMINI</span></div>
        <h1 class="brand-michelin">MICHELIN GUIDE</h1>
        <h1 class="brand-guide">Ask the Sommelier AI</h1>
        <div class="stars-gold">★ ★ ★</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  Load the integrated dataset into DuckDB
# ============================================================
sf_passcode = st.session_state.get("snowflake_passcode")
with st.spinner("Loading Michelin Guide Dataset..."):
    load_data(snowflake_passcode=sf_passcode)

all_awards = get_unique_awards()
df = get_restaurants(awards=all_awards)

if df is None or df.empty:
    st.error("No data found or failed to load data.")
    st.stop()

# ------------------------------------------------------------
#  Enrich City / Country / District (the raw table leaves them
#  empty — the real geography lives inside the Location column).
# ------------------------------------------------------------
if 'City' not in df.columns or df['City'].isnull().all() or 'Country' not in df.columns or df['Country'].isnull().all():
    location_split = df['Location'].astype(str).str.split(', ', n=1, expand=True)
    df['City'] = location_split[0]
    df['Country'] = location_split[1].fillna('Unknown') if location_split.shape[1] > 1 else 'Unknown'
else:
    df['City'] = df['City'].fillna('Unknown')
    df['Country'] = df['Country'].fillna('Unknown')

# Register an enriched, AI-queryable table in the same DuckDB connection.
AI_TABLE = "restaurants_ai"
conn = get_db_connection()
conn.register("ai_df_view", df)
conn.execute(f"CREATE OR REPLACE TABLE {AI_TABLE} AS SELECT * FROM ai_df_view")


# ============================================================
#  Build the schema "knowledge" the model learns the DB from
# ============================================================
@st.cache_data(show_spinner=False)
def build_schema_context(table_name, row_count):
    """Describe the table + real categorical values so the model knows the data."""
    c = get_db_connection()
    schema_rows = c.execute(f"DESCRIBE {table_name}").df()
    columns = list(zip(schema_rows['column_name'], schema_rows['column_type']))

    def distinct(col, limit=40):
        try:
            vals = c.execute(
                f"SELECT DISTINCT \"{col}\" FROM {table_name} "
                f"WHERE \"{col}\" IS NOT NULL AND \"{col}\" <> '' LIMIT {limit}"
            ).df()[col].tolist()
            return [str(v) for v in vals]
        except Exception:
            return []

    awards = distinct("Award")
    countries = distinct("Country", 60)
    prices = distinct("Price", 20)
    cities = distinct("City", 40)

    lines = [f"Table name: {table_name}", f"Total rows: {row_count}", "", "Columns:"]
    for name, typ in columns:
        lines.append(f"  - \"{name}\" ({typ})")
    lines.append("")
    lines.append(f"Distinct Award values: {awards}")
    lines.append(f"Distinct Price tier strings (currency symbols, e.g. €€€ / $$$ / ¥¥): {prices}")
    lines.append(f"Sample City values: {cities}")
    lines.append(f"Sample Country values: {countries}")
    lines.append("")
    lines.append(
        "Notes: 'Award' holds the Michelin distinction (e.g. '3 Stars', '2 Stars', "
        "'1 Star', 'Bib Gourmand', 'Selected Restaurants'). The 'City' and 'Country' columns are "
        "POPULATED — to filter by city or country ALWAYS use them with ILIKE (e.g. "
        "WHERE City ILIKE '%Tokyo%'), and do NOT pattern-match the 'Location' string. 'Location' is "
        "just a display field formatted 'City, Country'. 'Url' links to the official Michelin Guide "
        "page. 'Cuisine' may contain several comma-separated cuisines. 'Description' has prose."
    )
    return "\n".join(lines)


ROW_COUNT = conn.execute(f"SELECT COUNT(*) FROM {AI_TABLE}").fetchone()[0]
SCHEMA_CONTEXT = build_schema_context(AI_TABLE, ROW_COUNT)

st.caption(f"🍽️ Connected to **{ROW_COUNT:,}** Michelin Guide records. For data questions the AI runs a real SQL query; general questions are answered conversationally.")

# ============================================================
#  Google Gemini helpers (OpenAI-compatible endpoint)
# ============================================================
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|COPY|PRAGMA|INSTALL|LOAD|EXPORT|REPLACE|TRUNCATE|GRANT)\b",
    re.IGNORECASE,
)


def call_gemini(messages, api_key, model, temperature=0.2, max_tokens=1200):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=90)
    if resp.status_code == 429:
        raise RuntimeError(
            "Gemini rate limit reached (free tier). Please wait a minute and try again, "
            "or use a model/key with higher quota."
        )
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")
    data = resp.json()
    if not isinstance(data, dict) or not data.get("choices"):
        raise RuntimeError(f"Unexpected Gemini response: {resp.text[:300]}")
    return data["choices"][0]["message"]["content"]


def extract_sql(text):
    """Pull a SQL statement out of the model's (possibly fenced/JSON) reply."""
    text = text.strip()
    # ```sql ... ``` fence (closed or unterminated, e.g. truncated output)
    fence = re.search(r"```(?:sql)?\s*(.+?)```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    open_fence = re.search(r"```(?:sql)?\s*(.+)$", text, re.DOTALL | re.IGNORECASE)
    if open_fence:
        return open_fence.group(1).strip()
    # {"sql": "..."}
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and obj.get("sql"):
            return str(obj["sql"]).strip()
    except Exception:
        pass
    return text


def sanitize_sql(sql):
    """Allow a single read-only SELECT only; enforce a LIMIT."""
    sql = sql.strip().rstrip(";").strip()
    if not re.match(r"^\s*(SELECT|WITH)\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")
    if ";" in sql:
        raise ValueError("Only a single statement is allowed.")
    if FORBIDDEN_SQL.search(sql):
        raise ValueError("Query contains a forbidden keyword.")
    if not re.search(r"\bLIMIT\s+\d+\b", sql, re.IGNORECASE):
        sql = f"{sql}\nLIMIT 50"
    return sql


MAX_QUERIES = 5


def extract_json(text):
    """Pull a JSON object out of the model reply (fenced or bare)."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL | re.IGNORECASE)
    candidate = fence.group(1) if fence else None
    if candidate is None:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        candidate = m.group(0) if m else None
    if candidate is None:
        return None
    try:
        return json.loads(candidate)
    except Exception:
        return None


def plan_query(question, history_summary, api_key, model):
    """One call that routes AND (for data questions) plans MULTIPLE queries.

    Returns ('chat', []) for conversational questions, or ('data', [{label, sql}, ...])
    — one or several complementary angles — so the answer can be multi-dimensional.
    Still only one API call (the queries themselves run locally on DuckDB for free).
    """
    system = (
        "You are the planning step of a Michelin Guide analyst backed by a DuckDB table of "
        "~19,000 restaurants. Look at the user's latest message and respond with ONLY a JSON object "
        "inside a ```json code fence.\n\n"
        "If the message is general knowledge or conversation that does NOT need database rows (what a "
        "Michelin star means, criteria, dining etiquette, general advice, greetings, thanks, or a "
        "clarification answerable from the conversation), respond:\n"
        '{\"mode\": \"chat\"}\n\n'
        "Otherwise respond with a set of read-only DuckDB SELECT queries that, TOGETHER, let you give "
        "a thorough multi-dimensional answer:\n"
        '{\"mode\": \"data\", \"queries\": [{\"label\": \"short description\", \"sql\": \"SELECT ...\"}, ...]}\n\n'
        "How many queries:\n"
        "- A simple lookup/recommendation needs just 1 query.\n"
        "- An ANALYTICAL question ('what is X known for', 'analyze', 'compare', 'overview of', "
        "'เด่นเรื่องอะไร', 'ภาพรวม', 'วิเคราะห์') should use 2-5 complementary queries covering "
        "DIFFERENT angles, e.g.: (a) cuisine breakdown with award tiers, (b) the top starred "
        "restaurants themselves, (c) price-level distribution, (d) neighbourhood/district concentration, "
        "(e) comparison vs other relevant cities. Choose angles that fit the question.\n"
        f"- Use at most {MAX_QUERIES} queries.\n\n"
        "SQL rules:\n"
        "- Query only the described table and columns. One single SELECT per query.\n"
        "- Every query in the set MUST cover a DIFFERENT angle — never repeat the same query.\n"
        "- To COMPARE several named groups (e.g. multiple cities/countries/cuisines), write ONE query "
        "that GROUPs BY that dimension and returns all groups as rows (e.g. SELECT City, COUNT(*)... "
        "GROUP BY City) — do NOT emit a separate query per group. This keeps results comparable and chartable.\n"
        "- To filter by city or country, use the City / Country columns with ILIKE "
        "(e.g. WHERE City ILIKE '%Tokyo%'). Do NOT pattern-match the Location string.\n"
        "- Use case-insensitive ILIKE with '%...%' for text/cuisine filters too.\n"
        "- For 'best'/'top', order Award: '3 Stars' > '2 Stars' > '1 Star' > 'Bib Gourmand' > 'Selected Restaurants'.\n"
        "- For award-tier breakdowns use: COUNT(*) AS total, "
        "SUM(CASE WHEN Award='3 Stars' THEN 1 ELSE 0 END) AS three_star, "
        "SUM(CASE WHEN Award='2 Stars' THEN 1 ELSE 0 END) AS two_star, "
        "SUM(CASE WHEN Award='1 Star' THEN 1 ELSE 0 END) AS one_star, "
        "SUM(CASE WHEN Award='Bib Gourmand' THEN 1 ELSE 0 END) AS bib.\n"
        "- When listing actual restaurants to recommend, SELECT: Name, Award, Cuisine, Price, Location, "
        "\"FacilitiesAndServices\", PhoneNumber, WebsiteUrl, Url; otherwise include at least Name, Award, "
        "Cuisine, Location, Url.\n"
        "- Always add a LIMIT (<= 50) to every query.\n\n"
        f"DATABASE SCHEMA:\n{SCHEMA_CONTEXT}"
    )
    user = question
    if history_summary:
        user = f"Earlier conversation (for context):\n{history_summary}\n\nCurrent message: {question}"
    raw = call_gemini(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key, model, temperature=0.0, max_tokens=2500,
    )
    obj = extract_json(raw)
    if obj and str(obj.get("mode", "")).lower() == "chat":
        return "chat", []
    queries = []
    if obj and isinstance(obj.get("queries"), list):
        for q in obj["queries"][:MAX_QUERIES]:
            sql = (q or {}).get("sql")
            if not sql:
                continue
            try:
                queries.append({"label": (q.get("label") or "Query").strip(), "sql": sanitize_sql(sql)})
            except ValueError:
                continue
    # Fallbacks if JSON planning failed.
    if not queries:
        stripped = raw.strip()
        if re.search(r"\bCHAT\b", stripped, re.IGNORECASE) and not re.search(r"(SELECT|WITH)\b", stripped, re.IGNORECASE):
            return "chat", []
        queries = [{"label": "Query", "sql": sanitize_sql(extract_sql(raw))}]
    return "data", queries


def run_query_set(queries):
    """Execute each planned query locally; capture df or error per query."""
    conn = get_db_connection()
    executed = []
    for q in queries:
        try:
            df = conn.execute(q["sql"]).df()
            executed.append({"label": q["label"], "sql": q["sql"], "df": df, "error": None})
        except Exception as e:
            executed.append({"label": q["label"], "sql": q["sql"], "df": None, "error": str(e)})
    return executed


def repair_failed(question, executed, api_key, model):
    """One API call to fix any queries that errored; returns corrected {label: sql}."""
    failed = [e for e in executed if e["error"]]
    if not failed:
        return {}
    listing = "\n\n".join(
        f"Label: {e['label']}\nSQL:\n{e['sql']}\nError: {e['error']}" for e in failed
    )
    system = (
        "You fix broken DuckDB SELECT queries. Return ONLY a JSON object in a ```json fence mapping "
        'each label to a corrected single read-only SELECT query: {\"<label>\": \"SELECT ...\"}. '
        "Keep the same intent; add a LIMIT (<= 50).\n\n"
        f"DATABASE SCHEMA:\n{SCHEMA_CONTEXT}"
    )
    user = f"User question: {question}\n\nFix these failed queries:\n{listing}"
    raw = call_gemini(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key, model, temperature=0.0, max_tokens=1500,
    )
    obj = extract_json(raw) or {}
    fixed = {}
    for label, sql in obj.items():
        try:
            fixed[label] = sanitize_sql(str(sql))
        except (ValueError, TypeError):
            continue
    return fixed


def answer_from_results(question, executed, api_key, model):
    """Synthesize a multi-dimensional answer from one or more query result sets."""
    blocks = []
    for e in executed:
        if e["error"]:
            blocks.append(f"### {e['label']}\n(query failed: {e['error']})")
            continue
        df = e["df"]
        if df is None or df.empty:
            body = "(no rows)"
        else:
            body = df.head(30).to_csv(index=False)
        blocks.append(f"### {e['label']}\nSQL: {e['sql']}\nResult (CSV, up to 30 rows):\n{body}")
    results_text = "\n\n".join(blocks) if blocks else "(no data)"

    system = (
        "You are an elegant, knowledgeable Michelin Guide analyst. You are given the user's question "
        "and the results of SEVERAL database queries, each under a '### label' heading. Synthesize "
        "ONE cohesive answer that draws on ALL the result sets together — do NOT just dump each "
        "query. Cross-reference the angles (volume vs quality, top venues, prices, neighbourhoods, "
        "comparisons) and give a clear, structured takeaway with headings/bullets where helpful.\n"
        "Use ONLY facts present in the results — never invent restaurants, awards, counts, or prices. "
        "Reply in the SAME language as the user's question. When you mention a restaurant that has a "
        "Url, hyperlink its name as [Name](Url). If all results are empty, say so politely and suggest "
        "how to refine the question.\n\n"
        "QUALITATIVE QUESTIONS: If the user asks what a place is 'known for' / 'notable for' / 'best "
        "at' / Thai 'เด่น'/'ขึ้นชื่อ', weigh BOTH quality (number of 3/2/1-Star and Bib Gourmand "
        "venues) AND volume, and explain the reasoning (e.g. 'X has the most restaurants overall, but "
        "Y stands out for prestige with the most starred venues'). Give a balanced verdict.\n\n"
        "BOOKING GUIDANCE: When you recommend or list specific restaurants, add a short, practical "
        "booking note for each, INFERRED ONLY from the available fields — be explicit that real-time "
        "availability is NOT in the data. Heuristics:\n"
        "- '3 Stars'/'2 Stars' or expensive Price (€€€€ / $$$$): 'Reserve well in advance (often weeks ahead)'.\n"
        "- '1 Star': 'Booking recommended'.\n"
        "- 'Bib Gourmand'/'Selected Restaurants', or FacilitiesAndServices with 'Counter dining', "
        "'Cash only', or 'Credit cards not accepted': likely casual/walk-in — 'Often walk-in; call "
        "ahead for peak times' and mention 'cash only' if present.\n"
        "- Surface useful tips from FacilitiesAndServices (Cash only, Shoes must be removed, Bring your "
        "own bottle, Valet parking). Give PhoneNumber and/or hyperlink [Website](WebsiteUrl) when present. "
        "Do NOT claim a table is available or unavailable.\n"
        "Keep each restaurant's note to one short line. Do NOT build a morning/afternoon/evening day "
        "itinerary — that is handled by the separate Trip Planner page."
    )
    user = f"User question: {question}\n\nQuery results:\n{results_text}"
    return call_gemini(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key, model, temperature=0.3, max_tokens=2000,
    )


def answer_directly(question, history_summary, api_key, model):
    """Conversational answer that does NOT query the database."""
    system = (
        "You are an elegant, knowledgeable Michelin Guide concierge. You also have access to a "
        "database of ~19,000 restaurants, but you are NOT querying it for this message — answer "
        "conversationally from general knowledge and the conversation so far. Reply in the SAME "
        "language as the user. Be concise and well formatted with markdown.\n"
        "IMPORTANT: Do NOT invent specific restaurant names, exact counts, prices, or statistics. "
        "If the user actually wants specific restaurants or numbers from the data, briefly invite "
        "them to ask (e.g. 'ask me to list 2-star sushi in Tokyo and I'll pull it from the data')."
    )
    user = question
    if history_summary:
        user = f"Conversation so far:\n{history_summary}\n\nUser: {question}"
    return call_gemini(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        api_key, model, temperature=0.5, max_tokens=1200,
    )


# ============================================================
#  API key / model configuration
# ============================================================
env_api_key = get_config("GEMINI_API_KEY", "")
model = get_config("GEMINI_MODEL", "gemini-2.5-flash")

api_key = env_api_key
if not env_api_key:
    api_key = st.text_input(
        "Enter Google Gemini API Key", type="password",
        help="Get a free key at https://aistudio.google.com/apikey. Or set GEMINI_API_KEY in your env/secrets.",
    )

with st.expander("💡 Example questions"):
    st.markdown(
        "- How many 3-star restaurants are there, and which countries have the most?\n"
        "- What are the most common cuisines among 1-star restaurants in France?\n"
        "- แนะนำร้าน 2 ดาวในโตเกียว 3 ร้าน **ร้านไหนควรจองล่วงหน้า และจองยังไง**\n"
        "- มีร้าน Bib Gourmand ในกรุงเทพฯ ร้านไหนรับเงินสดอย่างเดียว / วอล์กอินได้\n"
        "- _ถามทั่วไปก็ได้:_ ดาว Michelin คืออะไร ต่างจาก Bib Gourmand ยังไง"
    )

# ============================================================
#  Rendering helpers (charts + a shared assistant-message renderer)
# ============================================================
# Columns that are identifiers/coordinates, not meaningful chart measures.
_NON_CHART_COLS = {"url", "websiteurl", "latitude", "longitude", "phonenumber", "id"}
_MAX_CHARTS = 3


def render_result_charts(queries):
    """Render a bar chart for each chartable query result (categorical x + numeric y)."""
    charted = 0
    for q in queries:
        if charted >= _MAX_CHARTS:
            break
        df = q.get("table")
        if df is None or df.empty:
            continue
        num_cols = [c for c in df.columns
                    if pd.api.types.is_numeric_dtype(df[c]) and str(c).lower() not in _NON_CHART_COLS]
        cat_cols = [c for c in df.columns
                    if c not in num_cols and str(c).lower() not in _NON_CHART_COLS]
        if not num_cols:
            continue

        fig = None
        show_legend = True
        try:
            if cat_cols and len(df) >= 2:
                # Multi-row: categories on x, numeric measures as grouped bars (legend needed).
                # For many rows, chart only the top 15 by the primary measure (table keeps all).
                plot_df = df.sort_values(num_cols[0], ascending=False).head(15) if len(df) > 15 else df
                fig = px.bar(plot_df, x=cat_cols[0], y=num_cols[:4], barmode="group", template="plotly_dark")
            elif len(df) == 1 and len(num_cols) >= 2:
                # Single-row metrics (e.g. award-tier counts): melt the columns into bars.
                # The x-axis already names each metric, so no legend needed.
                row = df.iloc[0]
                mdf = pd.DataFrame({"metric": num_cols, "value": [row[c] for c in num_cols]})
                fig = px.bar(mdf, x="metric", y="value", template="plotly_dark",
                             color="metric", color_discrete_sequence=px.colors.sequential.YlOrRd)
                show_legend = False
        except Exception:
            fig = None
        if fig is None:
            continue

        fig.update_layout(
            paper_bgcolor="#0c0c0c", plot_bgcolor="#0c0c0c", font_color="#ededed",
            margin=dict(l=10, r=10, t=40, b=10), height=320,
            legend_title_text="", legend=dict(orientation="h", y=1.15), showlegend=show_legend,
        )
        st.caption(f"📊 {q.get('label', 'Chart')}")
        st.plotly_chart(fig, width='stretch', key=f"chart_{id(q)}_{charted}")
        charted += 1


def render_assistant_body(content, queries):
    """Render an assistant turn: answer text, auto charts, and the SQL/data expander."""
    st.markdown(content, unsafe_allow_html=True)
    if queries:
        render_result_charts(queries)
        with st.expander(f"🔎 {len(queries)} quer{'y' if len(queries) == 1 else 'ies'} used + data"):
            for q in queries:
                label = q.get("label", "Query")
                err = q.get("error")
                st.caption(label + ("" if not err else f"  ·  ⚠️ {err}"))
                if q.get("sql"):
                    st.code(q["sql"], language="sql")
                if q.get("table") is not None:
                    st.dataframe(q["table"], width='stretch')


# ============================================================
#  Chat
# ============================================================
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []
if "ai_cache" not in st.session_state:
    st.session_state.ai_cache = {}

for msg in st.session_state.ai_messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_assistant_body(msg["content"], msg.get("queries"))
        else:
            st.markdown(msg["content"], unsafe_allow_html=True)

prompt = st.chat_input("Ask about the Michelin Guide data…")

if prompt:
    st.session_state.ai_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            st.error("Please provide a Google Gemini API Key (env/secrets or the field above).")
            st.stop()

        # Compact history for follow-up context (last few turns)
        history_summary = "\n".join(
            f"{m['role']}: {m['content'][:300]}" for m in st.session_state.ai_messages[-5:-1]
        )
        # Cache by the question text alone (not history) so re-asking the exact same
        # question reuses the answer — history always grows, so including it would never hit.
        cache_key = prompt.strip().lower()

        try:
            cached = st.session_state.ai_cache.get(cache_key)
            if cached is not None:
                # Identical question + context already answered this session — no API calls.
                st.caption("⚡ Reused a cached answer")
                render_assistant_body(cached["content"], cached.get("queries"))
                st.session_state.ai_messages.append(dict(cached))
            else:
                with st.spinner("Thinking…"):
                    route, queries = plan_query(prompt, history_summary, api_key, model)

                if route == "chat":
                    # Conversational / general-knowledge answer — no SQL.
                    with st.spinner("Composing the answer…"):
                        answer = answer_directly(prompt, history_summary, api_key, model)
                    message = {"role": "assistant", "content": answer}
                else:
                    with st.spinner(f"Running {len(queries)} quer{'y' if len(queries) == 1 else 'ies'} against the database…"):
                        executed = run_query_set(queries)
                        # One repair pass for any queries that errored.
                        if any(e["error"] for e in executed):
                            fixed = repair_failed(prompt, executed, api_key, model)
                            for e in executed:
                                if e["error"] and e["label"] in fixed:
                                    try:
                                        e["sql"] = fixed[e["label"]]
                                        e["df"] = get_db_connection().execute(e["sql"]).df()
                                        e["error"] = None
                                    except Exception as re_err:
                                        e["error"] = str(re_err)

                    with st.spinner("Analyzing the results…"):
                        answer = answer_from_results(prompt, executed, api_key, model)

                    message = {
                        "role": "assistant",
                        "content": answer,
                        "queries": [
                            {"label": e["label"], "sql": e["sql"], "table": e["df"], "error": e["error"]}
                            for e in executed
                        ],
                    }

                render_assistant_body(message["content"], message.get("queries"))
                st.session_state.ai_messages.append(message)
                st.session_state.ai_cache[cache_key] = message
        except Exception as e:
            err = f"Sorry, I couldn't answer that. {e}"
            st.error(err)
            st.session_state.ai_messages.append({
                "role": "assistant", "content": err,
            })
