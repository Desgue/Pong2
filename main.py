import pygame
from actors import *
from config import FPS
from manager import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
manager = Scene_Manager()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(SCREEN_COLOR)

    # RENDER YOUR GAME HERE
    manager.scene.render(screen)
    manager.scene.handle_events(pygame.event.get())
    manager.scene.update()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)# limits FPS to 60

pygame.quit()

