#!/usr/bin/python3

import pygame
pygame.init()

white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

screen_size = 600, 600
screen = pygame.display.set_mode(screen_size)

button = (100, 100, screen_size[0] // 4, screen_size[1] // 4)


clicked = False
while True:
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    screen.fill(black)

    # Close game if user clicks exit.
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            exit()

    mouseover = button[0] < mouse[0] < button[0] + button[2]\
            and button[1] < mouse[1] < button[1] + button[3]
    # Highlight button when mouse is over it.
    if mouseover:
        pygame.draw.rect(screen, white, button)
        pygame.draw.rect(screen, green, button, 4)
    else:
        pygame.draw.rect(screen, white, button)

    # If button is clicked, toggle permanent highlight.
    if click[0] and mouseover:
        clicked = True
    else:
        pass

    # Draw the permanent highlight when the mouse is NOT over the button.
    if clicked and not mouseover:
        pygame.draw.rect(screen, red, button, 4)
    else:
        pass


    pygame.display.update()
