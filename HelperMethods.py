import Engine
import random
import copy
import graphical_interface

# Make 2 Players : Player 1 and Player 2
# For Each turn :
#   Player selects a random piece
#   and makes one of the legal moves.


def get_opp_col(col):
    if col == "White":
        return "Black"
    else:
        return "White"


def sync_piece_positions(board_array):
    for i in range(8):
        for j in range(8):
            piece = board_array[i][j][1]
            if piece:
                piece.position = [i, j]


def GetAllLegalMoves(board,colour):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col][1]

            if ((piece != None) and (piece.colour == colour)):  
                psuedo_legal_moves = piece.get_legal_moves(board = board,ignore_pins = False)
                for move in psuedo_legal_moves:
                    newmove = [piece.position] + [move]
                    temp_board_array = copy.deepcopy(board)
                    sync_piece_positions(temp_board_array)
                    temp_board = Engine.Board(custom_position=temp_board_array)
                    temp_board.update_board(newmove)
                    king_pos = None
                    for i in range(8):
                        for j in range(8):
                            temp_piece = temp_board.getboard()[i][j][1]
                            if (isinstance(temp_piece, Engine.King) and temp_piece.colour == colour):
                                king_pos = [i, j]
                                break
                        if king_pos:
                            break
                    if not temp_board.getboard()[king_pos[0]][king_pos[1]][1].pos_in_check(temp_board.getboard()):
                        moves.append(newmove)

    return moves

def material_count(board):
    piece_values= {"Pawn":1,"Rook":5,"Knight":3,"Bishop":3,"King":4,"Queen":9}
    white_sum = 0
    black_sum = 0
    for row in range(8):
        for col in range(8):

            piece = board[row][col][1]
            if (piece != None):
                if (piece.colour == "White"):
                    white_sum += piece_values[type(piece).__name__]
                else:
                    black_sum += piece_values[type(piece).__name__]

    return white_sum - black_sum


def evaluate_position(game, colour_to_move):
    # Checkmate?
    if game.is_checkmate("White"):
        return -float("inf")  # side to move is checkmated
    if game.is_checkmate("Black"):
        return float("inf")  # opponent is checkmated

    # Stalemate?
    if not GetAllLegalMoves(game.get_board(), colour_to_move):
        return 0  # draw

    # Otherwise, just material
    return material_count(game.get_board())


# Game = Engine.ChessGame()
# board = Game.get_board()


# print(eval(board))


# Play Random Moves each turn.
# count = 0
# while((Game.is_checkmate("White") == False) and (Game.is_checkmate("Black") == False) and (count < 10)):
#     colour_to_play = Game.colour_to_move
#     moves = GetAllLegalMoves(Game.get_board(),colour=colour_to_play)
#     random_move = random.choice(moves)
#     Game.play(random_move)
#     Game.board.drawboard()
#     print('----------------')
#     count += 1
