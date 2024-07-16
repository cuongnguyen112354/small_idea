class Solver:
   def __init__(self, board):
      self.board = board

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