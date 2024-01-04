import pygame

class Paddle(pygame.Rect):
    def __init__(self,
                 surface: pygame.Surface,  
                 width: float,
                 height: float):
        self.surface = surface
        self.width = width
        self.height = height
        self.load()
        
    def load(self):
        self.speed = 5
        self.left = 0
        self.top = self.__calculate_center_pos()
        self.left_padding = 10
        self.right_padding = self.surface.get_width() - self.width - 10

    def move_up(self):
        if self.top > 20:
            self.top -= self.speed

    def move_down(self):
        if self.top <= self.surface.get_height() - self.height - 20:
            self.top += self.speed

    def draw(self):
        return pygame.draw.rect(self.surface, "white", self)

    def __calculate_center_pos(self):
        mid_screen = self.surface.get_height() / 2 
        mid_rect =  self.height / 2
        return mid_screen - mid_rect
    

class Player(Paddle):
    def __init__(self,
                 surface: pygame.Surface,  
                 width: float,
                 height: float):
        super().__init__(
                 surface, 
                 width,
                 height)
        self.left += self.left_padding

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            Paddle.move_up(self)
        if keys[pygame.K_DOWN]:
            Paddle.move_down(self)
    

class Computer(Paddle):
    def __init__(self,
                 surface: pygame.Surface,  
                 width: float,
                 height: float):
    
        super().__init__(
                 surface, 
                 width,
                 height)
        
        self.left += self.right_padding

class Ball(pygame.Rect):
    def __init__(self,
                 surface: pygame.Surface, 
                 color: str, 
                 x: int, 
                 y: int, 
                 radius: int,
                 velocity: int):
    
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity

    def draw(self):
        return pygame.draw.circle(self.surface, 
                                  self.color, 
                                  (self.x, self.y), 
                                  self.radius)
    def handle_movement(self):
        self.x += self.velocity
        self.y += self.velocity
    def invert_direction(self):
        self.acceleration *= -1
        