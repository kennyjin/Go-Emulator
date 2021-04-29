
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
# Parse coordinates, C12 -> (7, 3)
# play, genmove

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

        if s[0] == "showboard":
            print(out.format(''))
            print(showboard(board))
            print()

        if s[0] == "quit":
            break
