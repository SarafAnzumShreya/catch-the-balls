import pygame
import pygame.camera
import keyboard
import cv2
import time
import sys
import numpy as np
from random import randint

pygame.init()
game_active = True


detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
webcam = cv2.VideoCapture(0)
webcam.set(3, 1280)
webcam.set(4, 720)

screen = pygame.display.set_mode((1280, 720))
start_page = pygame.image.load('startpage.PNG')
pygame.display.set_caption("Catch the ball")
basket = pygame.image.load('basket_front.PNG')
basket = pygame.transform.scale(basket, (200, 100))
basket_back = pygame.image.load('basket_back.PNG')
basket_back = pygame.transform.scale(basket_back, (200, 100))
ball1 = pygame.image.load('ball.png')
ball1 = pygame.transform.scale(ball1, (50, 50))
ball2 = pygame.image.load('ball.png')
ball2 = pygame.transform.scale(ball2, (50, 50))

ball_sound = pygame.mixer.Sound("ball_sound.wav")
game_sound = pygame.mixer.Sound("game.wav")

score = 0
clock = pygame.time.Clock()
counter, timeboard = 31, '31'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
game_font = pygame.font.Font("freesansbold.ttf", 50)
end_font = pygame.font.Font("freesansbold.ttf", 100)
m1 = randint(10, 120)
n1 = -10
m2 = randint(10, 720)
n2 = -10
z = 0

running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                running = False
                pygame.display.quit()
    # opencv code
    ready, frame = webcam.read()
    gray_scaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_coordinates = detector.detectMultiScale(gray_scaled, scaleFactor=1.05,
	minNeighbors=7, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    # for (x, y, w, h) in face_coordinates:
    #     box = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # opencv code
    window = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    window = np.rot90(window)
    window = pygame.surfarray.make_surface(window).convert()
    if game_active:

        """basket back"""
        max_area = 0
        area = 0
        for (a, b, c, d) in face_coordinates:
            area = c * d
            if area>max_area:
                x = a
                y = b
                w = c
                h = d
                # max_area = area
                # frame = frame[y:y+h, x:x+w]
        window.blit(basket_back, (1280-x-w, y+h), )
        """basket back"""

        """ball"""
        val1 = randint(6, 10)
        n1 += val1
        window.blit(ball1, (m1, n1), )
        if n1 >= 700:
            n1 = -10
            m1 = randint(10, 1200)
            window.blit(ball1, (m1, n1), )
        """ball 2"""
        val2 = randint(10, 20)
        n2 += val2
        window.blit(ball2, (m2, n2), )
        if n2 >= 700:
            n2 = -10
            m2 = randint(10, 1200)
            window.blit(ball2, (m2, n2), )
        """ball"""

        """collision"""

        """collision"""

        """basket"""
        
        window.blit(basket, (1280-x-w, y+h+15), )
        if (m1 >= 1280-x-w-50) and (m1 <= 1280-x-w+200):
            if (n1 >= y+h+20) and (n1 <= y+h+60):
                m1 = 1200
                n1 = 1200
                window.blit(ball1, (m1, n1), )
                ball_sound.play()
                score += 1
        if (m2 >= 1280-x-w-50) and (m2 <= 1280-x-w+200):
            if (n2 >= y+h+20) and (n2 <= y+h+60):
                m2 = 1200
                n2 = 1200
                window.blit(ball2, (m2, n2), )
                ball_sound.play()
                score += 1
        """basket"""
        """scoreboard"""
        text = game_font.render('Score:', True, (255, 255, 255))
        window.blit(text, (50, 50))
        scoreboard = game_font.render(f"{score}", True, (255, 255, 255))
        window.blit(scoreboard, (250, 50))
        """scoreboard"""
        """Timer"""
        time = game_font.render('Timer:', True, (255, 255, 255))
        window.blit(time, (950, 50))
        window.blit(game_font.render(timeboard, True, (255, 255, 255)), (1100, 50))
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1
                timeboard = str(counter).rjust(3)
                if counter < 0:
                    counter = 0
                    timeboard = str(counter).rjust(3)
                    z = 1
                    break
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    running = False
                    pygame.display.quit()
        if z == 1:
            game_active = False
            # webcam.release()
            window.blit(start_page, (0, 0))
            endscreen = game_font.render('Score: ', True, (255, 255, 255))
            window.blit(endscreen, (350, 250))
            score_board = game_font.render(f"{score}", True, (255, 255, 255))
            window.blit(score_board, (550, 250))
            game_sound.play()
        """Timer"""
        screen.blit(window, (0, 0))
        pygame.display.update()
        clock.tick(60)


    else:
        if keyboard.is_pressed(' '):
            game_active = True
            z = 0
            counter, timeboard = 31, '31'.rjust(3)
            score = 0
            screen.blit(window, (0, 0))
            window.blit(start_page, (1300, 1300))
    key = cv2.waitKey(1)
    cv2.destroyAllWindows()
