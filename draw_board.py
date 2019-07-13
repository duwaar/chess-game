#!/usr/bin/python3
'''
Draws a chess board.

Russell Jeffery
7 July 2018
'''

from time import sleep
import pygame
pygame.init()

# Display.
black = 0, 0, 0
white = 255, 255, 255

screen_size = 640, 640
screen = pygame.display.set_mode(screen_size)

# Board.
odd_col = [1, 0] * 4
evn_col = [0, 1] * 4
grid = [odd_col, evn_col] * 4
square_size = screen_size[1] // 8, screen_size[1] // 8 # width, height


screen.fill(black)
x_pstn = 0
y_pstn = 0
for column in grid:
    for place in column:
        if place == True:
            position = x_pstn * square_size[0], y_pstn * square_size[1]
            square = pygame.Rect(position, square_size)
            pygame.draw.rect(screen, white, square)
        y_pstn += 1
    y_pstn = 0
    x_pstn += 1

pygame.display.flip()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
