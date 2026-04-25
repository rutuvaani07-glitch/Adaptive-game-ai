nodes_count = 0

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

def minimax(board, is_max):
    global nodes_count
    nodes_count += 1

    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif "" not in board:
        return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, False))
                board[i] = ""
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, True))
                board[i] = ""
        return best

def minimax_move(board):
    global nodes_count
    nodes_count = 0
    best_val = -100
    move = -1

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            move_val = minimax(board, False)
            board[i] = ""

            if move_val > best_val:
                move = i
                best_val = move_val

    return move, nodes_count
