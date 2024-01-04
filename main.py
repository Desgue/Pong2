import pygame, game

#Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 40
PADDLE_HEIGHT = 200
PADDLE_COLOR = "white"
BALL_COLOR = "white"
BALLX = int(SCREEN_WIDTH / 2)
BALLY = int(SCREEN_HEIGHT / 2)
RADIUS = 12
BALL_VELOCITY = 5

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True



# Game Objects
player_model = game.Player(screen, PADDLE_WIDTH, PADDLE_HEIGHT)
computer_model = game.Computer(screen, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_model = game.Ball(screen,
                 color =BALL_COLOR, 
                 x = BALLX,
                 y= BALLY,
                 radius = RADIUS,
                 velocity= BALL_VELOCITY
                 )


#Helper functions

x = 600

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    player = player_model.draw()
    computer = computer_model.draw()
    ball = ball_model.draw()
    
    player_model.handle_movement()
    ball_model.handle_movement()

    # Check collision
    if ball.colliderect(computer) or ball.colliderect(player):
        ball_model.invert_direction()


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)# limits FPS to 60

pygame.quit()

