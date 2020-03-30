import pygame
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
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemyX_change = 4
enemyY_change = 40

# Bullet

# Ready - u can't see the bullet on the screen
# Fire - the bullet is currently moving

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


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
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
