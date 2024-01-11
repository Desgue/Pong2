import pygame
from math import cos, sin, radians
from config import *

class Paddle(pygame.Rect):
    def __init__(self,
                  left:float,
                  top: float,
                  width: float = PADDLE_WIDTH,
                  height: float = PADDLE_HEIGHT,
                 ):
        
        super().__init__(left,
                         top,
                         width,
                         height)
        
        self.velocity = PADDLE_VELOCITY
        self.score = 0

    def move_up(self):
        self.y -= self.velocity
    def move_down(self):
        self.y += self.velocity
        

class Player(Paddle):
    def __init__(self,
                  left:float = PLAYER_LEFT_POS,
                  top: float = PADDLE_CENTER_POS,
                  width: float = PADDLE_WIDTH,
                  height: float = PADDLE_HEIGHT
                  ):
        
        super().__init__(left,
                         top,
                         width,
                         height
                         )


    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y > 10:
            self.move_up()
        if keys[pygame.K_s] and self.top < SCREEN_HEIGHT - self.height - 10:
            self.move_down()

class Computer(Paddle):
    def __init__(self,
                  left:float = COMPUTER_LEFT_POS,
                  top: float = PADDLE_CENTER_POS,
                  width: float = PADDLE_WIDTH,
                  height: float = PADDLE_HEIGHT
                  ):
        
        super().__init__(left,
                         top,
                         width,
                         height
                         )
    def handle_movement(self, ball: pygame.Rect):
        if ball.dir_x < 0 and self.y:
            if self.centery < SCREEN_HEIGHT / 2:
                self.move_down()
            if self.centery > SCREEN_HEIGHT / 2:
                self.move_up()
        else:
            if self.centery < ball.centery and self.bottom < SCREEN_HEIGHT - 10 :
                self.move_down()
            elif self.centery > ball.centery and self.top >10:
                self.move_up()


class Ball(pygame.Rect):
    def __init__(self,
                 left:float = BALLX,
                 top: float = BALLY,
                 width: float = BALL_WIDTH,
                 height: float = BALL_HEIGHT,
                 ):
        super().__init__(left,
                         top,
                         width,
                         height)

        self.start_velocity = 0        
        self.velocity = BALL_VELOCITY
        self.game_started = False
        self.angle = radians(0)
        self.dir_x = cos(self.angle)
        self.dir_y = -sin(self.angle)

    def start(self):
        self.game_started = True

    def reset(self, direction = 1):
        self.angle = radians(0)
        self.dir_x = cos(self.angle) * direction
        self.dir_y = -sin(self.angle) * direction
        self.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.game_started = False

    def check_collision(self, 
                        player: Player, 
                        computer: Computer):
        
        intersectY = self.y
        
        if self.top >= SCREEN_HEIGHT or self.top <= 0:
            self.velocity *= 1.005
            self.dir_y *= -1
        
        if self.colliderect(player):
            self.velocity *= 1.005
            relative_intersectY = (player.y + (player.height/2)) - intersectY
            normalized_relative_intersect_y = relative_intersectY / (player.height/2)
            self.angle = radians(normalized_relative_intersect_y * 60)
            self.dir_x = cos(self.angle)
            self.dir_y = -sin(self.angle)
            

        if self.colliderect(computer):
            self.velocity *= 1.01
            relative_intersectY = (computer.y + (computer.height/2)) - intersectY
            normalized_relative_intersect_y = relative_intersectY / (computer.height/2) 
            self.angle = radians(normalized_relative_intersect_y * 60)
            self.dir_x = -cos(self.angle)
            self.dir_y = sin(self.angle)

    def handle_movement(self):
        if self.game_started:
            self.x += self.dir_x * self.velocity 
            self.y += self.dir_y * self.velocity
        else:
            self.x += self.dir_x * self.start_velocity
            self.y += self.dir_y * self.start_velocity
    
class Button():
    def __init__(self, image = None, hover_image = None):
        self.image_src = image
        self.hover_image_src = hover_image
        self.image = pygame.image.load(self.image_src)
        self.rect = self.image.get_rect()
    
    def draw(self, screen: pygame.Surface, pos: tuple):
        
        self.rect.center = pos
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.image.load(self.hover_image_src)
            self.rect = self.image.get_rect()
            self.rect.center = pos
            screen.blit(self.image, self.rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
        else:
            self.image = pygame.image.load(self.image_src)
            self.rect = self.image.get_rect()
            self.rect.center = pos
            screen.blit(self.image, self.rect)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            
    
    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse_pos):
                return True
        