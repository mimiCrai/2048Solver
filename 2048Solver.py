import numpy as np


def printboard(board):
    for row in board:
        print("\t".join(map(str, row)))


def slide(board, direction):
    if direction == 'up':
        for i in range(4):
            for j in range(4):
                if i > 0:
                    if board[i][j] > 0:
                        tempi = i
                        while tempi > 0 and board[tempi-1][j] == 0:
                            board[tempi][j], board[tempi-1][j] = board[tempi-1][j], board[tempi][j]
                            tempi -= 1
    if direction == 'down': 
        for i in range(3, -1, -1):
            for j in range(4):
                if i < 3:
                    if board[i][j] > 0:
                        tempi = i
                        while tempi < 3 and board[tempi+1][j] == 0:
                            board[tempi][j], board[tempi+1][j] = board[tempi+1][j], board[tempi][j]
                            tempi += 1
    if direction == 'left': 
        for i in range(4):
            for j in range(4):
                if j > 0:
                    if board[i][j] > 0:
                        tempj = j
                        while tempj > 0 and board[i][tempj-1] == 0:
                            board[i][tempj], board[i][tempj-1] = board[i][tempj-1], board[i][tempj]
                            tempj -= 1
    if direction == 'right': 
        for i in range(4):
            for j in range(3, -1, -1):
                if j < 3:
                    if board[i][j] > 0:
                        tempj = j
                        while tempj < 3 and board[i][tempj+1] == 0:
                            board[i][tempj], board[i][tempj+1] = board[i][tempj+1], board[i][tempj]
                            tempj += 1
    return board


def merge_tiles(board, direction):
    if direction == 'up':
        for i in range(3):
            for j in range(4):
                if board[i][j] == board[i+1][j] and board[i][j] != 0:
                    board[i][j] *= 2
                    board[i+1][j] = 0
    if direction == 'down':
        for i in range(3, 0, -1):
            for j in range(4):
                if board[i][j] == board[i-1][j] and board[i][j] != 0:
                    board[i][j] *= 2
                    board[i-1][j] = 0
    if direction == 'left':
        for i in range(4):
            for j in range(3):
                if board[i][j] == board[i][j+1] and board[i][j] != 0:
                    board[i][j] *= 2
                    board[i][j+1] = 0
    if direction == 'right':
        for i in range(4):
            for j in range(3, 0, -1):
                if board[i][j] == board[i][j-1] and board[i][j] != 0:
                    board[i][j] *= 2
                    board[i][j-1] = 0
    return board


def move(board, direction):
    """moving board"""

    newboard = np.copy(board)
    newboard = slide(newboard, direction)
    newboard = merge_tiles(newboard, direction)
    return slide(newboard, direction)


def evaluate_board(board):
    """heuristic scoring"""

    empty_tiles = len([tile for row in board for tile in row if tile == 0])
    max_tile = np.max(board)
    return empty_tiles + max_tile


def expectimax(board, depth, is_maximizing):
    """calculates expected value"""
    if depth == 0 or game_over(board):
        return evaluate_board(board)
    if is_maximizing:
        max_eval = float('-inf')
        for direction in ['up', 'down', 'left', 'right']:
            new_board = move(board, direction)
            if not np.array_equal(board, new_board):  # Jika langkah valid
                eval = expectimax(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
        return max_eval
    else: #new tile (2 or 4)
        empty_positions = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if not empty_positions: #board is full, endgame
            return evaluate_board(board)

        total_score = 0
        for (i, j) in empty_positions:
            for value, prob in [(2, 0.9), (4, 0.1)]:
                new_board = np.copy(board)
                new_board[i][j] = value
                total_score += prob * expectimax(new_board, depth - 1, True)
        return total_score


def find_best_move(board, depth=2):
    best_move = None
    best_score = float('-inf')
    for direction in ['up', 'down', 'left', 'right']:
        new_board = move(board, direction)
        if not np.array_equal(board, new_board):
            score = expectimax(new_board, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = direction
    return best_move


def game_over(board):
    """return endame condition"""
    endgame = True
    win = False
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                win = True
            if i >0:
                if board[i][j] == board[i-1][j]:
                    endgame = False
            if j > 0:
                if board[i][j] == board[i][j-1]:
                    endgame = False
    return endgame | win


#starting program
board = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

print("Welcome to 2048 Solver! \n")
print("First, enter your desired search depth. The higher the depth, the longer the program will take to run.\n The maximum depth is 5. If you want to do more than 5, do it at your own risk.\n")
while True:
    depth = int(input("Enter the search depth (minimum 1): "))
    if depth >= 1:
        break
    else:
        print("Invalid input. Please enter a depth of at least 1.")
print("Input the current board state! \n")

for i in range(4):
    for j in range(4):
        while True:
            value = int(input(f"Value of row-{i+1} col-{j+1} (must be 0 or 2^n): "))
            if (value == 0 or (value > 0 and (value & (value - 1)) == 0) )and value !=1:
                board[i][j] = value
                break
            else:
                print("Invalid input. Please enter 0 or a power of 2.")
printboard(board)

best_move = find_best_move(board, depth)
print("Best move: ", best_move)

