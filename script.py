# Make all the piece classes
pieces = ["King", "Queen", "Knight", "Bishop", "Rook", "Pawn"]


class Piece:
    """
    This is a generic Piece class. Each Piece on the chess board has 2 properties; position on the chess board and it's colour.
    The chess board is assummed to be an 8x8 array in python.

    """

    def __init__(self, position, colour):
        self.position = (
            position  # Position is of form [row,col] (0 <= row <= 7) & (0 <= col <= 7)
        )
        self.colour = colour  # colour can be either "White" or "Black"

    def get_legal_moves(self, board):
        """
        This method returns a list of positions that the very specific piece can make on board.
        It is a generic method since each piece moves differently and is meant to be overriden by the specific piece class like "King" or "Queen" etc.

        """
        pass


class King(Piece):
    def pos_in_check(self, pos, board):
        """
        Checks if the King piece is in check. board is a 3 Dimensional Array. Imagine an 8 x 8 array and in each position is ['Chess Tile Colour' , 'Piece'].
        If there is no piece on that tile then position is ['Chess Tile Colour' , None]

        """

        for row in range(8):
            for col in range(8):
                if (
                    board[row][col][1] is not None
                    and board[row][col][1].colour != self.colour
                ):  # If there is a piece at this position and it is an enemy piece.
                    piece = board[row][col][
                        1
                    ]  # Store that piece and check it's legal moves
                    if isinstance(piece, King):
                        if pos in piece.squares_covered():
                            return True
                    elif pos in piece.get_legal_moves(
                        board
                    ):  # If the current pos (position) of the king lies in those legal moves, then the king is in check.
                        return True
        return False

    def squares_covered(self):
        covered_squares = []

        def validpos(dim):
            start_pos = (
                self.position[dim] - 1
            )  # This row/col will be the starting point in the for loop (included)
            end_pos = (
                self.position[dim] + 2
            )  # This row/col will be the stopping point in the for loop (not included)
            if start_pos < 0:
                start_pos = 0
            if end_pos > 7:
                end_pos = 7
            return (start_pos, end_pos)

        start_row, end_row = validpos(dim=0)
        start_col, end_col = validpos(dim=1)
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                covered_squares.append([row, col])
        return covered_squares

    def get_legal_moves(self, board):

        self.availablepositions = []

        def validpos(dim):
            start_pos = (
                self.position[dim] - 1
            )  # This row/col will be the starting point in the for loop (included)
            end_pos = (
                self.position[dim] + 2
            )  # This row/col will be the stopping point in the for loop (not included)
            if start_pos < 0:
                start_pos = 0
            if end_pos > 7:
                end_pos = 7
            return (start_pos, end_pos)

        start_row, end_row = validpos(dim=0)
        start_col, end_col = validpos(dim=1)
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if (
                    board[row][col][1] == None
                    and self.pos_in_check([row, col], board) == False
                ):  # If there is no piece in this position and my king doesn't move into a check
                    self.availablepositions.append(
                        [row, col]
                    )  # Then it's a valid positin to move to so append it to the list.
                elif (
                    board[row][col][1] is not None
                    and board[row][col][1].colour != self.colour
                ):  # If there is an enemy piece
                    if (
                        self.pos_in_check([row, col], board) == False
                    ):  # If by capturing it, the king falls into check (it means that it is an illegal capture) so we make sure that's not the case
                        self.availablepositions.append([row, col])

        # Remove the original position
        if self.position in self.availablepositions:
            self.availablepositions.remove(
                self.position
            )  # Obviously the king cannot move into the same position (thats equivalent to not making a move at all) so we remove it.
        return self.availablepositions


class Queen(Piece):
    def get_legal_moves(self, board):
        # Create temporary Rook and Bishop objects at the Queen's position
        rook = Rook(position=self.position, colour=self.colour)
        bishop = Bishop(position=self.position, colour=self.colour)

        # Combine their legal moves
        self.availablepositions = rook.get_legal_moves(board) + bishop.get_legal_moves(
            board
        )
        return self.availablepositions


class Knight(Piece):
    def get_legal_moves(self, board):
        row, col = self.position
        self.availablepositions = []
        moves = [
            [row + 2, col + 1],
            [row + 2, col - 1],
            [row - 2, col + 1],
            [row - 2, col - 1],  # Vertical L
            [row + 1, col + 2],
            [row + 1, col - 2],
            [row - 1, col + 2],
            [row - 1, col - 2],
        ]  # Horizontal L

        for move in moves:
            if (
                0 <= move[0] <= 7 and 0 <= move[1] <= 7
            ):  # Check if the position actually exists on the board.
                self.availablepositions.append(move)
        return self.availablepositions


class Bishop(Piece):
    def get_legal_moves(self, board):
        row, col = self.position
        diag_pos, diag_neg, antidiag_pos, antidiag_neg = True, True, True, True
        self.availablepositions = []
        # Diagonal:
        for d in range(1, 8):
            if row + d < 8 and col + d < 8 and diag_pos == True:
                if (
                    board[row + d][col + d][1] != None
                ):  # if there is a piece in that position
                    if (
                        board[row + d][col + d][1].colour != self.colour
                    ):  # And it's an enemy piece
                        self.availablepositions.append(
                            [row + d, col + d]
                        )  # It could be captured so add that position
                    diag_pos = False  # You can no longer continue in this direction as it is blocked
                else:
                    self.availablepositions.append([row + d, col + d])

            if row - d >= 0 and col - d >= 0 and diag_neg == True:
                if board[row - d][col - d][1] != None:
                    if board[row - d][col - d][1].colour != self.colour:
                        self.availablepositions.append([row - d, col - d])
                    diag_neg = False
                else:
                    self.availablepositions.append([row - d, col - d])
        # Anti-diagonal:
        for d in range(1, 8):
            if row + d < 8 and col - d >= 0 and antidiag_neg == True:
                if board[row + d][col - d][1] != None:
                    if board[row + d][col - d][1].colour != self.colour:
                        self.availablepositions.append([row + d, col - d])
                    antidiag_neg = False
                else:
                    self.availablepositions.append([row + d, col - d])

            if row - d >= 0 and col + d < 8 and antidiag_pos == True:
                if board[row - d][col + d][1] != None:
                    if board[row - d][col + d][1].colour != self.colour:
                        self.availablepositions.append([row - d, col + d])
                    antidiag_pos = False
                else:
                    self.availablepositions.append([row - d, col + d])

        return self.availablepositions


class Rook(Piece):
    def get_legal_moves(self, board):
        row, col = self.position
        row_pos, row_neg, col_pos, col_neg = True, True, True, True

        self.availablepositions = []
        for d in range(1, 8):
            if row + d < 8 and row_pos == True:
                if board[row + d][col][1] != None:
                    # Cannot append this position (unless it's opponent piece which can be captured) and none of the next positions in this row can be added
                    if (
                        board[row + d][col][1].colour != self.colour
                    ):  # Capture opponent piece
                        self.availablepositions.append([row + d, col])
                    row_pos = False
                else:
                    self.availablepositions.append([row + d, col])

            if row - d >= 0 and row_neg == True:
                if board[row - d][col][1] != None:
                    if (
                        board[row - d][col][1].colour != self.colour
                    ):  # Capture opponent piece
                        self.availablepositions.append([row + d, col])
                    # Cannot append this position and none of the next positions in this row can be added
                    row_neg = False

                else:
                    self.availablepositions.append([row - d, col])
            if col + d < 8 and col_pos == True:
                if board[row][col + d][1] != None:
                    # Cannot append this position and none of the next positions in this col can be added
                    if (
                        board[row][col + d][1].colour != self.colour
                    ):  # Capture opponent piece
                        self.availablepositions.append([row, col + d])
                    col_pos = False

                else:
                    self.availablepositions.append([row, col + d])
            if col - d >= 0 and col_neg == True:
                if board[row][col - d][1] != None:
                    # Cannot append this position and none of the next positions in this col can be added
                    if (
                        board[row][col - d][1].colour != self.colour
                    ):  # Capture opponent piece
                        self.availablepositions.append([row, col - d])
                    col_neg = False

                else:
                    self.availablepositions.append([row, col - d])

        return self.availablepositions


class Pawn(Piece):
    # I need to add promotion ability  - This will be handled on the board
    # capturing via en-passant as well
    def get_legal_moves(self, board):
        # Assuming position of a pawn can never be row 0 or 8 . They are forced to promote .
        row, col = self.position[0], self.position[1]
        self.availablepositions = []
        if self.colour == "White":
            # Check if Diag capture is available
            if col + 1 < 8 and row + 1 < 8 and board[row + 1][col + 1][1] is not None:
                if board[row + 1][col + 1][1].colour != self.colour:
                    self.availablepositions.append([row + 1, col + 1])
            if col - 1 >= 0 and row + 1 < 8 and board[row + 1][col - 1][1] is not None:
                if board[row + 1][col - 1][1].colour != self.colour:
                    self.availablepositions.append([row + 1, col - 1])
            # Positions to move forward
            if board[row + 1][col][1] == None:
                if row == 1:
                    self.availablepositions.append([row + 1, col])
                    if board[row + 2][col][1] == None:
                        self.availablepositions.append([row + 2, col])
                else:
                    self.availablepositions.append([row + 1, col])
        else:
            # piece colour must be black
            if col + 1 < 8 and row - 1 >= 0 and board[row - 1][col + 1][1] is not None:
                if board[row - 1][col + 1][1].colour != self.colour:
                    self.availablepositions.append([row - 1, col + 1])
            if col - 1 >= 0 and row - 1 >= 0 and board[row - 1][col - 1][1] is not None:
                if board[row - 1][col - 1][1].colour != self.colour:
                    self.availablepositions.append([row - 1, col - 1])

            if board[row - 1][col][1] == None:
                if row == 6:
                    self.availablepositions.append([row - 1, col])
                    if board[row - 2][col][1] == None:
                        self.availablepositions.append([row - 2, col])
                else:
                    self.availablepositions.append([row - 1, col])

        return self.availablepositions


class Board:
    def __init__(self):
        self.board = [
            [["W", None] for _ in range(8)] for _ in range(8)
        ]  # Create an 8 x 8 board where each tile is white and contains no pieces.
        for i in range(0, 8):
            for j in range(0, 8):
                if (i + j) % 2 == 0:
                    self.board[i][j] = [
                        "B",
                        None,
                    ]  # Make a checkerboard pattern where every white tile is adjacent to a black tile.

        def setpawns(board, row, colour):
            """
            Sets up a row of pawns at the given input row and of the given input colour.
            """
            for j in range(8):
                board[row][j][1] = Pawn(position=[row, j], colour=colour)

        def set_king_row(board, row, colour):
            """
            Sets up the initial king row of a given colour. I guess we can figure out what colour it is from the given row - but it's unnecessary to add this logic in. Just type the damn colour lol.
            """
            board[row][0][1] = Rook(position=[row, 0], colour=colour)
            board[row][7][1] = Rook(position=[row, 7], colour=colour)
            board[row][1][1] = Knight(position=[row, 1], colour=colour)
            board[row][6][1] = Knight(position=[row, 6], colour=colour)
            board[row][2][1] = Bishop(position=[row, 2], colour=colour)
            board[row][5][1] = Bishop(position=[row, 5], colour=colour)
            board[row][3][1] = Queen(position=[row, 3], colour=colour)
            board[row][4][1] = King(position=[row, 4], colour=colour)

        setpawns(self.board, 1, colour="White")
        setpawns(self.board, 6, colour="Black")
        set_king_row(self.board, 0, colour="White")
        set_king_row(self.board, 7, colour="Black")

    def getboard(self):
        return self.board

    def drawboard(self):
        PIECE_SYMBOLS = {
            "Black": {
                "King": "♔",
                "Queen": "♕",
                "Rook": "♖",
                "Bishop": "♗",
                "Knight": "♘",
                "Pawn": "♙",
            },
            "White": {
                "King": "♚",
                "Queen": "♛",
                "Rook": "♜",
                "Bishop": "♝",
                "Knight": "♞",
                "Pawn": "♟",
            },
        }
        for i in range(7, -1, -1):
            row = self.board[i]
            for square in row:
                piece = square[1]
                if piece is None:
                    print(".", end=" ")
                else:
                    symbol = PIECE_SYMBOLS[piece.colour][type(piece).__name__]
                    print(symbol, end=" ")
            print()

    def update_board(self, move):
        # move = [initial_pos,final_pos]
        # initial/final pos will be of form [row,col]
        initial_row, initial_col = move[0][0], move[0][1]
        final_row, final_col = move[1][0], move[1][1]
        piece = self.board[initial_row][initial_col][1]
        self.board[initial_row][initial_col][1] = None
        piece.position = move[1]
        self.board[final_row][final_col][1] = piece


class ChessGame:
    def __init__(
        self,
    ):
        self.moves = []
        self.board = Board()
        self.colour_to_move = "White"
        self.result = None

    def get_board(self):
        # Return the current board state
        return self.board.getboard()

    def make_move(self, colour, move):
        initial_row, initial_col = move[0][0], move[0][1]
        piece = self.board.board[initial_row][initial_col][1]
        if piece == None:
            print("No piece selected!")
            return False
        elif piece.colour != colour:
            print("Its the other colour's turn")
            return False
        else:
            if move[1] in piece.get_legal_moves(board=self.board.getboard()):
                self.moves.append(move)
                self.board.update_board(move=move)
                return True

            else:
                print("Not a valid position to move")
                return False

    def is_checkmate(self, colour):
        # Find the king
        king_pos = None
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j][1]
                if isinstance(piece, King) and piece.colour == colour:
                    king_pos = [i, j]
                    king = piece
                    break
            if king_pos:
                break

        # Check if the king is in check
        in_check = king.pos_in_check(king_pos, self.board.getboard())
        if not in_check:
            return False

        # Check if the king can escape
        legal_moves = king.get_legal_moves(board=self.board.getboard())
        for move in legal_moves:
            # Simulate the move
            original_pos = king.position
            captured_piece = self.board.board[move[0]][move[1]][1]
            self.board.board[move[0]][move[1]][1] = king
            self.board.board[original_pos[0]][original_pos[1]][1] = None
            king.position = move

            # Check if the king is still in check
            king_in_check = king.pos_in_check(move, self.board.getboard())

            # Undo the move
            self.board.board[original_pos[0]][original_pos[1]][1] = king
            self.board.board[move[0]][move[1]][1] = captured_piece
            king.position = original_pos

            if not king_in_check:
                return False

        # Check if any other piece can block the check or capture the attacker
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j][1]
                if piece and piece.colour == colour:
                    legal_moves = piece.get_legal_moves(self.board.getboard())
                    for move in legal_moves:
                        # Simulate the move
                        original_pos = piece.position
                        captured_piece = self.board.board[move[0]][move[1]][1]
                        self.board.board[move[0]][move[1]][1] = piece
                        self.board.board[original_pos[0]][original_pos[1]][1] = None
                        piece.position = move

                        # Check if the king is still in check
                        king_in_check = king.pos_in_check(
                            king_pos, self.board.getboard()
                        )

                        # Undo the move
                        self.board.board[original_pos[0]][original_pos[1]][1] = piece
                        self.board.board[move[0]][move[1]][1] = captured_piece
                        piece.position = original_pos

                        if not king_in_check:
                            return False

        return True

    def play(self, move):
        def get_opp_col(col):
            if col == "White":
                return "Black"
            else:
                return "White"

        x = self.make_move(colour=self.colour_to_move, move=move)
        if self.is_checkmate(colour=get_opp_col(self.colour_to_move)):
            self.result = f"{self.colour_to_move} wins!"
            print(self.result)
        if (x):
            self.colour_to_move = get_opp_col(self.colour_to_move)

# def main():
#     TrialGame = ChessGame()
#     TrialGameboard = TrialGame.board
#     TrialGameboard.drawboard()
#     print("------------------")
#     while (TrialGame.is_checkmate("White") == False and TrialGame.is_checkmate("Black") == False):
#         user_input = input(
#             "Enter your move  in the format initial_row,initial_col,final_row,final_col: "
#         )
#         move_list = list(map(int, user_input.split(",")))
#         pairs = [move_list[i : i + 2] for i in range(0, len(move_list), 2)]
#         TrialGame.play(move=pairs)
#         TrialGameboard.drawboard()
#         print("------------------")
#     print(TrialGame.result)
# if (__name__ == "__main__"):
#     main()

