import streamlit as st
from google.cloud import firestore
import os

# Pagina configuratie
st.set_page_config(
    page_title="ClubChessApp",
    page_icon="♟️",
    layout="wide"
)

# 1. Initialiseer de inlogstatus in Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. Functie om verbinding te maken met Firestore
@st.cache_resource
def init_firestore():
    json_path = "service-account.json"
    if not os.path.exists(json_path):
        return None
    try:
        db = firestore.Client.from_service_account_json(json_path)
        return db
    except Exception as e:
        st.error(f"Fout bij verbinden met Firestore: {e}")
        return None

db = init_firestore()

def show_login_page():
    st.title("♟️ ClubChessApp - Beveiligde Ingang")
    st.write("Log in om toegang te krijgen tot het platform.")
    
    with st.form("login_form"):
        username = st.text_input("Gebruikersnaam")
        password = st.text_input("Wachtwoord", type="password")
        submit_button = st.form_submit_button("Inloggen")
        
        if submit_button:
            # Tijdelijke inloggegevens (kun je later koppelen aan Firestore)
            if username == "pieter" and password == "schaak123":
                st.session_state.logged_in = True
                st.success("Succesvol ingelogd!")
                st.rerun()
            else:
                st.error("Onjuiste gebruikersnaam of wachtwoord.")

def show_main_app():
    # Sidebar voor navigatie en uitloggen
    st.sidebar.title("Navigatie")
    st.sidebar.write("Welkom, beheerder!")
    
    if st.sidebar.button("Uitloggen (Afmelden)"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("♟️ ClubChessApp - Dashboard")
    st.write("Welkom in de beveiligde omgeving van de schaaktraining.")
    
    # Database verbindingstest widget
    if db:
        st.success("Verbinding met Google Cloud Firestore is actief!")
        
        if st.button("Testbericht opslaan in Firestore"):
            doc_ref = db.collection("test_collectie").document("welkom")
            doc_ref.set({
                "bericht": "Hallo vanuit Streamlit en Firebase!",
                "status": "Succesvol gekoppeld"
            })
            st.info("Testbericht opgeslagen in de database!")

        if st.button("Laat testbericht zien"):
            doc_ref = db.collection("test_collectie").document("welkom")
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                st.write("Ontvangen uit Firestore:", data)
            else:
                st.warning("Nog geen testbericht gevonden. Klik eerst op opslaan!")
    else:
                st.error("Kan geen verbinding maken met de database. Controleer of 'service-account.json' aanwezig is.")

# 3. Logica om te bepalen of het inlogscherm of de app getoond wordt
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()