from streamlit import streamlit as st

st.title("Welkom voorraad beheer v.1.0")

import streamlit as st
import sqlite3
from pathlib import Path
import requests

# Pagina instellingen
st.set_page_config(page_title="Auto toevoegen", page_icon="➕🚗", layout="centered")
st.title("Nieuwe auto toevoegen op kenteken")

DB_PATH = Path(__file__).parent / "auto_data.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

# Stijl (CSS) – zelfde stijl als zoekscherm
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

# Functie om te controleren of kenteken al bestaat
def controleer_kenteken(kenteken: str) -> int:
    cur.execute("SELECT COUNT(*) FROM auto_voorraad WHERE Kenteken = ?", (kenteken,))
    result = cur.fetchone()
    return result[0] if result else 0

# RDW API urls
BASE_URL = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"
BASE_URL_BRANDSTOF = "https://opendata.rdw.nl/resource/8ys7-d773.json"

# Invoer
kenteken_input = st.text_input("Kenteken invoeren").upper()

if st.button("Auto toevoegen"):
    if not kenteken_input:
        st.warning("Vul eerst een kenteken in.")
    else:
        kenteken = kenteken_input.replace(" ", "").upper()

        # Check of kenteken al in de database staat
        if controleer_kenteken(kenteken) > 0:
            st.error(f"Kenteken {kenteken} bestaat al in de auto voorraad.")
        else:
            params = {"kenteken": kenteken}

            try:
                response = requests.get(BASE_URL, params=params)
                response_brandstof = requests.get(BASE_URL_BRANDSTOF, params=params)

                response.raise_for_status()
                response_brandstof.raise_for_status()

                gegevens = response.json()
                gegevens_2 = response_brandstof.json()

                if not gegevens:
                    st.error(f"Geen voertuiggegevens gevonden voor kenteken {kenteken}.")
                else:
                    # Basisgegevens
                    merk_api = gegevens[0].get("merk")
                    model_api = gegevens[0].get("handelsbenaming")
                    kleur_api = gegevens[0].get("eerste_kleur")
                    bouwjaar_api = gegevens[0].get("datum_eerste_toelating_dt")[:4]
                    catalogus_prijs_api = gegevens[0].get("catalogusprijs")
                    aantal_zitplaatsen_api = gegevens[0].get("aantal_zitplaatsen")

                    # Brandstof (kan soms ontbreken)
                    brandstof_api = None
                    if gegevens_2:
                        brandstof_api = gegevens_2[0].get("brandstof_omschrijving")

                    # Waarden normaliseren / fallback
                    Merk = (merk_api or "Onbekend").capitalize()
                    Model = (model_api or "").capitalize()
                    Kleur = (kleur_api or "Onbekend").capitalize()
                    Bouwjaar = bouwjaar_api or "Onbekend"
                    Nieuw_prijs = catalogus_prijs_api or "Onbekend"
                    Brandstof = (brandstof_api or "Onbekend").capitalize()
                    aantal_zitplaats = aantal_zitplaatsen_api or "Onbekend"
                    Registratie_land = "NL"  # RDW -> standaard NL

                    try:
                        cur.execute(
                            "INSERT INTO auto_voorraad VALUES (?,?,?,?,?,?,?,?,?)",
                            (
                                kenteken,
                                Merk,
                                Model,
                                Kleur,
                                Bouwjaar,
                                Nieuw_prijs,
                                Brandstof,
                                aantal_zitplaats,
                                Registratie_land,
                            ),
                        )
                        conn.commit()

                        st.success(f"Voertuig {kenteken} is toegevoegd aan de voorraad.")

                        # Mooie kaart tonen met gegevens
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown(f"<h3>{Merk} {Model}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Kenteken:</b> {kenteken}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Kleur:</b> {Kleur}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Bouwjaar:</b> {Bouwjaar}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Nieuwprijs:</b> {Nieuw_prijs}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Brandstof:</b> {Brandstof}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Aantal zitplaatsen:</b> {aantal_zitplaats}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><b>Registratieland:</b> {Registratie_land}</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    except sqlite3.IntegrityError as e:
                        st.error(f"Database fout, kan geen gegevens opslaan: {e}")

            except requests.exceptions.RequestException as e:
                st.error(f"Fout bij het ophalen van gegevens van RDW: {e}")
