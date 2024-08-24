"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""
from math import sqrt
import copy


def is_empty(board):
    for i in range(len(board)):
        for e in range(len(board[0])):
            if board[i][e] != " ":
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    judge_number = 0
    if y_end + d_y <= 7 and x_end + d_x <= 7:
        if board[y_end + d_y][x_end + d_x] == " ":  # the last one
            judge_number = judge_number + 1
    if y_end - (length) * (d_y) >= 0 and x_end - (length) * (d_x) >= 0:
        if board[y_end - (length) * (d_y)][x_end - (length) * (d_x)] == " ":
            judge_number = judge_number + 1
    if judge_number == 0:
        return "CLOSED"
    if judge_number == 1:
        return "SEMIOPEN"
    if judge_number == 2:
        return "OPEN"
    judge_number = 0


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    counter = 0
    y_end_location = 0
    x_end_location = 0
    for e in range(min(len(board), len(board[0]))):
        rows = y_start + e * d_y
        cols = x_start + e * d_x
        counter = counter + 1
        if rows == len(board) or cols == len(board[0]):
            break
    col_counter = 0
    for s in range(counter - length):
        for i in range(length):
            if board[y_start + (s + i) * d_y][x_start + (s + i) * d_x] == col:
                col_counter += 1
            else:
                pass
            if col_counter == length:
                y_end_location = y_start + (s + i) * d_y
                x_end_location = x_start + (s + i) * d_x
                break
    # if it doesnt end at the endpoints:
    if y_end_location != len(board) - 1 and x_end_location != len(board[0]) - 1:
        if board[y_end_location + 1][x_end_location + 1] == " " and board[y_end_location - length][x_end_location - length] == " ":
            open_seq_count += 1
            return open_seq_count, semi_open_seq_count
        if board[y_end_location + 1][x_end_location + 1] == " " or board[y_end_location - length][x_end_location - length] == " ":
            semi_open_seq_count += 1
            return open_seq_count, semi_open_seq_count
        else:
            return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(len(board)):
        for e in range(len(board[0])):
            if board[i][e] == col:  # if that piece is that col
                # different types
                # (dy,dx)
                # (0,1) type, left to right
                dy, dx = 0, 1
                counter = 0
                if i + dy * length <= len(board) and e + dx * length <= len(board[0]):
                    for s in range(length):
                        if board[i + s * dy][e + s * dx] == col:
                            counter += 1
                    if counter == length:  # if it does make a sequecne of same colors
                        if e == 0:  # if its touch left side colum
                            # the other side is free
                            if board[i + (length) * dy][e + (length) * dx] == " ":
                                semi_open_seq_count += 1
                        else:
                            # other side is out of bounds
                            if i + (length) * dy > len(board) or e + (length) * dx > len(board[0]):
                                if board[i - dy][e - dx] == " ":
                                    semi_open_seq_count += 1
                            else:
                                # and i - dy >= 0 and e - dx >= 0:
                                if i + (length) * dy < len(board) and e + (length) * dx < len(board[0]):
                                    # both ends open
                                    if board[i + (length) * dy][e + (length) * dx] == " " and board[i - dy][e - dx] == " ":
                                        open_seq_count += 1
                                    # only one end open
                                    elif board[i + (length) * dy][e + (length) * dx] == " " or board[i - dy][e - dx] == " ":
                                        semi_open_seq_count += 1
                                elif e + length*dx == len(board[0]):
                                    if board[i - dy][e - dx] == " " and i - dy >= 0 and e - dx >= 0:
                                        semi_open_seq_count += 1
                # (0,1) type, top to bottom shabi qi shi shi (1,0)
                dy, dx = 1, 0
                counter = 0
                if i + dy * length <= len(board) and e + dx * length <= len(board[0]):
                    for s in range(length):
                        if board[i + s * dy][e + s * dx] == col:
                            counter += 1
                    if counter == length:
                        if i == 0:
                            if i + (length) * dy < len(board):
                                # the other side is free
                                if board[i + (length) * dy][e + (length) * dx] == " ":
                                    semi_open_seq_count += 1
                        else:
                            # not first row nor first column
                            if i + (length) * dy < len(board) and e + (length) * dx <= len(board[0]) and i - dy >= 0 and e - dx >= 0:
                                # just changed
                                if board[i + (length) * dy][e + (length) * dx] == " " and board[i - dy][e - dx] == " ":
                                    open_seq_count = open_seq_count + 1
                                elif board[i + (length) * dy][e + (length) * dx] == " " or board[i - dy][e - dx] == " ":
                                    semi_open_seq_count += 1
                            else:  # last element is at the edge
                                if i + (length) * dy == len(board) + 1:
                                    if board[i - dy][e - dx] == " " and i - dy >= 0 and e - dx >= 0:
                                        semi_open_seq_count += 1

                # (1,1) type, upper left lower right
                dy, dx = 1, 1
                counter = 0
                if i + dy * length <= len(board) and e + dx * length <= len(board[0]):
                    for s in range(length):
                        if board[i + s * dy][e + s * dx] == col:
                            counter += 1
                    if counter == length:
                        if i == 0 and e == 0:  # if its touch left edge
                            # the other side is free
                            if board[i + (length) * dy][e + (length) * dx] == " ":
                                semi_open_seq_count += 1
                        elif i == 0:  # if its at the first row
                            if i + (length) * dy <= len(board) and e + (length) * dx <= len(board[0]):
                                # the other side is free
                                if board[i + (length) * dy][e + (length) * dx] == " ":
                                    semi_open_seq_count += 1
                        elif e == 0:  # if its at the first column
                            # the other side is free
                            if board[i + (length) * dy][e + (length) * dx] == " ":
                                semi_open_seq_count += 1
                        else:
                            if i + (length) * dy < len(board) and e + (length) * dx < len(board[0]):
                                if board[i + (length) * dy][e + (length) * dx] == " " and board[i - dy][e - dx] == " ":
                                    open_seq_count += 1
                                elif board[i + (length) * dy][e + (length) * dx] == " " or board[i - dy][e - dx] == " ":
                                    semi_open_seq_count += 1
                # (1,-1) type, upper right to lower left
                dy, dx = 1, -1
                counter = 0
                # make sure that the stone is on board
                if i + dy * length <= len(board) and e + dx * length <= len(board[0]) and e + dx * length >= 0:
                    for s in range(length):
                        if board[i + s * dy][e + s * dx] == col:
                            counter += 1
                    if counter == length:
                        if i == len(board) - 1 or e == 0:  # if its at the last row
                            pass
                        elif e == len(board[0]) - 1:  # if its at the last column
                            # the other side is free
                            if board[i + (length) * dy][e + (length) * dx] == " ":
                                semi_open_seq_count += 1
                        elif i + length * dy == len(board) - 1 or e + length * dx == 0:
                            if board[i - dy][e - dx] == " ":
                                semi_open_seq_count += 1
                        else:
                            # if i + (length) * dy < len(board) and e + (length) * dx < len(board[0]):#just in case if the stone is not in the board
                            if board[i + (length) * dy][e + (length) * dx] == " " and board[i - dy][e - dx] == " ":
                                open_seq_count += 1
                            elif board[i + (length) * dy][e + (length) * dx] == " " or board[i - dy][e - dx] == " ":
                                semi_open_seq_count += 1

    return open_seq_count, semi_open_seq_count


def search_max(board):
    # collect all the empty spaces in the board
    row_num = []
    col_num = []
    for i in range(len(board)):
        for e in range(len(board[0])):
            if board[i][e] == " ":
                row_num.append(i)
                col_num.append(e)
    # loop through of putting all the stones on the empty spaces
    listofscore = []
    for s in range(len(row_num)):
        temp_board = copy.deepcopy(board)
        put_seq_on_board(temp_board, row_num[s], col_num[s], 0, 0, 1, "b")
        x = 0
        x = score(temp_board)
        listofscore.append(x)
        x = 0
    y = listofscore.index(max(listofscore))
    move_y = row_num[y]
    move_x = col_num[y]
    # get a list of score of corresponding placemnets
    # return the highest one
    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    '''is win(board) This function determines the current status of the game, and returns one of
["White won", "Black won", "Draw", "Continue playing"], depending on the current status
on the board. The only situation where "Draw" is returned is when board is full.'''
    for color in ["b", "w"]:
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == color:
                    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
                    for dr, dc in directions:
                        count = 1
                        for step in range(1, 5):
                            r, c = row + dr * step, col + dc * step
                            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == color:
                                count += 1
                            else:
                                break
                        if count == 5:
                            if color == "b":
                                return "Black won"
                            else:
                                return "White won"
    if all(board[row][col] != " " for row in range(len(board)) for col in range(len(board[0]))):
        return "Draw"

    return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i % 10) + "|"
    s += str((len(board[0])-1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5
    y = 1
    d_x = 0
    d_y = 1
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5
    y = 1
    d_x = 0
    d_y = 1
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5
    y = 1
    d_x = 0
    d_y = 1
    length = 3
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5
    y = 0
    d_x = 0
    d_y = 1
    length = 4
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6
    y = 0
    d_x = 0
    d_y = 1
    length = 4
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4, 6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")
        print(search_max(board))


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5
    x = 2
    d_x = 0
    d_y = 1
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3
    x = 5
    d_x = -1
    d_y = 1
    length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5
    x = 3
    d_x = -1
    d_y = 1
    length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    easy_testset_for_main_functions()
    some_tests()
