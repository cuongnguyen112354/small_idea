import tkinter as tk
from tkinter import messagebox

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.entries = [[tk.Entry(root, width=3, font=('Arial', 18), justify='center') for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].grid(row=row, column=col, padx=5, pady=5)

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=3)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        clear_button.grid(row=9, column=3, columnspan=3)

        quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        quit_button.grid(row=9, column=6, columnspan=3)

    def solve(self):
        board = self.get_board()
        if self.solve_sudoku(board):
            self.set_board(board)
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists")

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.entries[row][col].get()
                if value == '':
                    current_row.append(0)
                else:
                    current_row.append(int(value))
            board.append(current_row)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if board[row][col] != 0:
                    self.entries[row][col].insert(0, board[row][col])

    def solve_sudoku(self, board):
        empty = self.find_empty_location(board)
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0

        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, board, row, col, num):
        return (self.is_row_safe(board, row, num) and
                self.is_col_safe(board, col, num) and
                self.is_box_safe(board, row - row % 3, col - col % 3, num))

    def is_row_safe(self, board, row, num):
        return not any(board[row][i] == num for i in range(9))

    def is_col_safe(self, board, col, num):
        return not any(board[i][col] == num for i in range(9))

    def is_box_safe(self, board, box_start_row, box_start_col, num):
        return not any(board[i][j] == num for i in range(box_start_row, box_start_row + 3) for j in range(box_start_col, box_start_col + 3))


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
