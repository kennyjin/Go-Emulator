import random
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
def valid_move(color, row, col, board, board_positions, board_positions_set):
    if not (0 <= row < len(board) and 0 <= col < len(board[0])):
        return False

    if board[row][col] != 0:
        return False
    
    board[row][col] = color

    # When it is False after 2 steps, the move must be invalid. When it is True, we need to check for ko
    ko_check = False
    
    # check if the connected group of color has >= 1 liberty
    if count_liberties(row, col, board, fast_mode=True) >= 1:
        board[row][col] = 0
        ko_check = True
        # return True
    
    if not ko_check:
        # check if any of the opponent's stone will be captured
        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            curr_row, curr_col = row + drow, col + dcol
            if 0 <= curr_row < len(board) and 0 <= curr_col < len(board[0]) and board[curr_row][curr_col] == -color:
                li = count_liberties(curr_row, curr_col, board, fast_mode=True)
                if li == 0:
                    board[row][col] = 0
                    ko_check = True
                    # return True

    if not ko_check:
        board[row][col] = 0
        return False

    # The move meets the basic requirements of validity, now check for ko
    board[row][col] = color
    
    # Capture opponent's stone
    for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        curr_row, curr_col = row + drow, col + dcol
        if 0 <= curr_row < len(board) and 0 <= curr_col < len(board[0]) and board[curr_row][curr_col] == -color:
            li = count_liberties(curr_row, curr_col, board, fast_mode=True)
            if li == 0:
                capture_stones(curr_row, curr_col, board)

    if tuple(tuple(row) for row in board) in board_positions_set:
        # restore board to the previous board position
        # cannot set board to a new object as it will not impact board outside of this function
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j] = board_positions[-1][i][j]
        return False

    # restore board to the previous board position        
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = board_positions[-1][i][j]

    return True

'''
Undo the previous move
If the length of board positions <= 1, the position is not undoable.
Return True is undo is successful, False otherwise. 
'''
def undo(board, board_positions, board_positions_set):
    if len(board_positions) <= 1:
        return False

    # remove current board position from board_positions and board_positions_set
    curr_board_position = board_positions.pop()
    board_positions_set.remove(curr_board_position)

    # restore board to the previous board position        
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = board_positions[-1][i][j]

    return True




'''
inputs:
color: -1 for black, 1 for white
row, col are integers
returns None
call valid_move() before calling this
'''
def play_move(color, row, col, board, board_positions, board_positions_set):
    
    board[row][col] = color
    
    # Capture opponent's stone
    for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        curr_row, curr_col = row + drow, col + dcol
        if 0 <= curr_row < len(board) and 0 <= curr_col < len(board[0]) and board[curr_row][curr_col] == -color:
            li = count_liberties(curr_row, curr_col, board, fast_mode=True)
            if li == 0:
                capture_stones(curr_row, curr_col, board)

    # save current board position
    board_positions.append(tuple(tuple(row) for row in board))
    board_positions_set.add(tuple(tuple(row) for row in board))
    # print(len(board_positions), len(board_positions_set))

'''
inputs: color, either black, b or white, w
board
returns the coordinates of the next move
random move selection
this function will always return a valid move position or None (for pass).
'''
def genmove(color, board, board_positions, board_positions_set):
    valid_positions = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0 and valid_move(color, i, j, board, board_positions, board_positions_set):
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
    # print(board)
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

'''
https://senseis.xmp.net/?TrompTaylorRules
Computes the Tromp-Taylor score (komi not included) of the current board position.
Returns black_score, white_score
Note that empty points that can "reach" both black stones and white stones 
are not included in either black_score or white_score.
'''
def tromp_taylor_score(board):
    black_score, white_score = 0, 0
    queue = deque([])
    visited = set()
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == -1:
                black_score += 1
                continue
            elif board[i][j] == 1:
                white_score += 1
                continue
                
            # When getting to an empty point, we check what color this point can reach.
            if (i, j) in visited:
                continue
                
            reachable_black_cnt = 0
            reachable_white_cnt = 0
            queue.append((i, j))
            visited.add((i, j))
            
            # The positions of visited reachable black stones and white stones
            visited_bw = set()
            
            # The connected group of this empty point is of size 1 initially.
            comp_size = 1
            
            while queue:
                (curr_row, curr_col) = queue.popleft()
                for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = curr_row + drow, curr_col + dcol
                    if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                        if board[new_row][new_col] == 0 and (new_row, new_col) not in visited:
                            queue.append((new_row, new_col))
                            visited.add((new_row, new_col))
                            comp_size += 1
                            continue
                            
                        if board[new_row][new_col] == -1 and (new_row, new_col) not in visited_bw:
                            reachable_black_cnt += 1
                            visited_bw.add((new_row, new_col))
                            continue
                        
                        if board[new_row][new_col] == 1 and (new_row, new_col) not in visited_bw:
                            reachable_white_cnt += 1
                            visited_bw.add((new_row, new_col))
                            continue
                            
            if reachable_black_cnt > 0 and reachable_white_cnt == 0:
                black_score += comp_size
            elif reachable_black_cnt == 0 and reachable_white_cnt > 0:
                white_score += comp_size
                        
                
    return black_score, white_score

'''
Returns the final score of the game, using Tromp-Taylor scoring.
Example results: 'B+2.5' (Black wins by 2.5 points), 'W+0.5' (White wins by 0.5 points), etc.
'''
def final_score(board, komi):
    black_score, white_score = tromp_taylor_score(board)
    white_score += komi
    
    # Draw
    if black_score == white_score:
        return '0'
    if black_score > white_score:
        return 'B+{}'.format(black_score - white_score)
    return 'W+{}'.format(white_score - black_score)