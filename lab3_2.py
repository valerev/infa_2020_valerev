import pygame
from pygame.draw import *
import numpy as np
import random

pygame.init()

# Colors:
Blue = (100, 100, 220)
Gray = (100, 100, 100)
White = (225, 225, 225)
L_green = (100, 200, 100)
Green = (0, 210, 0)
Black = (0, 0, 0)
Yellow = (225, 225, 0)
Purple = (225, 0, 225)

def draw_bush(x, y, R):
    circle(screen, Green, (x,y), R)
    #circle(screen, Black, (x,y), R, 1)
    n = random.randint(4, 6)
    s = R * 7 / 11
    draw_flower(x, y, R/5)
    for i in range(n):
        phi = i * 2 * np.pi / n
        draw_flower(x + s*np.cos(phi),
                    y + s*np.sin(phi),
                    R/4)


def draw_flower(x, y, R):
    ellipse(screen, Yellow, pygame.Rect(x-R, y-R/2, 2*R, R))
    ellipse(screen, Black, pygame.Rect(x-R, y-R/2, 2*R, R), 1)
    n=4
    for j in (-1,1):
        for k in (-1, 1):
            for i in range(1, n):
                phi = i*i*np.pi/(n*n)
                ellipse(screen, White, pygame.Rect(x + j*R/np.sqrt(1 + 4*(np.tan(phi)**2)) - R/2 ,
                                                   y + k*R/np.sqrt(4 + 1/(np.tan(phi)**2)) - R/4,
                                                   R,
                                                   R/2))
                ellipse(screen, Black, pygame.Rect(x + j*R/np.sqrt(1 + 4*(np.tan(phi)**2)) - R/2 ,
                                                   y + k*R/np.sqrt(4 + 1/(np.tan(phi)**2)) - R/4,
                                                   R,
                                                   R/2),
                                                    1)
                

                
def draw_lama(x, y, size):
    ellipse(screen, White, pygame.Rect(x - size/2,
                                       y - size/4,
                                       size,
                                       3*size/8))  # Draw a lama_body
    draw_lama_leg(x - 3*size/8, y - size/32, size/3)
    draw_lama_leg(x - 3*size/16, y + size/32, size/3)
    draw_lama_leg(x + 3*size/8, y + size/32, size/3)
    draw_lama_leg(x + 2*size/8, y - size/32, size/3)
    ellipse(screen, White, pygame.Rect(x + size/2 - size/5,
                                       y - 5*size/7,
                                       size/6,
                                       5*size/7)) # Draw a lama_neck
    ellipse(screen, White, pygame.Rect(x + size/2 - size/5,
                                       y - 6*size/7,
                                       2*size/7,
                                       3*size/14)) # Draw a lama_head
    ellipse(screen, Purple, (x + size/2 - 5*size/32,
                             y - 5*size/7 - 2*size/16,
                             size/8,
                             size/8)) # Draw a lama_eye
    ellipse(screen, Black, (x + size/2 - 7*size/64,
                             y - 5*size/7 - 3*size/32,
                             size/16,
                             size/16))
    draw_lama_horn(x + size/2 - 9*size/64 + size/100,
                   y - 6*size/7 + size/100,
                   2*size/32)
    draw_lama_horn(x + size/2 - size/5 + size/100,
                   y - 26*size/32,
                   3*size/32)


def draw_lama_leg(x, y, size):
    ellipse(screen, White, pygame.Rect(x - size/6,
                                        y,
                                        size/3,
                                        size))
    ellipse(screen, White, pygame.Rect(x - size/6,
                                        y + 5*size/7,
                                        size/3,
                                        size))
    ellipse(screen, White, pygame.Rect(x - size/6,
                                        y + 2*size - 3*size/7,
                                        5*size/9,
                                        size/4))

def draw_lama_horn(x, y, size):
    points = [(x,y),
              (x - size, y - size),
              (x, y + size/2),
              (x,y)]
    polygon(screen, White, points)

xsize=500
ysize=700

FPS = 30
screen = pygame.display.set_mode((xsize, ysize))


screen.fill(Blue)

# Drawing a landscape

Mountain_heels = []
for i in range(9):
    Mountain_heels.append((i*xsize/8, random.randint(ysize//120, ysize//3)))

polygon(screen, Gray, Mountain_heels + [(xsize, ysize), (0, ysize)])
lines(screen, Black, False, Mountain_heels, 1)

# Drawing a grass

Grass = []
for i in range(100):
    Grass.append((i*xsize/8,
                           random.randint(50 + ysize//3 + ysize//120,
                                          60 + ysize//3 + ysize//120)))

polygon(screen, L_green, Grass + [(xsize, ysize), (0, ysize)])
lines(screen, Black, False, Grass, 1)

# Drawing a bush

for t in range(3):
    draw_bush(random.randint(0, xsize), random.randint(ysize / 2, ysize), random.randint(50, 100))

# Drawing a lama

for t in range(5):
    draw_lama(random.randint(0, xsize), random.randint(ysize / 2, ysize), random.randint(50, 200))

pygame.display.update()
clock = pygame.time.Clock()
finished = False



while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()

