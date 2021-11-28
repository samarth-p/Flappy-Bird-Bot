import random

import numpy as np
import pygame

from Genetic_Algo import initialize, flappy_boi, fitness, selection

# color definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 215, 0)

# global game variables
winW = 800
winH = 600

num_bird = 50
dist = np.array([0] * num_bird)
pipeInit = winW + 150
gen = 1

pygame.init()
gameDisplay = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("Flappy Birds")
clock = pygame.time.Clock()
FPS = 30
smallfont = pygame.font.SysFont(None, 30)
mediumfont = pygame.font.SysFont(None, 50)
largefont = pygame.font.SysFont(None, 80)

# image loading
bg = pygame.image.load("images/bg.jpeg")
bg = pygame.transform.scale(bg, (800, 600))

birdy1 = pygame.image.load("images/redbird.png")
birdy1 = pygame.transform.scale(birdy1, (50, 50))
birdy2 = pygame.image.load("images/yellowbird.png")
birdy2 = pygame.transform.scale(birdy2, (50, 50))
birdy3 = pygame.image.load("images/bluebird.png")
birdy3 = pygame.transform.scale(birdy3, (50, 50))

gameover = pygame.image.load('images/gameOver.jpg')
gameover = pygame.transform.scale(gameover, (600, 300))

pipeDown = pygame.image.load("images/pipeDown.jpeg")
pipeUp = pygame.image.load("images/pipeUp.jpeg")

# audio files
hit = pygame.mixer.Sound('sound/hit.wav')
point = pygame.mixer.Sound('sound/point.wav')
flap = pygame.mixer.Sound('sound/flap.wav')
die = pygame.mixer.Sound('sound/die.wav')


def calc_dist(birdX, birdW, pipeX, pipeW, score):
    if score == 0:
        dist = pipeInit - pipeX
    elif birdX + birdW <= pipeX + pipeW:
        dist = score * winW + winW - ((pipeX + pipeW) - (birdX + birdW))
    else:
        dist = score * winW + (birdX + birdW) - (pipeX + pipeW)
    return dist


def gameQuit():
    pygame.quit()
    quit()


def printMessage(msg, color, font, yLoc=0):
    textSurface = font.render(msg, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (winW / 2), (winH / 2) + yLoc
    gameDisplay.blit(textSurface, textRect)


def dispScore(score, gen):
    spaces = str(10 * " ")
    pygame.draw.rect(gameDisplay, yellow, [0, 0, 500, 50])
    text = smallfont.render("Generation -  " + str(gen), True, blue)
    gameDisplay.blit(text, [10, 5])
    text = smallfont.render("Score -  " + str(score), True, blue)
    gameDisplay.blit(text, [200, 5])
    # text = smallfont.render("Prev HighScore -  " , True, blue)
    # gameDisplay.blit(text, [10, 30])
    pygame.display.update()


def instructions():
    instructionPage = True
    gameDisplay.fill(yellow)
    gameDisplay.blit(birdy1, (winW / 8, winH / 5))
    gameDisplay.blit(birdy3, (winW / 4, winH / 5))
    gameDisplay.blit(birdy2, (winW / 2, winH / 5))
    gameDisplay.blit(birdy3, (winW - winW / 4, winH / 5))
    gameDisplay.blit(birdy1, (winW - winW / 8, winH / 5))
    while instructionPage == True:
        msg = "Flap your way through the pipes"
        msg1 = "Controls are as follows"
        msg2 = "UP ARROW to flap"
        msg4 = "Press P to play and q to Quit"
        msg5 = "While playing, press P to pause"
        printMessage(msg, blue, mediumfont, -50)
        printMessage(msg1, black, smallfont)
        printMessage(msg2, black, smallfont, 30)
        printMessage(msg4, red, smallfont, 150)
        printMessage(msg5, red, smallfont, 180)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    instructionPage = False
                elif event.key == pygame.K_q:
                    gameQuit()

        clock.tick(10)
        pygame.display.update()


def gameIntro():
    intro = True
    introScreen = pygame.image.load('images/Flappy_Logo.png')
    introScreen = pygame.transform.scale(introScreen, (int(winW / 2), int(winH / 4)))
    while intro:
        gameDisplay.fill(yellow)
        gameDisplay.blit(introScreen, (winW / 4, winH / 3))

        msg1 = "Press I to view the instructions to play and q to Quit"
        printMessage(msg1, red, smallfont, +100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    instructions()
                    intro = False
                elif event.key == pygame.K_q:
                    gameQuit()

        clock.tick(10)
        pygame.display.update()


def gamePaused():
    # pygame.mixer.music.pause()
    gameDisplay.fill(yellow)
    printMessage("Game Paused", red, largefont, -20)
    printMessage("Press P to continue playing and Q to quit", black, smallfont, 70)
    pygame.display.update()

    paused = True

    while paused == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # pygame.mixer.music.unpause()
                    paused = False
                if event.key == pygame.K_q:
                    gameQuit()

    clock.tick(10)


def genetic_algo():
    fitness(dist)
    selection()
    global gen
    gen += 1


def gameLoop():
    # variable declarations
    x1 = np.array([0.] * num_bird)       # distance to closest pipe
    x2 = np.array([0.] * num_bird)       # distance to gap of pipe
    x3 = np.array([0.] * num_bird)       # height of bird

    gameExit = False
    gameOver = [False] * num_bird
    birdW = 50
    birdH = 50
    birdX = winW / 4
    birdY = np.array([winH / 2] * num_bird)
    y_change = np.array([0] * num_bird)
    y_disp = 20
    score = np.array([0] * num_bird)
    level = 1
    speed = 0
    i = j = 1

    global pipeUp
    global pipeDown

    pipeGap = 150
    pipeWidth = 100
    pipeX = pipeInit

    pipeDownHeight = random.randrange(100, 400)
    pipeUpHeight = winH - pipeGap - pipeDownHeight

    pipeDownY = 0
    pipeUpY = pipeDownHeight + pipeGap

    bgX = 0
    bgY = 0
    bgX1 = winW
    bgY1 = 0
    bgX_change = 10

    pipeDown = pygame.transform.scale(pipeDown, (pipeWidth, pipeDownHeight))
    pipeUp = pygame.transform.scale(pipeUp, (pipeWidth, pipeUpHeight))

    f = open("highScore.txt")
    prevHigh = int(f.read())
    f.close()

    randBird = random.randrange(1, 4)
    counter = 0

    initialize(num_bird)

    while not gameExit:
        # game over event handling

        if all(gameOver):
            genetic_algo()

        while all(gameOver):

            gameDisplay.fill(yellow)
            gameDisplay.blit(gameover, (winW / 8, winH / 4))
            # printMessage("Flappy's dead", red, largefont)
            printMessage("Distance: " + str(dist), black, smallfont, 200)
            # printMessage("Press P to play and q to Quit", black, smallfont, 200)

            with open("highScore.txt") as f:
                highScore = int(f.read())
                if any(score) > highScore:
                    highScore = max(score)
            with open("highScore.txt", "w") as f:
                f.write(str(highScore))

            printMessage("High Score: " + str(highScore), black, smallfont, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        f = open("highScore.txt")
                        prevHigh = int(f.read())
                        f.close()
                        gameOver = [False] * num_bird
                    elif event.key == pygame.K_q:
                        gameQuit()

            pipeDownHeight = random.randrange(100, 400)
            pipeUpHeight = winH - pipeGap - pipeDownHeight

            pipeDownY = 0
            pipeUpY = pipeDownHeight + pipeGap

            bgX = 0
            bgY = 0
            bgX1 = winW
            bgY1 = 0
            bgX_change = 10

            pipeDown = pygame.transform.scale(pipeDown, (pipeWidth, pipeDownHeight))
            pipeUp = pygame.transform.scale(pipeUp, (pipeWidth, pipeUpHeight))

            birdY = np.array([winH / 4] * num_bird)
            y_change = np.array([0] * num_bird)
            pipeX = pipeInit
            score = np.array([0] * num_bird)
            level = 1
            counter = 0
            randBird = random.randrange(1, 4)
            clock.tick(10)
            pygame.display.update()

        y_change += 1

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(flap)
                    y_change -= y_disp
                    # y_change[1] -= y_disp
                elif event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(flap)
                    y_change[1] -= y_disp
                elif event.key == pygame.K_p:
                    gamePaused()

        # -----------------------------------------------------------------------------------------
        # Neural network

        # if counter == 2:
        for i in range(num_bird):
            if gameOver[i]:
                continue
            elif pipeX + pipeWidth >= birdX + birdW:
                x1[i] = ((pipeWidth + pipeX) - (birdW + birdX)) / 700.
            else:
                x1[i] = (winW - (birdW + birdX) + (pipeWidth + pipeX)) / 700.
            x2[i] = ((pipeDownHeight + pipeGap/2) - (birdY[i] + birdH)) / 425.
            # x3[i] = (winH - birdY[i]) / 800.

            y = flappy_boi(x1[i], x2[i], i)
            print("gen%d - y%d: %f %f %f" % (gen, i, y, x1[i], x2[i]))
            if y >= 0.5:
                pygame.mixer.Sound.play(flap)
                y_change[i] -= y_disp
        # ------------------------------------------------------------------------------------------

        birdY += y_change
        bgX1 -= bgX_change
        bgX -= bgX_change
        pipeX -= 10 + speed

        # game rendering
        gameDisplay.fill(white)
        gameDisplay.blit(bg, (bgX, bgY))
        gameDisplay.blit(bg, (bgX1, bgY1))

        for i in range(num_bird):
            if not gameOver[i]:
                gameDisplay.blit(birdy1, (birdX, birdY[i]))

        pipeDown = pygame.transform.scale(pipeDown, (pipeWidth, pipeDownHeight))
        pipeUp = pygame.transform.scale(pipeUp, (pipeWidth, pipeUpHeight))
        gameDisplay.blit(pipeUp, (pipeX, pipeUpY))
        gameDisplay.blit(pipeDown, (pipeX, pipeDownY))

        dispScore(score, gen)
        pygame.display.update()
        clock.tick(FPS)

        # gameLogic

        for i in range(num_bird):

            if gameOver[i]:
                continue

            # bird hits floor
            if birdY[i] + birdH >= winH:
                pygame.mixer.Sound.play(hit)
                gameOver[i] = True

            # bird hits ceiling
            if birdY[i] <= 0:
                pygame.mixer.Sound.play(hit)
                gameOver[i] = True

            # change pipe location to back of the screen
            if pipeX < 0:
                pipeDownHeight = random.randrange(100, 400)
                pipeUpHeight = winH - pipeGap - pipeDownHeight
                pipeDownY = 0
                pipeUpY = pipeDownHeight + pipeGap
                pipeX = winW

            # bird hits pipe
            if birdX + birdW >= pipeX and birdX <= pipeX + pipeWidth:
                if birdY[i] < pipeDownHeight or birdY[i] + birdH > pipeUpY:
                    pygame.mixer.Sound.play(hit)
                    gameOver[i] = True

            if birdX == pipeX + pipeWidth and not gameOver[i]:
                score[i] += 1

            if gameOver[i]:
                dist[i] = calc_dist(birdX, birdW, pipeX, pipeWidth, score[i])
            # dist[i] += 1

        if bgX + winW <= 0:
            bgX = winW
        if bgX1 + winW <= 0:
            bgX1 = winW

        if any(score >= 1 * j):
            pygame.mixer.Sound.play(point)
            j += 1

        # if score >= 100 * i:
        #     i += 1
        #     level += 1
        #     speed += 2

        # counter = (counter + 1) % 3


# function calls
gameIntro()
gameLoop()
gameQuit()
