import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")

# ---------- BACKGROUND ----------
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1655841439659-0afc60676b70?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* Dark overlay for readability */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: -1;
        }

        /* Button styling */
        div.stButton > button {
            height: 80px;
            font-size: 24px;
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ---------- TITLE ----------
st.title("🎮 Tic-Tac-Toe AI")
st.caption("Play against an unbeatable AI 🤖")

# ---------- SESSION STATE ----------
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "score" not in st.session_state:
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}

board = st.session_state.board

# ---------- GAME LOGIC ----------
def check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None

def is_draw(board):
    return " " not in board

def minimax(board, is_max):
    winner = check_winner(board)
    if winner == "O": return 1
    if winner == "X": return -1
    if is_draw(board): return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best = max(best, score)
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best = min(best, score)
        return best

def ai_move():
    best_score = -100
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# ---------- SCOREBOARD ----------
st.subheader("📊 Scoreboard")
c1, c2, c3 = st.columns(3)
c1.metric("Player ❌", st.session_state.score["X"])
c2.metric("AI ⭕", st.session_state.score["O"])
c3.metric("Draw 🤝", st.session_state.score["Draw"])

st.divider()

# ---------- STATUS ----------
winner = check_winner(board)

if winner:
    st.success(f"🎉 {winner} wins!")
elif is_draw(board):
    st.warning("It's a Draw!")
else:
    st.info("Your turn ❌")

# ---------- BOARD ----------
for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        label = board[idx] if board[idx] != " " else " "

        if cols[j].button(label, key=idx, use_container_width=True):
            if board[idx] == " " and not st.session_state.game_over:
                board[idx] = "X"

                winner = check_winner(board)
                if winner:
                    st.session_state.score[winner] += 1
                    st.session_state.game_over = True
                    st.rerun()

                if is_draw(board):
                    st.session_state.score["Draw"] += 1
                    st.session_state.game_over = True
                    st.rerun()

                ai = ai_move()
                if ai != -1:
                    board[ai] = "O"

                winner = check_winner(board)
                if winner:
                    st.session_state.score[winner] += 1
                    st.session_state.game_over = True
                elif is_draw(board):
                    st.session_state.score["Draw"] += 1
                    st.session_state.game_over = True

                st.rerun()

# ---------- CONTROLS ----------
st.divider()
col1, col2 = st.columns(2)

if col1.button("🔄 Restart Game", use_container_width=True):
    st.session_state.board = [" "] * 9
    st.session_state.game_over = False
    st.rerun()

if col2.button("🗑 Reset Score", use_container_width=True):
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}
    st.rerun()
