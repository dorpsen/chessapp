import chess
import chess.svg
import streamlit as st

st.set_page_config(page_title="Python Chess Opening Trainer", page_icon="♟️")
st.title("♟️ Opening Trainer")

# 1. Voorbeeld van openingsrepertoire (dit kun je uitbreiden of uit PGN's laden)
OPENINGS = {
    "Siciliaans (1. e4 c5)": ["e4", "c5"],
    "Frans (1. e4 e6)": ["e4", "e6"],
    "Spaans (1. e4 e5 2. Nf3 Nc6 3. Bb5)": ["e4", "e5", "Nf3", "Nc6", "Bb5"],
}

# 2. Selectie van de opening
selected_opening = st.selectbox("Kies een opening om te trainen:", list(OPENINGS.keys()))
target_moves = OPENINGS[selected_opening]

# 3. Initialiseer de staat van het bord en de voortgang
if "board" not in st.session_state or st.session_state.get("current_opening") != selected_opening:
    st.session_state.board = chess.Board()
    st.session_state.move_index = 0
    st.session_state.current_opening = selected_opening
    st.session_state.feedback = ""

board = st.session_state.board

# 4. Toon het schaakbord via de ingebouwde SVG van python-chess
board_svg = chess.svg.board(board=board, size=400)
st.image(board_svg, use_container_width=False)

# 5. Trainingslogica
if st.session_state.move_index < len(target_moves):
    expected_move = target_moves[st.session_state.move_index]
    
    st.write(f"**Stap {st.session_state.move_index + 1} van {len(target_moves)}**")
    
    # Als de computer aan de beurt is in het scenario, doe de zet automatisch
    if board.turn == chess.BLACK and expected_move:
        board.push_san(expected_move)
        st.session_state.move_index += 1
        st.rerun()

    # Veld voor de speler om zijn zet in te voeren
    user_move = st.text_input("Jouw zet (bijv. e4, Nf3, c5):", key=f"input_{st.session_state.move_index}")

    if st.button("Verstuur Zet"):
        try:
            parsed_move = board.parse_san(user_move)
            
            # Controleer of de zet klopt met het gekozen repertoire
            if user_move == expected_move:
                board.push(parsed_move)
                st.session_state.move_index += 1
                st.session_state.feedback = "✅ Goed zo! Dat is de juiste openingzet."
                st.rerun()
            else:
                st.error(f"❌ Fout! Dat is niet de verwachte zet in deze opening. Probeer opnieuw.")
        except Exception:
            st.error("Ongeldige schaaknotatie. Typ bijvoorbeeld 'e4' of 'Nf6'.")

else:
    st.success("🎉 Gefeliciteerd! Je hebt de variant succesvol afgerond.")

# Feedback-melding weergeven
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# Reset knop
if st.button("Opnieuw beginnen"):
    st.session_state.board = chess.Board()
    st.session_state.move_index = 0
    st.session_state.feedback = ""
    st.rerun()