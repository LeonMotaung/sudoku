def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()
    print()

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # empty cell
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0  # backtrack
                return False
    return True

# Example 9x9 Sudoku board (0 = empty cell)
sudoku_board = [
    [5, 0, 0, 1, 0, 0, 0, 0, 6],
    [0, 1, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 8, 9, 0, 2, 0, 5, 0],
    
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 8, 1, 6, 0, 0],
    [4, 8, 1, 3, 5, 0, 2, 9, 7],
    
    [1, 9, 0, 0, 0, 0, 4, 6, 2],
    [0, 4, 3, 2, 1, 5, 8, 7, 9],
    [8, 0, 0, 0, 9, 0, 3, 0, 5]
]


print("Sudoku Puzzle:")
print_board(sudoku_board)

if solve(sudoku_board):
    print("Solved Sudoku:")
    print_board(sudoku_board)
else:
    print("No solution exists.")
