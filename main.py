
import random

PROTOCOL_VERSION = 2
NAME = "Go Emulator"
VERSION = 0.1

komi = 7.5
boardsize = 19

valid_komi_range = (-100, 100)
valid_boardsize_range = (2, 25)

# 0 for empty, -1 for black, 1 for white
board = [[0] * boardsize for _ in range(boardsize)]

list_commands = ["protocol_version", "name", "version", "known_command", 
"list_commands", "quit", "boardsize", "clear_board", "komi", "play", "genmove", "showboard"]

set_commands = set(list_commands)

# TODO
# random play seems to be slower when move number is large, need to investigate

from collections import deque
'''
take the stones out of the board by
setting the connected group of (row, col) to 0
returns the number of stones captured
'''
def capture_stones(row, col, board):
    color = board[row][col]
    if color == 0:
        return 0
    
    queue = deque([])
    visited = set()
    queue.append((row, col))
    visited.add((row, col))
    board[row][col] = 0
    
    while queue:
        (curr_row, curr_col) = queue.popleft()
        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = curr_row + drow, curr_col + dcol
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and (new_row, new_col) not in visited and board[new_row][new_col] == color:
                queue.append((new_row, new_col))
                visited.add((new_row, new_col))
                board[new_row][new_col] = 0
                
    return len(visited)

'''
Count liberties for the connected group of (row, col)
if fast_mode is True, return 1 as soon as the group has >= 1 liberties
return liberty count
'''

def count_liberties(row, col, board, fast_mode=False):
    if board[row][col] == 0:
        return 0
    
    color = board[row][col]
    
    queue = deque([])
    visited = set()
    queue.append((row, col))
    visited.add((row, col))
    
    # the set of visited liberty positions
    visited_li = set()
    
    while queue:
        (curr_row, curr_col) = queue.popleft()
        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = curr_row + drow, curr_col + dcol
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                # Add liberty position to visited_li
                if board[new_row][new_col] == 0 and (new_row, new_col) not in visited_li:
                    # The group will have at least 1 liberty
                    if fast_mode:
                        return 1
                    visited_li.add((new_row, new_col))

                if board[new_row][new_col] == color and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col))
                    visited.add((new_row, new_col))
                    continue
                
    
    return len(visited_li)

'''
Checks if the move to be played is valid
inputs:
color: -1 for black, 1 for white
row, col are integers
returns whether the move is valid
'''
def valid_move(color, row, col, board):
    if not (0 <= row < len(board) and 0 <= col < len(board[0])):
        return False

    if board[row][col] != 0:
        return False
    
    board[row][col] = color
    
    # check if the connected group of color has >= 1 liberty
    if count_liberties(row, col, board, fast_mode=True) >= 1:
        board[row][col] = 0
        return True
    
    # check if any of the opponent's stone will be captured
    for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        curr_row, curr_col = row + drow, col + dcol
        if 0 <= curr_row < len(board) and 0 <= curr_col < len(board[0]) and board[curr_row][curr_col] == -color:
            li = count_liberties(curr_row, curr_col, board, fast_mode=True)
            if li == 0:
                board[row][col] = 0
                return True
            
    board[row][col] = 0
    return False

'''
inputs:
color: -1 for black, 1 for white
row, col are integers
returns None
'''
def play_move(color, row, col, board):
    if not valid_move(color, row, col, board):
        return
    
    board[row][col] = color
    
    # Capture opponent's stone
    for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        curr_row, curr_col = row + drow, col + dcol
        if 0 <= curr_row < len(board) and 0 <= curr_col < len(board[0]) and board[curr_row][curr_col] == -color:
            li = count_liberties(curr_row, curr_col, board, fast_mode=True)
            if li == 0:
                capture_stones(curr_row, curr_col, board)

'''
inputs: color, either black, b or white, w
board
returns the coordinates of the next move
random move selection
this function will always return a valid move position or None (for pass).
'''
def genmove(color, board):
    valid_positions = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0 and valid_move(color, i, j, board):
                valid_positions.append((i, j))

    # When there are no valid positions, the program will pass

    if len(valid_positions) == 0:
        return None

    (row, col) = random.choice(valid_positions)

    return row, col


'''
Parse coordinates, C12 -> (7, 3)
Note that C corresponds to the column number, 12 corresponds to the row number
There is no "I" in the letter part, J follows H
'''
def parse_letter_num_coor(l_n_coor, boardsize):
    l_n_coor = l_n_coor.lower()
    letter = l_n_coor[0]
    num = l_n_coor[1:]

    if not letter.isalpha() or letter == 'i':
        return None

    if not num.isdigit():
        return None

    row = boardsize - int(num)
    col = ord(letter) - ord('a') if letter < 'j' else ord(letter) - ord('a') - 1

    if row < 0 or row >= boardsize or col < 0 or col >= boardsize:
        return None

    return row, col

'''
Parse coordinates, (7, 3) -> C12
Note that C corresponds to the column number, 12 corresponds to the row number
There is no "I" in the letter part, J follows H
'''
def parse_row_col_coor(row, col, boardsize):
    letter = chr(col + ord('a')) if col < 8 else chr(col + 1 + ord('a'))
    num = boardsize - row
    return letter.upper() + str(num)

'''
Input: board, a 2d array with size boardsize * boardsize
Return: a string representation of the board
'''
def showboard(board):
    res = ''
    col_names = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    num_rows = len(board)
    num_cols = len(board[0])

    res += '   '
    res += ' '.join(col_names[:num_cols])
    res += '\n'

    for i in range(num_rows):
        row_num = num_rows - i

        if row_num >= 10:
            res += str(row_num) + " "
        else:
            res += " " + str(row_num) + " "

        row_res = ""

        for j in range(num_cols):
            if board[i][j] == 0:
                row_res += '. '
            elif board[i][j] == -1:
                # Black stone
                row_res += 'X '
            else:
                # White stone
                row_res += 'O '

        # remove the last space
        row_res = row_res[ : -1]
        res += row_res

        res += " " + str(row_num)
        res += "\n"

    res += '   '
    res += ' '.join(col_names[:num_cols])

    return res





if __name__ == '__main__':
    # print(NAME + ' v' + str(VERSION))
    # print("Type 'list_commands' to check available commands.")
    # print()

    while True:
        s = input()
        s = s.strip()
        s = s.split()

        out = "= {}"

        if len(s) == 0:
            continue

        if s[0] == "protocol_version":
            print(out.format(PROTOCOL_VERSION))
            print()
            continue
        
        if s[0] == "name":
            print(out.format(NAME))
            print()
            continue

        if s[0] == "version":
            print(out.format(VERSION))
            print()
            continue

        if s[0] == "known_command":
            if len(s) != 2:
                print("? Expected single argument for known_command")
                print()
                continue

            print(out.format(s[1] in set_commands))
            print()
            continue


        if s[0] == "list_commands":
            print(out.format('\n'.join(list_commands)))
            print()
            continue

        if s[0] == "boardsize":
            if len(s) != 2:
                print("? Expected single integer argument for known_command")
                print()
                continue

            if int(s[1]) < valid_boardsize_range[0] or int(s[1]) > valid_boardsize_range[1]:
                print("? Unacceptable size")
                print()
                continue


            # Reinitialize board only when boardsize changes
            if int(s[1]) != boardsize:
                boardsize = int(s[1])
                board = [[0] * boardsize for _ in range(boardsize)]

            print(out.format(''))
            print()
            continue

        if s[0] == "clear_board":
            board = [[0] * boardsize for _ in range(boardsize)]
            print(out.format(''))
            print()
            continue

        if s[0] == "komi":
            if len(s) != 2:
                print("? Expected single float argument for komi")
                print()
                continue

            if float(s[1]) < valid_komi_range[0] or float(s[1]) > valid_komi_range[1]:
                print("? Unacceptable komi")
                print()
                continue

            komi = float(s[1])
            print(out.format(''))
            print()
            continue

        if s[0] == "play":
            if len(s) != 3:
                print("? Expected 2 arguments for play")
                print()
                continue

            color = s[1]
            pos = s[2]

            if pos == 'pass':
                print(out.format(''))
                print()
                continue

            if color.lower() not in ['black', 'b', 'white', 'w']:
                print("? Invalid color")
                print()
                continue

            new_pos = parse_letter_num_coor(pos, boardsize)

            if new_pos == None:
                print("? Invalid move position")
                print()
                continue

            row, col = new_pos

            if color.lower() == 'black' or color.lower() == 'b':
                color = -1
            else:
                color = 1

            if not valid_move(color, row, col, board):
                print("? Invalid move position")
                print()
                continue

            play_move(color, row, col, board)

            print(out.format(''))
            print()
            continue

        if s[0] == "genmove":
            if len(s) != 2:
                print("? Expected color argument for genmove")
                print()
                continue

            if s[1].lower() not in ['black', 'b', 'white', 'w']:
                print("? Invalid color")
                print()
                continue

            if s[1].lower() == 'black' or s[1].lower() == 'b':
                color = -1
            else:
                color = 1

            new_pos = genmove(color, board)

            if new_pos == None:
                print(out.format('pass'))
                print()
                continue

            row, col = new_pos

            play_move(color, row, col, board)

            l_n_coor = parse_row_col_coor(row, col, boardsize)
            print(out.format(l_n_coor))
            print()
            continue


        if s[0] == "showboard":
            print(out.format(''))
            print(showboard(board))
            print()
            continue

        if s[0] == "quit":
            break

        print("? Unknown command")
        print()
