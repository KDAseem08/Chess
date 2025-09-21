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

            if(set(piecesfound) == set(pieces)):
                return moves
            
            piece = board[row][col][1]
            
            if ((piece != None) and (piece.colour == colour)):
                piecesfound.append(type(piece).__name__)
                legal_moves = piece.get_legal_moves(board = board)
                for legal_move in legal_moves:
                    newmove = piece.position + legal_move
                    moves.append(newmove)

    

    




Game = script.ChessGame()
board = Game.get_board()

print(GetAllLegalMoves(board=board,colour = "White"))


Player1 = "White"
Player2 = "Black"


