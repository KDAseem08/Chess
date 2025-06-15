import pygame 
# Make all the piece classes
pieces = ["King","Queen","Knight","Bishop","Rook","Pawn"]
class Piece:
    def __init__(self, position,colour):
        self.position = position
        self.colour = colour
    def get_legal_moves(self,board):
        pass


class King(Piece):
    def get_legal_moves(self,board):
        self.availablepositions = []
        def validpos(dim):
            start_pos = self.position[dim]-1 #This row/col will be the starting point in the for loop (included)
            end_pos = self.position[dim]+2 #This row/col will be the stopping point in the for loop (not included)
            if (start_pos < 0):
                start_pos = 0 
            if (end_pos > 8):
                end_pos = 7
            return (start_pos,end_pos)

        start_row,end_row = validpos(dim=0)
        start_col, end_col = validpos(dim = 1)
        for row in range(start_row,end_row):
            for col in range(start_col,end_col):
                # The king can't move into a check or a space that's occupied by another piece
                #Will handle the check for later
                if(board[row][col][1] == None and self.pos_in_check([row,col],board) == False):
                    self.availablepositions.append([row,col])
        # Remove the original position 
        self.availablepositions.remove(self.position)
        return self.availablepositions
    
    def pos_in_check(self,pos,board):
        for row in range(8):
            for col in range(8):
                if board[row][col][1] is not None and board[row][col][1].colour != self.colour:
                    piece = board[row][col][1]
                    if pos in piece.get_legal_moves(board):
                        return True
        return False





class Queen(Piece):
    def get_legal_moves(self,board):
        # Create temporary Rook and Bishop objects at the Queen's position
        rook = Rook(position=self.position, colour=self.colour)
        bishop = Bishop(position=self.position, colour=self.colour)

        # Combine their legal moves
        self.availablepositions = rook.get_legal_moves(board) + bishop.get_legal_moves(board)
        return self.availablepositions


class Knight(Piece):
    def get_legal_moves(self,board):
        row, col = self.position
        self.availablepositions = []
        moves = [[row+2,col+1],[row+2,col-1],[row-2,col+1],[row-2,col-1],
                 [row+1,col+2],[row+1,col-2],[row-1,col+2],[row-1,col-2]]
        
        for move in moves:
            if (0 <= move[0] <= 7 and 0 <= move[1] <= 7 ):
                self.availablepositions.append(move)

class Bishop(Piece):
    def get_legal_moves(self,board):
        row, col = self.position
        diag_pos , diag_neg,antidiag_pos,antidiag_neg = True
        self.availablepositions = []
        # Diagonal: 
        for d in range(1, 8):
            if (row + d < 8 and col + d < 8 and diag_pos == True):
                if (board[row+d][col+d][1] != None):
                    if board[row+d][col+d][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row+d, col+d])
                    diag_pos = False
                else:
                    self.availablepositions.append([row + d, col + d])
            if row - d >= 0 and col - d >= 0 and diag_neg == True:
                if (board[row-d][col-d][1] != None):
                    if board[row-d][col-d][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row-d, col-d])
                    diag_neg = False
                else:
                    self.availablepositions.append([row - d, col - d])
        # Anti-diagonal: 
        for d in range(1, 8):
            if row + d < 8 and col - d >= 0 and antidiag_neg == True:
                if (board[row+d][col-d][1] != None):
                    if board[row+d][col-d][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row+d, col-d])
                    antidiag_neg = False
                else:
                    self.availablepositions.append([row + d, col - d])
            if row - d >= 0 and col + d < 8 and antidiag_pos == True:
                if (board[row-d][col+d][1] != None):
                    if board[row-d][col+d][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row-d, col+d])
                    antidiag_pos = False
                else:
                    self.availablepositions.append([row - d, col + d])
            
        return self.availablepositions

class Rook(Piece):
    def get_legal_moves(self,board):
        row, col = self.position
        row_pos,row_neg,col_pos,col_neg = True
        
        self.availablepositions = []
        for d in range(1,8):
            if row + d < 8 and row_pos == True:
                if (board[row+d][col][1] != None ):
                    # Cannot append this position (unless it's opponent piece which can be captured) and none of the next positions in this row can be added
                    if board[row+d][col][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row+d, col])
                    row_pos = False
                else:
                    self.availablepositions.append([row+d,col])

            if row - d >= 0 and row_neg == True: 
                if (board[row-d][col][1] != None ):
                    if board[row-d][col][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row+d, col])
                    # Cannot append this position and none of the next positions in this row can be added
                    row_neg = False

                else:
                    self.availablepositions.append([row-d,col])
            if col + d < 8 and col_pos == True:
                if (board[row][col+d][1] != None ):
                    # Cannot append this position and none of the next positions in this col can be added
                    if board[row][col+d][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row, col+d])
                    col_pos = False

                else:
                    self.availablepositions.append([row,col+d])
            if col - d >= 0 and col_neg == True: 
                if (board[row][col-d][1] != None ):
                    # Cannot append this position and none of the next positions in this col can be added
                    if board[row][col-d][1].colour != self.colour:  # Capture opponent piece
                        self.availablepositions.append([row, col-d])
                    col_neg = False

                else:
                    self.availablepositions.append([row,col-d])

        return self.availablepositions

class Pawn(Piece):
    def get_legal_moves(self,board):
        # Assuming position of a pawn can never be row 0 or 8 . They are forced to promote .
        row,col = self.position[0],self.position[1]
        self.availablepositions = []
        if (self.colour == 'White'):
            #Check if Diag capture is available
            if col + 1 < 8 and row + 1 < 8 and board[row+1][col+1][1] is not None:
                if board[row+1][col+1][1].colour != self.colour:
                    self.availablepositions.append([row+1, col+1])
            if col - 1 >= 0 and row + 1 < 8 and board[row+1][col-1][1] is not None:
                if board[row+1][col-1][1].colour != self.colour:
                    self.availablepositions.append([row+1, col-1])
            # Positions to move forward
            if (board[row+1][col][1] == None):
                if(row == 1):
                    self.availablepositions.append([row+1,col])
                    if (board[row+2][col][1] == None):
                        self.availablepositions.append([row+2,col])
                else:
                    self.availablepositions.append([row+1,col])
        else:
            # piece colour must be black 
            if col + 1 < 8 and row - 1 >= 0 and board[row-1][col+1][1] is not None:
                if board[row-1][col+1][1].colour != self.colour:
                    self.availablepositions.append([row-1, col+1])
            if col - 1 >= 0 and row - 1 >= 0 and board[row-1][col-1][1] is not None:
                if board[row-1][col-1][1].colour != self.colour:
                    self.availablepositions.append([row-1, col-1])
            
            if (board[row-1][col][1] == None):
                if(row == 6):
                    self.availablepositions.append([row-1,col])
                    if (board[row-2][col][1] == None):
                        self.availablepositions.append([row-2,col])
                else:
                    self.availablepositions.append([row-1,col])
        return self.availablepositions

class board():
    def __init__(self):
        self.board = [ [ ['W', None] for _ in range(8) ] for _ in range(8) ]
        for i in range(0,8):
            for j in range(0,8):
                if ((i+j)%2 == 0):
                    self.board[i][j] = ['B',None]
        
        def setpawns(board,row,colour):
            for j in range(8):
                board[row][j][1] = Pawn(position=[row,j],colour = colour)
        
        def set_king_row(board,row,colour):
            board[row][0][1] = Rook(position=[row,0],colour = colour)
            board[row][7][1] = Rook(position=[row,7],colour = colour)
            board[row][1][1] = Knight(position=[row,1],colour = colour)
            board[row][6][1] = Knight(position=[row,6],colour = colour)
            board[row][2][1] = Bishop(position=[row,2],colour = colour)
            board[row][5][1] = Bishop(position=[row,5],colour = colour)
            board[row][3][1] = Queen(position=[row,3],colour = colour)
            board[row][4][1] = King(position=[row,4],colour = colour)

        setpawns(self.board,1,colour = "White")
        setpawns(self.board,6,colour = "Black")
        set_king_row(self.board,0,colour = "White")
        set_king_row(self.board,7,colour = "Black")

    
    def getboard(self):
        return self.board

    def drawboard(self,surface):
        
        def getcolourtuple(colour):
            if (colour == 'W'):
                return (255,255,255)
            if (colour == 'B'):
                return (43, 45, 48) # Lighter shade of black
        
        # Calculate center position
        tile_size = 65
        BOARD_SIZE = tile_size * 8
        start_x = (800 - BOARD_SIZE) // 2  # Center horizontally
        start_y = (600 - BOARD_SIZE) // 2  # Center vertically
        
        for i in range(8):
            for j in range(8):
                tile_colour = self.board[i][j][0]
                x = start_x + (j * tile_size)
                y = start_y + (i * tile_size) 
                pygame.draw.rect(surface, getcolourtuple(tile_colour), pygame.Rect(x, y, tile_size, tile_size))
                if (board[i][j][1] != None):
                    piece = self.board[i][j][1]
                    piece_name = (type(piece).__name__)
                    downcased_piece_name = piece_name[0].lower() + piece_name[1:]
                    piece_colour = piece.colour
                    downcased_colour = piece_colour[0].lower() + piece_colour[1:]
                    file_name = f"{downcased_colour}-{downcased_piece_name}"   
                    image = pygame.image.load("ChessGame/pieces-basic-png/" + file_name + ".png")
                    image = pygame.transform.scale(image, (65, 65))
                    surface.blit(image, (x,y))

        
    
    def update_board(self,move):
        # move = [initial_pos,final_pos]
        # initial/final pos will be of form [row,col]
        initial_row,initial_col = move[0][0],move[0][1]
        final_row,final_col = move[1][0],move[1][1]
        piece = self.board[initial_row][initial_col][1]
        self.board[initial_row][initial_col][1] = None
        piece.position = move[1]
        self.board[final_row][final_col][1] = piece


class ChessGame():
    def __init__(self,surface):
        self.surface = surface
        self.moves = []
        self.board = board()
        self.colour_to_move = 'White'
        self.result = None
    def make_move(self,colour,move):
        initial_row,initial_col = move[0][0],move[0][1]
        piece = self.board[initial_row][initial_col][1]
        if piece == None:
            print("No piece selected!")
        elif piece.colour != colour:
            print("Its the other colour's turn")
        else:
            if (move[1] in piece.get_legal_moves()):
                self.moves.append(move)
                self.board.update_board(move = move)
                self.board.drawboard(surface= self.surface)
            else:
                print("Not a valid position to move")
    def is_checkmate(self,colour):
        #First find the king 
        in_check = False
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j][1]
                if isinstance(piece, King) and piece.colour == colour:
                    king_pos = [i,j]
                    king = piece
                    break
        #Now check if king is in check and has nowhere to go 
        legal_moves = king.get_legal_moves()
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j][1]
                if (piece != None):
                    if (king_pos in piece.get_legal_moves()):
                        in_check = True
                    a = set(piece.get_legal_moves())
                    legal_moves = list(set(legal_moves) - a.intersection(set(legal_moves)))
                    if (len(legal_moves) == 0):
                        return True
    
    def play(self):
        def get_opp_col(col):
            if (col == 'White'):
                return 'Black'
            else:
                return 'White'
            

        while(self.result == None):
            player_move = input(f" Enter move ({self.colour_to_move} to move) ")
            self.make_move(colour = self.colour_to_move,move = player_move)
            if (self.is_checkmate(colour = get_opp_col(self.colour_to_move))):
                self.result = f'{self.colour_to_move} wins!'
            self.colour_to_move = get_opp_col(self.colour_to_move)
