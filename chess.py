#!/usr/bin/python3
'''
A basic chess game.

Russell Jeffery
7 July 2018
'''

from copy import deepcopy
import pygame
pygame.init()

# Display settings.
black = 0, 0, 0
grey = 200, 200, 200
white = 255, 255, 255

screen_size = 640, 640
screen = pygame.display.set_mode(screen_size)


# The checkerboard.
odd_col = tuple([1, 0] * 4)
evn_col = tuple([0, 1] * 4)
grid = tuple([odd_col, evn_col] * 4)


class Board():
    '''
    This keeps track of the locations of the pieces.
    '''
    def __init__(self, screen_size):
        # Generate an 8x8 array.
        col = [0] * 8
        self.grid = []
        for i in range(8):
            # There is no list method that actually makes deep copies, so I had to import one.
            self.grid.append(deepcopy(col))

        # Define the size of one board square.
        self.square_size = screen_size[1] // 8, screen_size[1] // 8 # width, height

    
    def set_board(self):
        '''
        Set the board in the initial state.
        '''
        # Load all the images.
        b_bishop = pygame.image.load("b_bishop.png").convert_alpha()
        b_bishop = pygame.transform.scale(b_bishop, self.square_size)

        b_king = pygame.image.load("b_king.png").convert_alpha()
        b_king = pygame.transform.scale(b_king, self.square_size)

        b_knight = pygame.image.load("b_knight.png").convert_alpha()
        b_knight = pygame.transform.scale(b_knight, self.square_size)

        b_pawn = pygame.image.load("b_pawn.png").convert_alpha()
        b_pawn = pygame.transform.scale(b_pawn, self.square_size)

        b_queen = pygame.image.load("b_queen.png").convert_alpha()
        b_queen = pygame.transform.scale(b_queen, self.square_size)

        b_rook = pygame.image.load("b_rook.png").convert_alpha()
        b_rook = pygame.transform.scale(b_rook, self.square_size)

        w_bishop = pygame.image.load("w_bishop.png").convert_alpha()
        w_bishop = pygame.transform.scale(w_bishop, self.square_size)

        w_king = pygame.image.load("w_king.png").convert_alpha()
        w_king = pygame.transform.scale(w_king, self.square_size)

        w_knight = pygame.image.load("w_knight.png").convert_alpha()
        w_knight = pygame.transform.scale(w_knight, self.square_size)

        w_pawn = pygame.image.load("w_pawn.png").convert_alpha()
        w_pawn = pygame.transform.scale(w_pawn, self.square_size)

        w_queen = pygame.image.load("w_queen.png").convert_alpha()
        w_queen = pygame.transform.scale(w_queen, self.square_size)

        w_rook = pygame.image.load("w_rook.png").convert_alpha()
        w_rook = pygame.transform.scale(w_rook, self.square_size)


        # Load the pieces into the array.
        # First the black pieces.
        self.grid[0][0] = b_rook
        self.grid[1][0] = b_knight
        self.grid[2][0] = b_bishop
        self.grid[3][0] = b_queen
        self.grid[4][0] = b_king
        self.grid[5][0] = b_bishop
        self.grid[6][0] = b_knight
        self.grid[7][0] = b_rook
        for i in range(8):
            self.grid[i][1] = b_pawn
        # Then the white pieces.
        self.grid[0][7] = w_rook
        self.grid[1][7] = w_knight
        self.grid[2][7] = w_bishop
        self.grid[3][7] = w_queen
        self.grid[4][7] = w_king
        self.grid[5][7] = w_bishop
        self.grid[6][7] = w_knight
        self.grid[7][7] = w_rook
        for i in range(8):
            self.grid[i][6] = w_pawn


    def draw_pieces(self, screen):
        '''
        Draws each piece on the board.
        '''
        # Draw the pieces.
        x_position = 0
        y_position = 0
        for column in self.grid:
            for piece in column:
                # Translate grid coordinates to pixel coordinates.
                position = x_position * self.square_size[0], y_position * self.square_size[1]

                if piece != 0:
                    rect = piece.get_rect()
                    rect = rect.move(position[0], position[1])
                    screen.blit(piece, rect)
                else:
                    pass
                y_position += 1
            y_position = 0
            x_position += 1


def draw_grid(screen, grid, colors=((255, 255, 255), (0, 0, 0))):
    '''
    Draws the checkerboard background pattern.
    '''
    square_size = screen_size[1] // 8, screen_size[1] // 8 # width, height

    # For every element in "grid", draw either a white or black square.
    x_position = 0
    y_position = 0
    for column in grid:
        for place in column:
            # Translate grid coordinates to pixel coordinates.
            position = x_position * square_size[0], y_position * square_size[1]

            # If there is a "1" at this position, make a white square.
            if place == True:
                square = pygame.Rect(position, square_size)
                pygame.draw.rect(screen, (255, 255, 255), square)
            # Otherwise, make a black one.
            elif place == False:
                square = pygame.Rect(position, square_size)
                pygame.draw.rect(screen, (20, 20, 20), square)
            else:
                pass

            # Go to the next square.
            y_position += 1
        # Go to the beginning of the next column.
        y_position = 0
        x_position += 1




###########################################################

board = Board(screen_size)
board.set_board()

draw_grid(screen, grid)
board.draw_pieces(screen)
pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

