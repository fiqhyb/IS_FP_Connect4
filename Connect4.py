import numpy as np
import math
import time

s_row = 6
s_column = 7

player_disk = 1
ai_disk = 2


# allscore = []
# allboard = []


def generate_board():
    board = np.zeros((s_row, s_column))
    return board


def fill(board, row, col, piece):
    board[row][col] = piece


def valid_slot(board, col):
    return board[s_row - 1][col] == 0


def get_row(board, col):
    for r in range(s_row):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))
    print("  1  2  3  4  5  6  7  ")


def four_in_row(board, piece):
    # Check horizontal locations for win
    for c in range(s_column - 3):
        for r in range(s_row):
            if board[r][c] == piece and \
                    board[r][c + 1] == piece and \
                    board[r][c + 2] == piece and \
                    board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(s_column):
        for r in range(s_row - 3):
            if board[r][c] == piece and \
                    board[r + 1][c] == piece and \
                    board[r + 2][c] == piece and \
                    board[r + 3][c] == piece:
                return True

    # Check positive diagonals
    for c in range(s_column - 3):
        for r in range(s_row - 3):
            if board[r][c] == piece and \
                    board[r + 1][c + 1] == piece and \
                    board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    # Check negative diagonals
    for c in range(s_column - 3):
        for r in range(3, s_row):
            if board[r][c] == piece and \
                    board[r - 1][c + 1] == piece and \
                    board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


def check_four(window, piece):
    score = 0
    opp_piece = player_disk
    if piece == player_disk:
        opp_piece = ai_disk

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_column(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, s_column // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(s_row):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(s_column - 3):
            window = row_array[c:c + 4]
            score += check_four(window, piece)

    ## Score Vertical
    for c in range(s_column):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(s_row - 3):
            window = col_array[r:r + 4]
            score += check_four(window, piece)

    ## Score Diagonal
    for r in range(s_row - 3):
        for c in range(s_column - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += check_four(window, piece)

    for r in range(s_row - 3):
        for c in range(s_column - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += check_four(window, piece)

    # print("SCORE")
    # print(score)
    return score


def terminal_node(board):
    return four_in_row(board, player_disk) or four_in_row(board, ai_disk) or len(get_columns(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_columns(board)
    is_terminal = terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if four_in_row(board, ai_disk):
                return (None, 100000000000000)
            elif four_in_row(board, player_disk):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_column(board, ai_disk))
    if maximizingPlayer:
        value = -math.inf
        column = int
        for col in valid_locations:
            row = get_row(board, col)
            b_copy = board.copy()
            fill(b_copy, row, col, ai_disk)
            # allboard.append(b_copy)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            # allscore.append(new_score)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = int
        for col in valid_locations:
            row = get_row(board, col)
            b_copy = board.copy()
            fill(b_copy, row, col, player_disk)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_columns(board):
    valid_locations = []
    for col in range(s_column):
        if valid_slot(board, col):
            valid_locations.append(col)
    return valid_locations


def ai_turn(game_board, player, depth):
    # input("Press Enter to continue...")
    print("###########################\nturn {0}".format(player))
    start = time.time()
    column, minimax_score = minimax(game_board, depth, -math.inf, math.inf, True)
    end = time.time()
    print(end - start)
    if valid_slot(game_board, column):
        row = get_row(game_board, column)
        fill(game_board, row, column, player)
    print_board(game_board)
    input("Press Enter to continue...")


def player_turn(game_board, player):
    print("###########################\nturn {0}".format(player))
    column = int(input("select a spot :")) - 1
    if valid_slot(game_board, column):
        row = get_row(game_board, column)
        fill(game_board, row, column, player)

    print_board(game_board)


def game():
    # Standard Connect 4 board dimensions
    global choice, ai_depth2, ai_depth1, selected_turn
    game_board = generate_board()
    print_board(game_board)
    winner = 0
    turn = 1
    count = 0
    while True:
        print("Choose option:")
        print("[1] Player vs Player")
        print("[2] Player vs AI")
        print("[3] AI vs AI")
        try:
            choice = int(input("Choice: "))
            if not (choice in [1, 2, 3]):
                print("Invalid input. Please select a number from 1-3")
                continue
            break
        except:
            print("Invalid input. Please select a number from 1-3")
            continue

    if choice == 2:
        while True:
            print("Player or AI move first?")
            print("[1] Turn 1 Player")
            print("[2] Turn 2 Player")
            try:
                selected_turn = int(input("Turn: "))
                if not (selected_turn in [1, 2]):
                    print("Invalid input. Please select a number from 1-2")
                    continue
                break
            except:
                print("Invalid input. Please select a number from 1-2")
                continue

        while True:
            print("Set depth for AI")
            print("Range 1-8, the higher the value the longer the computation time")
            try:
                ai_depth1 = int(input("Depth: "))
                if not (ai_depth1 in [1, 2, 3, 4, 5, 6, 7, 8]):
                    print("Invalid input. Please select a number from 1-8")
                    continue
                break
            except:
                print("Invalid input. Please select a number from 1-8")
                continue

    if choice == 3:
        while True:
            print("Set depth for first AI")
            print("Range 1-8, the higher the value the longer the computation time")
            try:
                ai_depth1 = int(input("Depth: "))
                if not (ai_depth1 in [1, 2, 3, 4, 5, 6, 7, 8]):
                    print("Invalid input. Please select a number from 1-8")
                    continue
                break
            except:
                print("Invalid input. Please select a number from 1-8")
                continue

        while True:
            print("Set depth for second AI")
            print("Range 1-8, the higher the value the longer the computation time")
            try:
                ai_depth2 = int(input("Depth: "))
                if not (ai_depth2 in [1, 2, 3, 4, 5, 6, 7, 8]):
                    print("Invalid input. Please select a number from 1-8")
                    continue
                break
            except:
                print("Invalid input. Please select a number from 1-8")
                continue
    counter = 0
    while winner == 0:
        print_board(game_board)
        if turn == 1:
            if choice == 1:
                player_turn(game_board, turn)
            elif choice == 2:
                if selected_turn == 1:
                    player_turn(game_board, turn)
                else:
                    ai_turn(game_board, turn, ai_depth1)
            elif choice == 3:
                ai_turn(game_board, turn, ai_depth1)

            if four_in_row(game_board, 1):
                winner = 1
            turn = 2
        elif turn == 2:

            if choice == 1:
                player_turn(game_board, turn)
            elif choice == 2:
                if selected_turn == 2:
                    player_turn(game_board, turn)
                else:
                    ai_turn(game_board, turn, ai_depth1)

            elif choice == 3:
                ai_turn(game_board, turn, ai_depth2)

            if four_in_row(game_board, 2):
                winner = 2
            turn = 1
        if winner != 0:
            print("Winner :", winner)
            input("Press Enter to continue...")
            break


while True:
    gaming = int
    game()
    while True:
        print("New game?")
        print("[1] Yes")
        print("[2] No")
        try:
            gaming = int(input("Choice: "))
            if not (gaming in [1, 2]):
                print("Invalid input. Please select a number from 1-2")
                continue
            break
        except:
            print("Invalid input. Please select a number from 1-2")
            continue
    if gaming == 2:
        break
