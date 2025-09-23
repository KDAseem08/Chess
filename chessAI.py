import script
import random
# Make 2 Players : Player 1 and Player 2
# For Each turn :
#   Player selects a random piece
#   and makes one of the legal moves.

pieces = ["Pawn","Rook","Knight","Bishop","King","Queen"]


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
            


    




Game = script.ChessGame()
board = Game.get_board()

Player1 = "White"
Player2 = "Black"
count = 0
# while((Game.is_checkmate(Player1) == False) and (Game.is_checkmate(Player2) == False) and (count < 10)):
#     colour_to_play = Game.colour_to_move
#     moves = GetAllLegalMoves(Game.get_board(),colour=colour_to_play)
#     random_move = random.choice(moves)
#     Game.play(random_move)
#     Game.board.drawboard()
#     print('----------------')
#     count += 1

