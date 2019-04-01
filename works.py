import chess
import time
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

board = chess.Board()
columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

def move_to_coordinates(the_move):
    from_coordinate = (char_to_int(the_move[0]), int(the_move[1]))
    to_coordinate = (char_to_int(the_move[2]), int(the_move[3]))
    return (from_coordinate, to_coordinate)

def char_to_int(char):
    for i in range(len(columns)):
        if columns[i] == char:
            return i+1
def remove_instance(k, arr):
    for i in arr:
        if(i == k):
            arr.remove(i)
    return arr

while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.100))
    where_to = move_to_coordinates(str(result.move))[1]
    where_from = move_to_coordinates(str(result.move))[0]

    print(where_from, where_to)
    #Capture piece
    board_array = board.unicode_array()
    board_array = remove_instance(" ", board_array)
    board_array = remove_instance("\n", board_array)
    print(str(board_array[((where_from[0]-1) + (8-where_from[1])*8)]) + "-->" + str(board_array[((where_to[0]-1) + (8-where_to[1])*8)]))
    time.sleep(0.01)

    #Castling
    castled = True
    if str(result.move) == "e1g1":
        new_rook_position = "g1"
    elif str(result.move) == "e1c1":
        new_rook_position = "c1"
    elif str(result.move) == "e8c8":
        new_rook_position = "c8"
    elif str(result.move) == "e8g8":
        new_rook_position = "g8"
    else:
        castled = False
    print(castled)

    board.push(result.move)
    print(board.unicode())
    print(result.move)
    print("---------------")
if board.is_game_over():
    print(board.result())

engine.quit()