import pygame
from config import *
from manager import Scene_Manager


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.manager = Scene_Manager()
    
    def run(self):
        while self.running:

            self.screen.fill(SCREEN_COLOR)
            
            self.manager.scene.render(self.screen)
            self.handle_events()
            self.manager.scene.update()

            pygame.display.flip()

            self.clock.tick(FPS)
            
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.manager.scene.handle_events(event)