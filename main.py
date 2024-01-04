import pygame
from actors import Player, Computer, Ball

#Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 40
PADDLE_HEIGHT = 200
PADDLE_COLOR = "white"
PADDLE_VELOCITY = 5
PADDLE_CENTER_POS = (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2)
PLAYER_LEFT_POS = 10
COMPUTER_LEFT_POS = SCREEN_WIDTH - PADDLE_WIDTH - PLAYER_LEFT_POS
BALL_COLOR = "white"
BALL_WIDTH = 20
BALL_HEIGHT = 20
BALLX = int(SCREEN_WIDTH / 2)
BALLY = int(SCREEN_HEIGHT / 2)
BALL_BORDER = 8
RADIUS = 12
BALL_VELOCITY = 5

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True



# Game Objects
player = Player()
computer = Computer()
ball = Ball()

#Helper functions


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, PADDLE_COLOR, player)
    pygame.draw.rect(screen, PADDLE_COLOR, computer)
    pygame.draw.rect(screen, BALL_COLOR, ball, border_radius= BALL_BORDER )
    player.handle_movement()
    computer.handle_movement(ball)
    ball.handle_movement()
    ball.check_collision(player, computer)

    # Check collision
  


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)# limits FPS to 60

pygame.quit()

