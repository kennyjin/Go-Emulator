import helper

PROTOCOL_VERSION = 2
NAME = "Go Emulator"
VERSION = 0.1

komi = 7.5
boardsize = 19

valid_komi_range = (-100, 100)
valid_boardsize_range = (2, 25)

# 0 for empty, -1 for black, 1 for white
board = [[0] * boardsize for _ in range(boardsize)]

# a list of previous board positions
# each board position is stored as a 2d tuple
board_positions = []
board_positions.append(tuple(tuple(row) for row in board))

# a set of previous board positions
# each board position is stored as a 2d tuple
board_positions_set = set(board_positions)

list_commands = ["protocol_version", "name", "version", "known_command", 
"list_commands", "quit", "boardsize", "clear_board", "komi", "play", "genmove", "showboard", "final_score"]

set_commands = set(list_commands)

# random play seems to be slower when move number is large, which seems to be the problem of Sabaki

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

                # a list of previous board positions
                # each board position is stored as a 2d tuple
                board_positions = []
                board_positions.append(tuple(tuple(row) for row in board))

                # a set of previous board positions
                # each board position is stored as a 2d tuple
                board_positions_set = set(board_positions)

            print(out.format(''))
            print()
            continue

        if s[0] == "clear_board":
            board = [[0] * boardsize for _ in range(boardsize)]

            # a list of previous board positions
            # each board position is stored as a 2d tuple
            board_positions = []
            board_positions.append(tuple(tuple(row) for row in board))

            # a set of previous board positions
            # each board position is stored as a 2d tuple
            board_positions_set = set(board_positions)

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

            if pos.lower() == 'pass':
                print(out.format(''))
                print()
                continue

            if color.lower() not in ['black', 'b', 'white', 'w']:
                print("? Invalid color")
                print()
                continue

            new_pos = helper.parse_letter_num_coor(pos, boardsize)
            # print(new_pos)

            if new_pos == None:
                print("? Invalid move position")
                print()
                continue

            row, col = new_pos

            if color.lower() == 'black' or color.lower() == 'b':
                color = -1
            else:
                color = 1

            if not helper.valid_move(color, row, col, board, board_positions, board_positions_set):
                print("? Invalid move position")
                print()
                continue

            helper.play_move(color, row, col, board, board_positions, board_positions_set)

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

            new_pos = helper.genmove(color, board, board_positions, board_positions_set)

            if new_pos == None:
                print(out.format('pass'))
                print()
                continue

            row, col = new_pos

            helper.play_move(color, row, col, board, board_positions, board_positions_set)

            l_n_coor = helper.parse_row_col_coor(row, col, boardsize)
            print(out.format(l_n_coor))
            print()
            continue


        if s[0] == "showboard":
            print(out.format(''))
            print(helper.showboard(board))
            print()
            continue

        if s[0] == 'final_score':
            print(out.format(helper.final_score(board, komi)))
            print()
            continue

        if s[0] == "quit":
            break

        print("? Unknown command")
        print()
