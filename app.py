from flask import Flask, render_template, request, jsonify
from minimax import minimax_move
from alphabeta import alphabeta_move
import time

app = Flask(__name__)

board = [""] * 9

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.json
    index = data["index"]
    algo = data["algo"]

    board[index] = "X"

    if algo == "minimax":
        start = time.time()
        move, nodes = minimax_move(board)
        end = time.time()
    else:
        start = time.time()
        move, nodes = alphabeta_move(board)
        end = time.time()

    if move != -1:
        board[move] = "O"

    return jsonify({
        "board": board,
        "time": end - start,
        "nodes": nodes
    })

@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = [""] * 9
    return jsonify({"board": board})

if __name__ == "__main__":
    app.run(debug=True)
