nodes_count = 0

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

def alphabeta(board, depth, alpha, beta, is_max):
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
                best = max(best, alphabeta(board, depth+1, alpha, beta, False))
                board[i] = ""
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, alphabeta(board, depth+1, alpha, beta, True))
                board[i] = ""
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

def alphabeta_move(board):
    global nodes_count
    nodes_count = 0
    best_val = -100
    move = -1

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            move_val = alphabeta(board, 0, -100, 100, False)
            board[i] = ""

            if move_val > best_val:
                move = i
                best_val = move_val

    return move, nodes_count
