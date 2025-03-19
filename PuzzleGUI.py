import tkinter as tk
from tkinter import messagebox, simpledialog
from Tiles import Tiles
import random


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.resizable(False, False)
        self.board = None
        self.initial_board = None
        self.tiles = None
        self.move_history = []
        self.move_count = 0
        self.nodes_expanded = 0
        if not self.get_user_input():
            self.root.destroy()
            return
        self.create_widgets()
        self.update_board()
        self.update_moves_display()

    def get_user_input(self):
        user_input = simpledialog.askstring("Input", "Enter 9 space-separated numbers (0-8) or type 'random':")
        if not user_input:
            return False
        if user_input.lower() == "random":
            self.board = list(range(9))
            random.shuffle(self.board)
        else:
            try:
                self.board = list(map(int, user_input.split()))
                if len(self.board) != 9 or sorted(self.board) != list(range(9)):
                    raise ValueError
            except:
                messagebox.showerror("Error", "Invalid input. Enter numbers 0-8 exactly once.")
                return self.get_user_input()
        self.initial_board = self.board[:]
        self.tiles = Tiles(self.board)
        return True

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, columnspan=4)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.frame, text="", width=5, height=2, font=("Arial", 24))
            btn.grid(row=i // 3, column=i % 3)
            btn.bind("<Button-1>", self.create_move_tile_callback(i))
            self.buttons.append(btn)

        self.solve_bfs_button = tk.Button(self.root, text="Solve with BFS", command=self.solve_bfs)
        self.solve_bfs_button.grid(row=1, column=0)

        self.solve_astar_button = tk.Button(self.root, text="Solve with A*", command=self.solve_astar)
        self.solve_astar_button.grid(row=1, column=1)

        self.play_button = tk.Button(self.root, text="Solve by Yourself", command=self.reset_game)
        self.play_button.grid(row=1, column=2)

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=1, column=3)

        self.show_moves_button = tk.Button(self.root, text="Show Moves", command=self.show_moves_popup)
        self.show_moves_button.grid(row=2, column=0, columnspan=4)

        self.instructions_button = tk.Label(self.root, text="Instructions", font=("Arial", 14), fg="blue",
                                            cursor="hand2")
        self.instructions_button.grid(row=3, column=0, columnspan=4)
        self.instructions_button.bind("<Button-1>", self.show_instructions)

        self.move_count_label = tk.Label(self.root, text="Move Count: 0", font=("Arial", 14))
        self.move_count_label.grid(row=4, column=0, columnspan=4)

    def show_instructions(self, event=None):
        instructions = (
            "How to Play:\n"
            "- The goal is to arrange the tiles in numerical order with the empty space at the top-left.\n"
            "- You can move tiles by clicking on a tile adjacent to the empty space.\n"
            "- The game ends when the board matches (zero is the empty tile): \n"
            "  0 1 2 \n  3 4 5 \n  6 7 8 \n"
            "- Use the Solve buttons to see solutions or try solving it yourself!\n"
            "- On the Show Moves button you will see the path from the initial state"
            "  to the goal state.the nodes expanded will point on how many node were"
            "  expanded by the algorithm during the process."
        )
        messagebox.showinfo("Instructions", instructions)

    def reset_game(self):
        self.board = self.initial_board[:]
        self.tiles = Tiles(self.board)
        self.move_history = []
        self.update_board()
        self.update_moves_display()

    def new_game(self):
        if not self.get_user_input():
            self.root.destroy()
            return
        self.move_history = []
        self.update_board()
        self.update_moves_display()

    def create_move_tile_callback(self, index):
        def callback(event):
            self.move_tile(index)

        return callback

    def move_tile(self, index):
        empty_index = self.board.index(0)
        if index in self.tiles.moves_states[empty_index]:
            self.board[empty_index], self.board[index] = self.board[index], self.board[empty_index]
            self.move_history.append(self.board[empty_index])
            self.update_board()
            self.update_moves_display()
            if self.board == list(self.tiles.end_state):
                messagebox.showinfo("Success", "Puzzle Solved!")

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=str(self.board[i]) if self.board[i] != 0 else "")

    def update_moves_display(self):
        self.move_count_label.config(text=f"Move Count: {len(self.move_history)}")

    def show_moves_popup(self):
        moves_text = " -> ".join(map(str, self.move_history)) if self.move_history else "No moves made yet."
        messagebox.showinfo("Moves History", f"Nodes Expanded: {self.nodes_expanded}\nMoves: {moves_text}")

    def solve(self, algorithm):
        self.reset_game()
        self.nodes_expanded, path = algorithm()
        if self.nodes_expanded == -1:
            messagebox.showerror("Error", "No solution found")
            return
        self.move_history = []
        self.animate_solution(path)

    def solve_bfs(self):
        self.solve(self.tiles.bfs)

    def solve_astar(self):
        self.solve(self.tiles.a_star)

    def animate_solution(self, path):
        for i, move in enumerate(path):
            self.root.after(500 * (i + 1), lambda m=move: self.move_tile_animated(m))

    def move_tile_animated(self, move):
        empty_index = self.board.index(0)
        move_index = self.board.index(move)
        self.board[empty_index], self.board[move_index] = self.board[move_index], self.board[empty_index]
        self.move_history.append(move)
        self.update_board()
        self.update_moves_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
