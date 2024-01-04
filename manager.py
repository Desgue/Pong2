import pygame
from actors import *
from config import *
class Manager(object):
    def __init__(self):
        pass

class Game_Scene():
    def __init__(self,
                 surface: pygame.Surface,
                 player: Player = Player(),
                 computer: Computer = Computer(),
                 ball: Ball = Ball()):
        
        self.surface = surface
        self.player = player
        self.computer = computer
        self.ball = ball

    def render(self):
        pygame.draw.rect(self.surface, PADDLE_COLOR, self.player)
        pygame.draw.rect(self.surface, PADDLE_COLOR, self.computer)
        pygame.draw.rect(self.surface, BALL_COLOR, self.ball, border_radius= BALL_BORDER )
    
    def update(self):
        self.ball.check_collision(self.player, self.computer)
        self.player.handle_movement()
        self.computer.handle_movement(self.ball)
        self.ball.handle_movement()
