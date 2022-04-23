import math
import random

import pygame
from pygame import mixer

# initialise the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerXchange = 0
# playerYchange = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(1)
    enemyYchange.append(40)

    # Bullet
    # Ready - you can't see the bullet on screen
    # Fire - The bullet is currently moving
    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletXchange = 0
    bulletYchange = 10
    bullet_state = "ready"

    # score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    textY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
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


# infinite game loop so that screen doesn't close
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether is right or left

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerXchange = -5

            if event.key == pygame.K_RIGHT:
                playerXchange = 5
            # if event.key == pygame.K_UP:
            #     print("Dp key pressed")
            #     playerYchange = -5

            # if event.key == pygame.K_DOWN:
            #     print("Down key pressed")
            #     playerYchange = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # get current x of ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #     print("Keystroke has been released")
            #     playerYchange = 0
    # spaceship boundary
    playerX += playerXchange
    # playerY += playerYchange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # if playerY < 0:
    #     playerY = 0
    # elif playerY > 536:
    #     playerY = 536

    # enemy movement

    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 2
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 736:
            enemyXchange[i] = -2
            enemyY[i] += enemyYchange[i]

        # if enemyY[i] < 0:
        #     enemyXchange[i] = 1
        #     enemyY[i] -= enemyYchange[i]
        # elif enemyY[i] > 536:
        #     enemyXchange[i] = -1
        #     enemyY[i] -= enemyYchange[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange

    if bulletY < 0:
        bulletY = playerY
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


