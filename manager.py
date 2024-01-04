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
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.surface = surface
        self.player = player
        self.computer = computer 
        self.ball = ball
        
    


    def render(self):
        self.player_score=self.font.render("{}".format(self.player.score),1,pygame.Color("white"))
        self.enemy_score=self.font.render("{}".format(self.computer.score),1, pygame.Color("white")) 
        self.surface.blit(self.player_score,(SCREEN_WIDTH / 4,SCREEN_HEIGHT/4))
        self.surface.blit(self.enemy_score,(SCREEN_WIDTH - SCREEN_WIDTH / 4, SCREEN_HEIGHT/4))
        pygame.draw.rect(self.surface, PADDLE_COLOR, self.player)
        pygame.draw.rect(self.surface, PADDLE_COLOR, self.computer)
        pygame.draw.rect(self.surface, BALL_COLOR, self.ball, border_radius= BALL_BORDER )
    
    def update(self):

        self.ball.check_collision(self.player, self.computer)
        self.player.handle_movement()
        self.computer.handle_movement(self.ball)
        self.ball.handle_movement()
        self.handle_point(self.ball, self.player, self.computer)
    
    def reset(self, dir: int = 1):
        self.ball = Ball()
        


    def handle_point(self,ball: Ball, player: Player, computer: Computer):
        if ball.x <= 0:
            computer.score += 1
            print("goal")
            self.reset(-1)
        if ball.x >= SCREEN_WIDTH:
            player.score += 1
            self.reset()
        
        
