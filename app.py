import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")

st.title("🎮 Tic-Tac-Toe AI")
st.markdown("Play against an unbeatable AI 🤖")

# ---------- SESSION STATE ----------
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
    st.session_state.game_over = False
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}

board = st.session_state.board

# ---------- FUNCTIONS ----------
def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
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
col1, col2, col3 = st.columns(3)
col1.metric("Player ❌", st.session_state.score["X"])
col2.metric("AI ⭕", st.session_state.score["O"])
col3.metric("Draw 🤝", st.session_state.score["Draw"])

st.divider()

# ---------- GAME STATUS ----------
winner = check_winner(board)

if winner:
    st.success(f"🎉 {winner} wins!")
elif is_draw(board):
    st.warning("It's a Draw!")
else:
    st.info("Your turn ❌")

# ---------- BOARD UI ----------
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
                elif is_draw(board):
                    st.session_state.score["Draw"] += 1
                    st.session_state.game_over = True
                else:
                    ai = ai_move()
                    board[ai] = "O"

                    winner = check_winner(board)
                    if winner:
                        st.session_state.score[winner] += 1
                        st.session_state.game_over = True
                    elif is_draw(board):
                        st.session_state.score["Draw"] += 1
                        st.session_state.game_over = True

# ---------- CONTROLS ----------
st.divider()

col1, col2 = st.columns(2)

if col1.button("🔄 Restart Game", use_container_width=True):
    st.session_state.board = [" "] * 9
    st.session_state.game_over = False

if col2.button("🗑 Reset Score", use_container_width=True):
    st.session_state.score = {"X": 0, "O": 0, "Draw": 0}
