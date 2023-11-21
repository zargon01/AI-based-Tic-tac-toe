import tkinter as tk

# Function to check if a player has won
def check_win(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Function to check if the board is full
def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

# Function to handle player's move
def player_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        update_button(row, col)
        if check_win(board, 'X'):
            result_label.config(text="Player wins!")
        elif is_full(board):
            result_label.config(text="It's a draw!")
        else:
            ai_move()

# Function to handle AI's move
def ai_move():
    best_move, _ = minimax(board, 'O', 'O', -float('inf'), float('inf'))
    row, col = best_move
    board[row][col] = 'O'
    update_button(row, col)
    if check_win(board, 'O'):
        result_label.config(text="AI wins!")
    elif is_full(board):
        result_label.config(text="It's a draw!")

# Minimax algorithm with alpha-beta pruning
def minimax(board, currentPlayer, aiPlayer, alpha, beta):
    if check_win(board, aiPlayer):
        return None, 1
    elif check_win(board, 'X'):
        return None, -1
    elif is_full(board):
        return None, 0

    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    best_move = None

    if currentPlayer == aiPlayer:
        best_score = -float('inf')
        for row, col in empty_cells:
            board[row][col] = currentPlayer
            _, result = minimax(board, 'X', aiPlayer, alpha, beta)
            board[row][col] = ' '
            if result > best_score:
                best_score = result
                best_move = (row, col)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
    else:
        best_score = float('inf')
        for row, col in empty_cells:
            board[row][col] = currentPlayer
            _, result = minimax(board, aiPlayer, aiPlayer, alpha, beta)
            board[row][col] = ' '
            if result < best_score:
                best_score = result
                best_move = (row, col)
            beta = min(beta, best_score)
            if beta <= alpha:
                break

    return best_move, best_score

# Function to start a new game
def new_game():
    global board
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '
            buttons[row][col].config(text=' ', state='active')
    result_label.config(text="")

# Function to update the button text
def update_button(row, col):
    buttons[row][col].config(text=board[row][col], state='disabled')

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Initialize the game board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Create buttons for the game grid with styling
buttons = [[None for _ in range(3)] for _ in range(3)]
button_font = ('Helvetica', 20, 'bold')
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text=' ', width=10, height=3, font=button_font, command=lambda r=row, c=col: player_move(r, c))
        buttons[row][col].grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10)

# Label to display the game result with styling
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# New Game button with styling
new_game_button = tk.Button(root, text="New Game", font=("Helvetica", 16), command=new_game)
new_game_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
