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
        self.x = left
        self.y = top
        self.width = width
        self.height = height
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
        if keys[pygame.K_UP] and self.top > 10:
            self.move_up()
        if keys[pygame.K_DOWN] and self.top < SCREEN_HEIGHT - self.height - 10:
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
        self.x = left
        self.y = top

    def handle_movement(self, ball: pygame.Rect):
        middleCoord = self.y + self.height / 2
        if ball.dir_x < 0 and self.y:
            if middleCoord < SCREEN_HEIGHT / 2:
                self.move_down()
            if middleCoord > SCREEN_HEIGHT / 2:
                self.move_up()

        elif ball.dir_x > 0:
            if ball.y < middleCoord and self.y > 10:
                self.move_up()
            if ball.y > middleCoord and self.y < SCREEN_HEIGHT - self.height - 10:
                self.move_down()

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
        self.x = left
        self.y = top
        self.width = width
        self.height = height
        self.velocity = BALL_VELOCITY
        self.angle = radians(0)
        self.dir_x = cos(self.angle)
        self.dir_y = -sin(self.angle)

    def check_collision(self, 
                        player: Player, 
                        computer: Computer):
        
        intersectY = self.y

        if self.top >= SCREEN_HEIGHT or self.top <= 0:
            self.velocity *= 1.02
            self.dir_y *= -1
        
        if self.colliderect(player):
            self.velocity *= 1.02
            relative_intersectY = (player.y + (player.height/2)) - intersectY
            normalized_relative_intersect_y = relative_intersectY / (player.height/2)
            self.angle = radians(normalized_relative_intersect_y * 60)
            self.dir_x = cos(self.angle)
            self.dir_y = -sin(self.angle)
            

        if self.colliderect(computer):
            self.velocity *= 1.02
            relative_intersectY = (computer.y + (computer.height/2)) - intersectY
            normalized_relative_intersect_y = relative_intersectY / (computer.height/2) 
            self.angle = radians(normalized_relative_intersect_y * 60)
            self.dir_x = -cos(self.angle)
            self.dir_y = sin(self.angle)

    def handle_movement(self):
        self.x += self.dir_x * self.velocity
        self.y += self.dir_y * self.velocity
    
    