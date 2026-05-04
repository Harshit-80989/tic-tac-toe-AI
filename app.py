import streamlit as st

# ---------- INIT ----------
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
    st.session_state.current = "X"
    st.session_state.game_over = False

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


# ---------- UI ----------
st.title("Tic-Tac-Toe AI")

cols = st.columns(3)

for i in range(9):
    if cols[i % 3].button(board[i] if board[i] != " " else "-", key=i):
        if board[i] == " " and not st.session_state.game_over:
            board[i] = "X"

            winner = check_winner(board)
            if winner:
                st.success(f"{winner} wins!")
                st.session_state.game_over = True
            elif is_draw(board):
                st.warning("Draw!")
                st.session_state.game_over = True
            else:
                ai = ai_move()
                board[ai] = "O"

                winner = check_winner(board)
                if winner:
                    st.success(f"{winner} wins!")
                    st.session_state.game_over = True
                elif is_draw(board):
                    st.warning("Draw!")
                    st.session_state.game_over = True


# ---------- RESET ----------
if st.button("Restart Game"):
    st.session_state.board = [" "] * 9
    st.session_state.current = "X"
    st.session_state.game_over = False
