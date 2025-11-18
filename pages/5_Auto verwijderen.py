import streamlit as st
import sqlite3
from pathlib import Path

# Pagina instellingen
st.set_page_config(page_title="Auto verwijderen", page_icon="🗑️🚗", layout="centered")
st.title("Auto verwijderen uit de voorraad")

DB_PATH = Path(__file__).parent / "auto_data.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

# Stijl (CSS) – zelfde stijl als bij zoeken/toevoegen
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

# Invoer kenteken
kenteken_input = st.text_input("Welk kenteken wilt u verwijderen?").upper()

if "auto_data" not in st.session_state:
    st.session_state.auto_data = None

if st.button("Zoek auto"):
    if not kenteken_input:
        st.warning("Vul eerst een kenteken in.")
    else:
        cur.execute("SELECT * FROM auto_voorraad WHERE Kenteken = ?", (kenteken_input,))
        result = cur.fetchall()

        if not result:
            st.session_state.auto_data = None
            st.error(f"Ingevoerde kenteken: {kenteken_input} is niet gevonden in de database.")
        else:
            # Kolomnamen en data
            columns = [desc[0] for desc in cur.description]
            data = dict(zip(columns, result[0]))
            st.session_state.auto_data = data

# Als er een auto is gevonden, tonen we alle gegevens ter bevestiging
if st.session_state.auto_data:
    data = st.session_state.auto_data

    st.markdown("### Gegevens van het te verwijderen voertuig")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"<h3>{data.get('Merk', 'Onbekend')} {data.get('Model', '')}</h3>",
        unsafe_allow_html=True
    )
    for key, value in data.items():
        st.markdown(f"<p><b>{key}:</b> {value}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"⚠️ Weet u zeker dat u kenteken **{data.get('Kenteken', '')}** wilt verwijderen?"
    )

    bevestiging = st.checkbox("Ja, ik wil dit kenteken definitief verwijderen")

    if st.button("Definitief verwijderen"):
        if not bevestiging:
            st.warning("Vink eerst de bevestiging aan voordat u verwijdert.")
        else:
            try:
                cur.execute(
                    "DELETE FROM auto_voorraad WHERE Kenteken = ?",
                    (data.get("Kenteken"),)
                )
                conn.commit()
                st.success(f"Kenteken {data.get('Kenteken')} is verwijderd!")
                st.session_state.auto_data = None
            except sqlite3.Error as e:
                st.error(f"Database fout, kon kenteken niet verwijderen: {e}")
