from flask import Flask, render_template, request, jsonify
import tkinter as tk
from PIL import Image, ImageTk

app = Flask(__name__)

# Flask route for the home page
@app.route('/')
def index():
    return render_template("index.html")

# Flask route for making a move
@app.route('/make_move', methods=['POST'])
def make_move():
    try:
        row = int(request.form['row'])
        col = int(request.form['col'])
        board.make_move(row, col)
        return jsonify(success=True, message="Move made successfully")
    except Exception as e:
        return jsonify(success=False, message=str(e))
# Define a route to provide the initial game state
@app.route('/get_initial_game_state')
def get_initial_game_state():
    # Assuming you have a class instance representing the Tic-Tac-Toe board
    initial_game_state = {
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "currentPlayer": "X"  # Assuming "X" starts the game
    }
    return jsonify(gameState=initial_game_state)
# Tkinter-based Tic-Tac-Toe game
class Board:
    def __init__(self):
        self.image_references = []
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.draw_grid()

    def draw_grid(self):
        for i in range(1, 3):
            canvas.create_line(0, i * 100, 300, i * 100)
            canvas.create_line(i * 100, 0, i * 100, 300)

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != "":
            return
        self.board[row][col] = self.current_player
        self.draw_mark(row, col)
        self.check_game_over()
        self.switch_player()

    def draw_mark(self, row, col):
        x = col * 100 + 50
        y = row * 100 + 50

        image_path = "x_symbol.png" if self.current_player == "X" else "o_symbol.png"
        try:
            image = Image.open(image_path)
            image = image.resize((90, 90), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image)
            canvas.create_image(x, y, image=photo_image, anchor=tk.CENTER)
            self.image_references.append(photo_image)
        except Exception as e:
            print(f"Error loading image: {e}")

    def check_game_over(self):
        winner = self.check_winner()
        tie = self.is_board_full()
        if winner != "":
            self.game_over = True
            status_label.config(text=f"{winner} wins!")
            self.highlight_win()
        elif tie:
            self.game_over = True
            status_label.config(text="It's a tie!")
        else:
            status_label.config(text=f"{self.current_player}'s turn")

    def check_winner(self):
        win_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        for combination in win_combinations:
            cells = [self.board[row][col] for row, col in combination]
            if cells.count(cells[0]) == len(cells) and cells[0] != "":
                return cells[0]
        return ""

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def highlight_win(self):
        win_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        for combination in win_combinations:
            cells = [self.board[row][col] for row, col in combination]
            if cells.count(cells[0]) == len(cells) and cells[0] != "":
                x1 = min(col for row, col in combination) * 100 + 5
                y1 = min(row for row, col in combination) * 100 + 5
                x2 = (max(col for row, col in combination) + 1) * 100 - 5
                y2 = (max(row for row, col in combination) + 1) * 100 - 5
                if cells[0] == "X":
                    canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=4)
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=4)

# Tkinter GUI setup
window = tk.Tk()
window.title("Tic-Tac-Toe")
canvas = tk.Canvas(window, width=300, height=300, bg="white")
canvas.pack()
status_label = tk.Label(window, text="X's turn", font=("Helvetica", 20))
status_label.pack()

# Create an instance of the Board class
board = Board()

# Define a function to handle mouse clicks on the canvas
def handle_click(event):
    x = event.x
    y = event.y
    row = y // 100
    col = x // 100
    board.make_move(row, col)

# Bind the handle_click function to mouse clicks on the canvas
canvas.bind("<Button-1>", handle_click)

# Start the main loop
window.mainloop()

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

