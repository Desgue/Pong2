import pygame
from actors import *
from config import *

class Menu_Scene():
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 56)
        
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and (e.key == pygame.K_SPACE or e.key == pygame.K_ESCAPE):
                self.manager.go_to(Game_Scene())  
            
    def render(self, screen):
        screen.fill("black")
        game_name = self.font.render("Pong: The Remake", False, "white")
        instructions = self.font.render('> press space to start <', True, "white")
        screen.blit(game_name, (SCREEN_WIDTH / 2 - game_name.get_width() /2, SCREEN_HEIGHT / 4))
        screen.blit(instructions, (SCREEN_WIDTH / 2 - instructions.get_width() /2, SCREEN_HEIGHT / 2))

    def update(self):
        pass
        
    

class Game_Scene():
    def __init__(self,
                 player: Player = Player(),
                 computer: Computer = Computer(),
                 ball: Ball = Ball()):
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.player = player
        self.computer = computer 
        self.ball = ball
        
    

    def __render_scoreboard(self, surface):
        self.player_score=self.font.render("{}".format(self.player.score),1,pygame.Color("white"))
        self.enemy_score=self.font.render("{}".format(self.computer.score),1, pygame.Color("white")) 
        surface.blit(self.player_score,(SCREEN_WIDTH / 4,SCREEN_HEIGHT/4))
        surface.blit(self.enemy_score,(SCREEN_WIDTH - SCREEN_WIDTH / 4, SCREEN_HEIGHT/4))
    
    def __render_actors(self, surface):
        pygame.draw.rect(surface, PADDLE_COLOR, self.player, border_radius= 8)
        pygame.draw.rect(surface, PADDLE_COLOR, self.computer, border_radius= 8)
        pygame.draw.rect(surface, BALL_COLOR, self.ball, border_radius= BALL_BORDER )


    def render(self, surface):
        self.__render_scoreboard(surface)
        self.__render_actors(surface)

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
    def handle_events(self, events ):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.manager.go_to(Menu_Scene())

        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.manager.go_to(Menu_Scene())
        
        
        
class Scene_Manager():
    def __init__(self):
        self.go_to(Menu_Scene())
    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
