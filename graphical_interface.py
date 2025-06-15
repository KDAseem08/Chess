import pygame
import script

pygame.init()
screen = pygame.display.set_mode((800,600))

# Window features
pygame.display.set_caption("Chess")
icon = pygame.image.load("/Users/aseem/Dev/Python/ChessGame/chess_icon.png")
pygame.display.set_icon(icon)


Current_Game  = script.ChessGame(surface = screen) 


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,255,255))
    Current_Game.play()
    
    pygame.display.update()


