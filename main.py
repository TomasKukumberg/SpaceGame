import pygame
from pygame import mixer
import random
import math

# Initiliaze the pygame lib
pygame.init()

# Create the screen
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))

# Background
bg = pygame.image.load("background.png")

# Background sound
mixer.music.load('background.wav')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Title and logo
pygame.display.set_caption("Space Game")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("rocket.png")
playerX = screenX * 0.45
playerY = (5 / 6) * screenY
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# load all enemies
# could be reworked for consts to not append them
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - u can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score and font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True

# Game loop that exits if users clicks the X button in the window
while running:

    screen.fill((0, 0, 0))  # RGB
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # if any key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.set_volume(0.3)
                    bullet_sound.play()
                    bulletX = playerX  # get the current x coordinate of the spaceship
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # if any key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # if left or right arrow is released
                playerX_change = 0

    playerX += playerX_change

    # Checking for boundaries of space
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # make enemies disappear after crashing
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.set_volume(0.3)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
