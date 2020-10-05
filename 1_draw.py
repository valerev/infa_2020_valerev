import pygame
from pygame.draw import *
import numpy as np

pygame.init()

xsize=400
ysize=400

FPS = 30
screen = pygame.display.set_mode((xsize, ysize))


screen.fill((225, 225, 225))

circle(screen, (225, 225, 0), (200, 200), 150, 0) # face


circle(screen, (225, 0, 0), (150, 160), 30, 0) # left eye (red)
circle(screen, (0, 0, 0), (150, 160), 30, 1) # border
circle(screen, (0, 0, 0), (150, 160), 10, 0)

circle(screen, (225, 0, 0), (250, 160), 20, 0) # right eye (red)
circle(screen, (0, 0, 0), (250, 160), 20, 1) # border
circle(screen, (0, 0, 0), (250, 160), 8, 0)

a=13.5
b=5
polygon(screen, (0, 0, 0), [(250-a-20, 160-a+20), (250-a+35, 160-a-35),
                               (250-a+35-b, 160-a-35-b), (250-a-20-b, 160-a+20-b),
                                (250-a-20, 160-a+20)], 0) # mouth


polygon(screen, (0, 0, 0), [(110, 290), (290,290),
                               (290,300), (110,300), (110, 290)], 0) # eyebrovright

l=30
h=10

polygon(screen, (0, 0, 0), [(165 + l*np.sqrt(3)/2, 134 + l/2),
                            (165 + l*np.sqrt(3)/2 + h/2, 134 + l/2 - h*np.sqrt(3)/2),
                            (165 - 2*l*np.sqrt(3)/2 + h/2, 134 - l - h*np.sqrt(3)/2),
                            (165 - 2*l*np.sqrt(3)/2, 134 - l),
                            (165 + l*np.sqrt(3)/2, 134 + l/2)],
                            0) # eyebrovleft

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()

##
##rect(screen, (255, 0, 255), (100, 100, 200, 200))
##rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
##
##polygon(screen, (255, 255, 0), [(100,100), (200,50),
##                               (300,100), (100,100)])
##polygon(screen, (0, 0, 255), [(100,100), (200,50),
##                               (300,100), (100,100)], 5)
##circle(screen, (0, 255, 0), (200, 175), 50)
##circle(screen, (255, 255, 255), (200, 175), 50, 5)
