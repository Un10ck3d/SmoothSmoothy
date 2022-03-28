# Make game with pygame
import pygame
import random
from pygame.locals import *
import os

def DrawScore(text, score, color, space):
    text = f'{text}: ' + str(score)
    textSurface = pygame.font.Font('OpenSans-Bold.ttf', 32).render(text, True, WHITE, color)
    textRect = textSurface.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery + space
    windowSurface.blit(textSurface, textRect)

def StopLeavingScreen(object):
    if object.left < 0:
        object.left = 0
    elif object.right > 500:
        object.right = 500
    if object.top < 0:
        object.top = 0
    elif object.bottom > 400:
        object.bottom = 400

# Initialize pygame
pygame.init()

# Craete highscore.txt if it doesn't exist
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

# Load highscore from file
with open("highscore.txt", "r") as f:
    highscore = float(f.read())

# Set up the window
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Hello world!')

#Make window fullscreen 
pygame.display.set_mode((500, 400), pygame.FULLSCREEN)

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up variables
score = 0
last_score = 0
size = 1
time_left = 10000

x = 40
y = 60
xx = 60
yy = 40

# Create enemy
enemy = pygame.Rect(250, 300, 32, 32)
# Create target
target = pygame.Rect(200, 200, 64, 64)

# Start render loop
while True:
    # Create player
    player = pygame.Rect(xx, yy, x * size, y * size)
    pygame.draw.rect(windowSurface, BLUE, player)

    # Check for the QUIT event
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == K_RETURN or event.key == K_r:
                time_left = 10000
                score = 0
                size = 1

    # Clear screen
    windowSurface.fill(WHITE)

    # Decrease time_left every second
    time_left -= 1

    # Randomly move enemy ball
    enemy.x += random.randint(-3, 3)
    enemy.y += random.randint(-3, 3)

    # Randomly move target ball
    target.x += random.randint(-5, 5)
    target.y += random.randint(-5, 5)

    # Check for enemy collisions
    if player.colliderect(enemy):
        # Invert screeen colors
        windowSurface.fill(RED)
        # increase score by 1
        score -= 2
        size -= 0.0001

    # Check for enemy collisions
    if player.colliderect(target):
        # Invert screeen colors
        windowSurface.fill(BLACK)
        # increase score by 1
        score += 1
        size += 0.00005

    # Draw score
    DrawScore('Score', score, RED, 0)
    # Draw highscore
    DrawScore('Highscore', highscore, GREEN, 50)
    # Draw time left  
    DrawScore('Time left', time_left, BLUE, 100)
    # Draw last_score
    DrawScore('Last score', last_score, BLACK, 150)

    # If score is higher than highscore set highscore to score
    if score > highscore:
        highscore = score
        with open('highscore.txt', 'w') as f:
            f.write(str(highscore))

    # Player movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            xx -= 1
        elif event.key == pygame.K_a:
            xx -= 1
        elif event.key == pygame.K_RIGHT:
            xx += 1
        elif event.key == pygame.K_UP:
            yy -= 1
        elif event.key == pygame.K_DOWN:
            yy += 1

    # Stop player from leaving the screen
    StopLeavingScreen(player)

    # stop enemy from leaving the screen
    StopLeavingScreen(enemy)

    # stop target from leaving the screen
    StopLeavingScreen(target)
    
    # restart game
    if time_left == 0:
        last_score = score
        time_left = 10000
        windowSurface.fill(RED)
        # update highscore
        if highscore < score:
            highscore = score
        score = 0
        # save highscore to file
        with open('highscore.txt', 'w') as f:
            f.write(str(highscore))
        size = 1

    # Draw objects
    pygame.draw.rect(windowSurface, BLUE, player)
    pygame.draw.rect(windowSurface, RED, enemy)
    pygame.draw.rect(windowSurface, GREEN, target)
    # Draw the window onto the screen
    pygame.display.update()