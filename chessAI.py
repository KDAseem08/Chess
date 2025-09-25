import script
import random
# Make 2 Players : Player 1 and Player 2
# For Each turn :
#   Player selects a random piece
#   and makes one of the legal moves.

piece_values= {"Pawn":1,"Rook":5,"Knight":3,"Bishop":3,"King":4,"Queen":9}


def GetAllLegalMoves(board,colour):
    piecesfound =[]
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col][1]
            
            if ((piece != None) and (piece.colour == colour)):
                piecesfound.append(type(piece).__name__)    
                legal_moves = piece.get_legal_moves(board = board)
                for legal_move in legal_moves:
                    newmove = [piece.position] + [legal_move]
                    moves.append(newmove)
    return moves
            
def eval(board):
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




Game = script.ChessGame()
board = Game.get_board()

#print(eval(board))


# Play Random Moves each turn. 
#count = 0
# while((Game.is_checkmate("White") == False) and (Game.is_checkmate("White") == False) and (count < 10)):
#     colour_to_play = Game.colour_to_move
#     moves = GetAllLegalMoves(Game.get_board(),colour=colour_to_play)
#     random_move = random.choice(moves)
#     Game.play(random_move)
#     Game.board.drawboard()
#     print('----------------')
#     count += 1

