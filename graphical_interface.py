import pygame
import script
import chessAI
import random
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Window features
pygame.display.set_caption("Chess")
icon = pygame.image.load("C:\\Users\\aseem\\Dev\\Python\\Chess\\chess_icon.png")
pygame.display.set_icon(icon)
base_font = pygame.font.Font(None, 32)
user_text = ''
input_rect = pygame.Rect(0, 0, 200, 50)
Current_Game = script.ChessGame()
colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('gray15')
colour = colour_passive
active = False
count = 0

def drawboard(surface, board):
    def getcolourtuple(colour):
        if colour == 'W':
            return (255, 255, 255)
        if colour == 'B':
            return (43, 45, 48)  # Lighter shade of black

    # Calculate center position
    tile_size = 65
    BOARD_SIZE = tile_size * 8 #  65 * 8 = 520
    start_x = (800 - BOARD_SIZE) // 2  # Center horizontally  # 140
    start_y = (600 - BOARD_SIZE) // 2  # Center vertically  # 40

    def draw_rows():
        start_h = start_x - (tile_size // 2)
        start_v = start_y + (tile_size // 2)
        for i in range(8):
            text = f"{(8-i)}"
            font = pygame.font.Font(None,25)
            surface = font.render(text,True,(0,0,0))
            screen.blit(surface,(start_h,start_v + (i * tile_size)))

    def draw_cols():
        start_h = start_x + (tile_size // 2)
        start_v = start_y + BOARD_SIZE + (tile_size // 4)
        for i in range(8):
            text = f"{chr(ord('a') + i)}"
            font = pygame.font.Font(None, 25)
            surface = font.render(text, True, (0, 0, 0))
            screen.blit(surface, (start_h+ (i * tile_size), start_v) )

    draw_rows()
    draw_cols()
    for i in range(8):
        for j in range(8):
            tile_colour = board[7-i][j][0]
            x = start_x + (j * tile_size)
            y = start_y + (i * tile_size)
            pygame.draw.rect(surface, getcolourtuple(tile_colour), pygame.Rect(x, y, tile_size, tile_size))
            if board[7-i][j][1] is not None:
                piece = board[7-i][j][1]
                piece_name = type(piece).__name__
                downcased_piece_name = piece_name[0].lower() + piece_name[1:]
                piece_colour = piece.colour
                downcased_colour = piece_colour[0].lower() + piece_colour[1:]
                file_name = f"{downcased_colour}-{downcased_piece_name}"
                image = pygame.image.load("pieces-basic-png/" + file_name + ".png")
                image = pygame.transform.scale(image, (65, 65))
                surface.blit(image, (x, y))

def parse_algebraic(input):
    """
    Input should be like "a2-a4". I need to convert that into "0113" so that I could feed it into parse_move.
    """
    acceptable_rows = ['a','b','c','d','e','f','g','h']
    acceptable_cols = [1,2,3,4,5,6,7,8]

    # Check if input is valid
    try: 
        if ((input[0] not in acceptable_rows) | (input[3] not in acceptable_rows)):
            raise ValueError("Invalid input format. A valid move should be like a2-a4. Rows should be from a to h")
        elif ((int(input[1]) not in acceptable_cols) | (int(input[4]) not in acceptable_cols)):
            raise ValueError("Invalid input format. A valid move should be like a2-a4. Cols should be from a to h")
        else:
            result = [
                [(int(input[1]) - 1), (ord(input[0]) - 97)],
                [(int(input[4]) - 1), (ord(input[3]) - 97)],
            ]
            return result

    except ValueError as e:
        print(e)
        return None


def parse_move(user_input):
    """Parse the user input into a move format [[row1, col1], [row2, col2]]."""
    try:
        # Ensure the input is exactly 4 characters long (e.g., "1234")
        if len(user_input) != 4 or not user_input.isdigit():
            raise ValueError("Invalid input format. Enter 4 digits (e.g., 1234).")
        # Convert input into move format
        move = [[int(user_input[0]), int(user_input[1])], [int(user_input[2]), int(user_input[3])]]
        return move
    except ValueError as e:
        print(e)
        return None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    if user_text != '':  # If there is no text.
                        user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Process the move when Enter is pressed
                    #moves = chessAI.GetAllLegalMoves(board=Current_Game.get_board(),colour=Current_Game.colour_to_move)
                    #print(moves)
                    #move = random.choice(moves)
                    #print("----")
                    #print(move)
                    move = parse_algebraic(user_text)
                    if move:
                        # if not Current_Game.is_checkmate(Current_Game.colour_to_move):
                        #if (count < 5):
                        Current_Game.play(move)
                        board_state = Current_Game.get_board()
                        drawboard(screen, board_state)
                        count += 1
                    else:
                            running = False
                    user_text = ''  # Reset user_text for the next move
                else:
                    user_text += event.unicode

    screen.fill((0, 245, 220))

    # Draw the input box
    if active:
        colour = colour_active
    else:
        colour = colour_passive
    pygame.draw.rect(screen, colour, input_rect, 2)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Draw the board
    board_state = Current_Game.get_board()
    drawboard(screen, board_state)

    pygame.display.update()
