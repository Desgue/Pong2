import pygame
from actors import *
from config import *

class Menu_Scene():
    def __init__(self):

        self.init()

    def init(self):
        self.font = pygame.font.SysFont('Arial', 56)
        self.start_button = Button(image = PLAY_BUTTON_SM, hover_image = PLAY_BUTTON_SM_HOVER)

    def handle_events(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or self.start_button.clicked() :
            self.manager.go_to(Game_Scene().new())  

    def render(self, screen):
        screen.fill("black")
        self.draw_name_text(screen, (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 4))
        self.start_button.draw(screen, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            
    def update(self):
        pass
        
    def draw_name_text(self, screen, pos):
        game_name = self.font.render("Pong: The Remake", False, "white")
        game_name_rect = game_name.get_rect()
        game_name_rect.center = pos
        screen.blit(game_name, game_name_rect)

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
        self.game_over = False
        self.paused = False
    
    def new(self):
        self.player = Player()
        self.computer = Computer()
        self.ball = Ball()
        self.paused = False
        self.game_over = False
        return self

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.ball.start()
    
    def render(self, screen):
        if self.game_over:
            self.manager.go_to(Game_Over_Scene())
            return
        if self.paused:
            self.manager.go_to(Paused_Scene(self))
            return
        
        self.draw_scoreboard(screen)
        self.draw_actors(screen)

    def update(self):
        self.ball.check_collision(self.player, self.computer)
        self.player.handle_movement()
        self.computer.handle_movement(self.ball)
        self.ball.handle_movement()
        self.handle_point(self.ball, self.player, self.computer)


    def draw_scoreboard(self, screen):
        self.player_score=self.font.render("{}".format(self.player.score),1,pygame.Color("white"))
        self.enemy_score=self.font.render("{}".format(self.computer.score),1, pygame.Color("white")) 
        screen.blit(self.player_score,(SCREEN_WIDTH / 4,SCREEN_HEIGHT/4))
        screen.blit(self.enemy_score,(SCREEN_WIDTH - SCREEN_WIDTH / 4, SCREEN_HEIGHT/4))
    
    def draw_actors(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.player, border_radius= 8)
        pygame.draw.rect(screen, PADDLE_COLOR, self.computer, border_radius= 8)
        pygame.draw.rect(screen, BALL_COLOR, self.ball, border_radius= BALL_BORDER ) 
    
        
    def handle_point(self,ball: Ball, player: Player, computer: Computer):
        if ball.x <= 0:
            computer.score += 1
            ball.reset(-1)
            if computer.score >= 2:
                self.game_over = True
        if ball.x >= SCREEN_WIDTH:
            player.score += 1
            ball.reset()


class Paused_Scene():
    def __init__(self, current_game):
        self.big_font = pygame.font.SysFont('Arial', 56)
        self.current_game = current_game
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.current_game.paused = False
            self.manager.go_to(self.current_game)

    def render(self, screen):
        screen.fill("black")
        paused_text = self.big_font.render("PAUSED", False, "white")
        paused_text_rect = paused_text .get_rect()
        paused_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        screen.blit(paused_text, paused_text_rect)

    def update(self):
        pass

class Game_Over_Scene():
    def __init__(self):
        self.big_font = pygame.font.SysFont('Arial', 56)
        self.small_font = pygame.font.SysFont('Arial', 36)
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.manager.go_to(Menu_Scene())

    def render(self, screen):
        screen.fill("black")
        game_over_text = self.big_font.render("GAME OVER", False, "white")
        game_over_text_rect = game_over_text .get_rect()
        game_over_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        screen.blit(game_over_text, game_over_text_rect)

        restart_text = self.small_font.render("Press SPACE to restart", False, "white")
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 300)
        screen.blit(restart_text, restart_text_rect)

    def update(self):
        pass

class Player_Won_Scene():
    def __init__(self):
        pass
    
    def handle_events(self):
        pass
    def render(self):
        pass
    def update(self):
        pass
        
        
class Scene_Manager():
    def __init__(self):
        self.go_to(Menu_Scene())
    def go_to(self, scene):
        if hasattr(self, "scene"): del self.scene
        self.scene = scene
        self.scene.manager = self
