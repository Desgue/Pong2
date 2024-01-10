import pygame
import random
import json
from actors import *
from config import *

class Scene:
    def __init__(self) -> None:
        pygame.font.init()
        self.header_font = pygame.font.SysFont('Copmic Sans MS', 56)
        self.sub_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.last_score = 0
        self.high_score = self.get_highscore()

    def handle_events(self):
        pass
    def render(self):
        pass
    def update(self):
        pass
    
    def get_highscore(self):
        with open(HIGHSCORE_PATH, "r") as f:
            data = json.load(f)
            f.close()
            return int(data["highscore"])
        
    def save_highscore(self, new_score):
        with open(HIGHSCORE_PATH, "w") as f:
            data = {"highscore": new_score}
            json.dump(data, f)
            f.close()
        return


class Menu_Scene(Scene):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
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
        game_name = self.header_font.render("Pong: The Remake", False, "white")
        game_name_rect = game_name.get_rect()
        game_name_rect.center = pos
        screen.blit(game_name, game_name_rect)

class Game_Scene(Scene):
    def __init__(self):
        self.new()
        super().__init__()
    def new(self):
        self.player = Player()
        self.computer = Computer()
        self.ball = Ball()
        self.final_score = 5
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
        self.handle_point()


    def draw_scoreboard(self, screen):
        self.player_score_text =self.sub_font.render("{}".format(self.player.score),1,pygame.Color("white"))
        screen.blit(self.player_score_text,(SCREEN_WIDTH / 4, SCREEN_HEIGHT/4))

        self.enemy_score_text =self.sub_font.render("{}".format(self.computer.score),1, pygame.Color("white")) 
        screen.blit(self.enemy_score_text,(SCREEN_WIDTH - SCREEN_WIDTH / 4, SCREEN_HEIGHT/4))

        self.high_score_text = self.sub_font.render("Highscore: {}".format(self.high_score),1, pygame.Color("white"))
        high_score_text_rect = self.high_score_text.get_rect()
        screen.blit(self.high_score_text,(SCREEN_WIDTH  / 2  -  high_score_text_rect.centerx, SCREEN_HEIGHT - 200))
    
    def draw_actors(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.player, border_radius= 8)
        pygame.draw.rect(screen, PADDLE_COLOR, self.computer, border_radius= 8)
        pygame.draw.rect(screen, BALL_COLOR, self.ball, border_radius= BALL_BORDER )
    
    def increase_difficulty(self):
        rand = random.randint(0,5)
        match rand:
            case 0:
                self.player.height *= 0.90
            case 1: 
                self.computer.velocity *= 1.05
            case 2:
                self.computer.height *= 1.10
            case 3: 
                self.ball.velocity *= 1.01
        return
    
    def handle_point(self):
        if self.ball.x <= 0:
            self.computer.score += 1
            self.ball.reset(-1)
            if self.computer.score >= self.final_score:
                if self.player.score > self.high_score:
                    self.save_highscore(self.player.score)
                self.game_over = True

        if self.ball.x >= SCREEN_WIDTH:
            self.player.score += 1
            self.ball.reset()
            self.increase_difficulty()


class Paused_Scene(Scene):
    def __init__(self, current_game: Game_Scene):
        super().__init__()
        self.current_game = current_game
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.current_game.paused = False
            self.manager.go_to(self.current_game)

    def render(self, screen):
        screen.fill("black")
        paused_text = self.header_font.render("PAUSED", False, "white")
        paused_text_rect = paused_text .get_rect()
        paused_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        screen.blit(paused_text, paused_text_rect)

    def update(self):
        pass

class Game_Over_Scene(Scene):
    def __init__(self):
        super().__init__()
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.manager.go_to(Menu_Scene())

    def render(self, screen):
        screen.fill("black")
        game_over_text = self.header_font.render("GAME OVER", False, "white")
        game_over_text_rect = game_over_text .get_rect()
        game_over_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        screen.blit(game_over_text, game_over_text_rect)

        restart_text = self.sub_font.render("Press SPACE to restart", False, "white")
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
        
        

