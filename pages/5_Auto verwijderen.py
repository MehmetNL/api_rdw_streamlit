import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from versie_def import versie_info

versie_info()

st.set_page_config(page_title="Auto's verwijderen", layout="centered")
st.title("🚗 Auto's verwijderen uit de database")

# --- Databaseverbinding (zelfde DB als in je script) ---
DB_PATH = (Path(__file__).parent / "auto_data.db").resolve()

@st.cache_resource
def get_conn():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database niet gevonden op: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def zoek_autos_op_deel_kenteken(fragment: str):
    fragment = fragment.upper().strip()
    if not fragment:
        return []

    conn = get_conn()
    cur = conn.cursor()
    # Zoekt alle kentekens waar het fragment in voorkomt (case-insensitive)
    cur.execute(
