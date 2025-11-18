import streamlit as st
import sqlite3
from pathlib import Path

# Titel en instellingen
st.set_page_config(page_title="Auto zoeken", page_icon="🚗", layout="centered")
st.title("Auto zoeken op kenteken")

# Database
DB_PATH = Path(__file__).parent / "auto_data.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

# Stijl (CSS)
st.markdown("""
<style>
.card {
  border-radius: 14px;
  padding: 18px 20px;
  border: 1px solid rgba(150,150,150,0.15);
  background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(248,248,248,0.95));
  box-shadow: 0 4px 14px rgba(0,0,0,0.05);
  margin-top: 14px;
}
.card h3 {
  margin-bottom: 6px;
  font-size: 22px;
}
.card p {
  margin: 4px 0;
  font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# Zoekveld
kenteken = st.text_input("Kenteken")

if st.button("Zoek auto op kenteken"):
    cur.execute("SELECT * FROM auto_voorraad WHERE Kenteken = ?", (kenteken.upper(),))
    result = cur.fetchall()

    if result:
        # Kolomnamen ophalen uit de cursor
        columns = [desc[0] for desc in cur.description]
        data = dict(zip(columns, result[0]))  # Neem de eerste rij als dict

        # Mooie kaart tonen
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<h3>{data.get('Merk', 'Onbekend')} {data.get('Model', '')}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Kenteken:</b> {data.get('Kenteken', '-')}</p>", unsafe_allow_html=True)
        for key, value in data.items():
            if key not in ['Merk', 'Model', 'Kenteken']:
                st.markdown(f"<p><b>{key}:</b> {value}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning(f"Kenteken: {kenteken} niet gevonden!")
