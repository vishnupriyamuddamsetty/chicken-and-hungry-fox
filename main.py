import pygame
import random
import math
from pygame import mixer

#initialization
pygame.init()
#create the screen
screen = pygame.display.set_mode((800,600))
#sound
mixer.music.load("background.mp3")
mixer.music.play(-1)


#background
background = pygame.image.load('background.png')
#caption and logo
pygame.display.set_caption("CHICKEN AND HUNGRY FOXES")
icon = pygame.image.load('chickenicon.png')
pygame.display.set_icon(icon)
#chicken
chickenImg = pygame.image.load('chicken.png')
chickenX = 370
chickenY = 480
chickenX_change = 0


#fox
foxImg = []
foxX = []
foxY = []
foxX_change=[]
foxY_change=[]
num_of_foxes = 9

for i in range(num_of_foxes):
    foxImg.append(pygame.image.load('fox.png'))
    foxX.append(random.randint(0,736))
    foxY.append(random.randint(50,150))
    foxX_change.append(4)
    foxY_change.append(40)



#balloon
#ready -you can't see the balloon on screen
#thrown- the balloon is currently moving

balloonImg = pygame.image.load('balloon.png')
balloonX = 0
balloonY = 480
balloonX_change = 0
balloonY_change = 10
balloon_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


#Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = font.render("GAME OVER!!", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def show_score(x,y):
    score = font.render("ScorePoints:" +str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))






def chicken(x,y):
    screen.blit(chickenImg, (x,y))

def balloon(x,y):
    global balloon_state
    balloon_state = "thrown"
    screen.blit(balloonImg, (x,y))




def fox(x,y,i):
    screen.blit(foxImg[i], (x,y))

def iscollision(foxX, foxY, balloonX, balloonY):
    distance = math.sqrt(math.pow(foxX - balloonX, 2) + (math.pow(foxY - balloonY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Game loop
running = True
while running:
    #RGB is Red,Blue,Green
    screen.fill((0,0,0))
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #when we close button
            running = False

        if event.type == pygame.KEYDOWN:
            #keydown means pressing key
            if event.key == pygame.K_LEFT:
               chickenX_change = -5
            if event.key == pygame.K_RIGHT:
                chickenX_change = 5
            if event.key == pygame.K_SPACE:
                if balloon_state == "ready":
                    balloonSound = mixer.Sound("laser.wav")
                    balloonSound.play()
                    #get the current x coordinate of the spaceship
                    balloonX = chickenX
                    balloon(balloonX, balloonY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               chickenX_change = 0



    chickenX += chickenX_change
    if chickenX <= 0:
        chickenX = 0
    elif chickenX >= 736:
        chickenX = 736
    #fox movement
    for i in range(num_of_foxes):
         #Game Over
        if foxY[i] > 440:
            for j in range(num_of_foxes):
                foxY[j] = 2000
            game_over_text()
            break

        foxX[i] += foxX_change[i]
        if foxX[i]  <= 0:
            foxX_change[i]  = 4
            foxY[i]  += foxY_change[i]
        elif foxX[i]  >= 736:
            foxX_change[i]  = -4
            foxY[i]  += foxY_change[i]

         # collision
        collision = iscollision(foxX[i], foxY[i], balloonX, balloonY)
        if collision:
            explosionSound = mixer.Sound("balloonblast.mp3")
            explosionSound.play()

            balloonY = 480
            balloon_state = "ready"
            score_value += 1
            foxX[i] = random.randint(0, 736)
            foxY[i] = random.randint(50, 150)
        fox(foxX[i], foxY[i], i)








    #balloon Movement
    if balloonY <= 0:
        balloonY = 480
        balloon_state = "ready"




    if balloon_state == "thrown":
        balloon(balloonX, balloonY)
        balloonY -= balloonY_change








    chicken(chickenX, chickenY)

    show_score(textX, textY)
    pygame.display.update()




