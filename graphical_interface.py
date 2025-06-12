import pygame
import script

pygame.init()
screen = pygame.display.set_mode((800,600))

# Window features
pygame.display.set_caption("Chess")
icon = pygame.image.load("/Users/aseem/Dev/Python/ChessGame/chess_icon.png")
pygame.display.set_icon(icon)



def drawboard(board):
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
            tile_colour = board[i][j][0]
            x = start_x + (j * tile_size)
            y = start_y + (i * tile_size) 
            pygame.draw.rect(screen, getcolourtuple(tile_colour), pygame.Rect(x, y, tile_size, tile_size))
            if (board[i][j][1] != None):
                piece = board[i][j][1]
                piece_name = (type(piece).__name__)
                downcased_piece_name = piece_name[0].lower() + piece_name[1:]
                piece_colour = piece.colour
                downcased_colour = piece_colour[0].lower() + piece_colour[1:]
                file_name = f"{downcased_colour}-{downcased_piece_name}"   
                image = pygame.image.load("ChessGame/pieces-basic-png/" + file_name + ".png")
                image = pygame.transform.scale(image, (65, 65))
                screen.blit(image, (x,y))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,255,255))
    Current_Game  = script.ChessGame()
    Board = Current_Game.board
    drawboard(board = Board.getboard())
    pygame.display.update()


