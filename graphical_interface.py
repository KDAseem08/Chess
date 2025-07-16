import pygame
import script

pygame.init()
screen = pygame.display.set_mode((800,600))

# Window features
pygame.display.set_caption("Chess")
icon = pygame.image.load("/Users/aseem/Dev/Python/ChessGame/chess_icon.png")
pygame.display.set_icon(icon)
base_font = pygame.font.Font(None,32)
user_text = ''
input_rect = pygame.Rect(0,0,200,50)
Current_Game  = script.ChessGame() 
colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('gray15')
colour = colour_passive
active = False


def drawboard(surface, board):
    def getcolourtuple(colour):
        if colour == 'W':
            return (255, 255, 255)
        if colour == 'B':
            return (43, 45, 48)  # Lighter shade of black

    # Calculate center position
    tile_size = 65
    BOARD_SIZE = tile_size * 8
    start_x = (800 - BOARD_SIZE) // 2  # Center horizontally
    start_y = (600 - BOARD_SIZE) // 2  # Center vertically

    for i in range(8):
        for j in range(8):
            tile_colour = board[i][j][0]
            x = start_x + (j * tile_size)
            y = start_y + (i * tile_size)
            pygame.draw.rect(surface, getcolourtuple(tile_colour), pygame.Rect(x, y, tile_size, tile_size))
            if board[i][j][1] is not None:
                piece = board[i][j][1]
                piece_name = type(piece).__name__
                downcased_piece_name = piece_name[0].lower() + piece_name[1:]
                piece_colour = piece.colour
                downcased_colour = piece_colour[0].lower() + piece_colour[1:]
                file_name = f"{downcased_colour}-{downcased_piece_name}"
                image = pygame.image.load("ChessGame/pieces-basic-png/" + file_name + ".png")
                image = pygame.transform.scale(image, (65, 65))
                surface.blit(image, (x, y))

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
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                    if user_text != '': # If there is no text.
                        user_text = user_text[:-1]
                else:
                    user_text += event.unicode 
    screen.fill((0,255,255))
    if active:
        colour = colour_active
    else:
        colour_passive
    pygame.draw.rect(screen,colour,input_rect,2)
    text_surface = base_font.render(user_text,True,(255,255,255))
    screen.blit(text_surface,(input_rect.x+5,input_rect.y +5))
    board_state = Current_Game.get_board()
    drawboard(screen, board_state)

    
    pygame.display.update()


