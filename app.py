import streamlit as st
from google.cloud import firestore
import os

# Pagina configuratie
st.set_page_config(
    page_title="ClubChessApp - Trainer Dashboard",
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
            if username == "pieter" and password == "schaak123":
                st.session_state.logged_in = True
                st.success("Succesvol ingelogd!")
                st.rerun()
            else:
                st.error("Onjuiste gebruikersnaam of wachtwoord.")

# --- PAGINA'S VAN HET DASHBOARD ---

def page_dashboard():
    st.header("📊 Dashboard Overzicht")
    st.write("Welkom in het centrale beheerdersdashboard van de ClubChessApp.")
    
    # Statusblokken
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Actieve Leerlingen", value="--")
    with col2:
        st.metric(label="Beschikbare Stappen", value="Stap 1 t/m 6")
    with col3:
        status_db = "🟢 Verbonden" if db else "🔴 Niet verbonden"
        st.metric(label="Database Status", value=status_db)

    st.divider()

    # Database verbindingstest
    st.subheader("Database Verbindingstest")
    if db:
        st.success("Verbinding met Google Cloud Firestore is actief!")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Testbericht opslaan in Firestore"):
                doc_ref = db.collection("test_collectie").document("welkom")
                doc_ref.set({
                    "bericht": "Hallo vanuit Streamlit en Firebase!",
                    "status": "Succesvol gekoppeld"
                })
                st.info("Testbericht opgeslagen in de database!")
        with col_btn2:
            if st.button("Laat testbericht zien"):
                doc_ref = db.collection("test_collectie").document("welkom")
                doc = doc_ref.get()
                if doc.exists:
                    st.write("Ontvangen uit Firestore:", doc.to_dict())
                else:
                    st.warning("Nog geen testbericht gevonden.")
    else:
        st.error("Kan geen verbinding maken met de database. Controleer 'service-account.json'.")

def page_stappenmethode():
    st.header("📚 Stappenmethode Curriculum")
    st.write("Beheer hier de lessen, thema's en opgaven per Stap.")
    
    stap_keuze = st.selectbox(
        "Kies een Stap om te bekijken of te bewerken:",
        ["Stap 1", "Stap 2", "Stap 3", "Stap 4", "Stap 5", "Stap 6"]
    )
    
    tab1, tab2 = st.tabs(["📖 Lessen & Theorie", "🧩 Opgaven & Oefeningen"])
    with tab1:
        st.subheader(f"Lessen voor {stap_keuze}")
        st.info(f"Hier komen de lessen en theorie-onderdelen van {stap_keuze}.")
    with tab2:
        st.subheader(f"Opgaven voor {stap_keuze}")
        st.info(f"Hier kunnen straks opgaves en schaakpuzzels voor {stap_keuze} worden toegevoegd.")

def page_gebruikersbeheer():
    st.header("👥 Gebruikersbeheer")
    st.write("Overzicht en beheer van leerlingen en trainers.")
    
    tab_lijst, tab_nieuw = st.tabs(["📋 Leerlingenlijst", "➕ Nieuwe Leerling Toevoegen"])
    with tab_lijst:
        st.info("Binnenkort verschijnt hier de lijst met geregistreerde leerlingen en hun voortgang.")
    with tab_nieuw:
        with st.form("nieuwe_gebruiker_form"):
            naam = st.text_input("Naam leerling")
            stap = st.selectbox("Huidige Stap", ["Stap 1", "Stap 2", "Stap 3", "Stap 4", "Stap 5", "Stap 6"])
            opslaan = st.form_submit_button("Leerling Opslaan")
            if opslaan:
                st.success(f"Leerling '{naam}' ingedeeld bij {stap} (Mockup function)!")

def page_instellingen():
    st.header("⚙️ Instellingen")
    st.write("Systeeminstellingen en accountbeheer.")
    st.info("Hier komen in de toekomst instellingen voor beheerders en applicatie-opties.")

# --- HOOFDNAVIGATIE ---

def show_main_app():
    # Sidebar Navigatie
    st.sidebar.title("♟️ ClubChessApp")
    st.sidebar.write("Welkom, beheerder!")
    st.sidebar.divider()
    
    menu_keuze = st.sidebar.radio(
        "Navigatie",
        ["📊 Dashboard", "📚 Stappenmethode", "👥 Gebruikersbeheer", "⚙️ Instellingen"]
    )
    
    st.sidebar.divider()
    if st.sidebar.button("Uitloggen (Afmelden)"):
        st.session_state.logged_in = False
        st.rerun()

    # Pagina weergave op basis van selectie
    if menu_keuze == "📊 Dashboard":
        page_dashboard()
    elif menu_keuze == "📚 Stappenmethode":
        page_stappenmethode()
    elif menu_keuze == "👥 Gebruikersbeheer":
        page_gebruikersbeheer()
    elif menu_keuze == "⚙️ Instellingen":
        page_instellingen()

# --- HOOFDLOGICA ---

if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()