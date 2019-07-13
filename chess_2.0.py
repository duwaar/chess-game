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
grey = 128, 128, 128
white = 255, 255, 255
red = 225, 0, 0
green = 0, 255, 0
yellow = 255, 255, 0

screen_size = 640, 640
screen = pygame.display.set_mode(screen_size)


class Board():
    '''
    This keeps track of the locations of the pieces.
    '''
    def __init__(self, screen):
        # Display and board things.
        self.screen_size = screen.get_size()
        self.square_size = screen_size[0] // 8, screen_size[0] // 8 # width, height

        # Each grid square has three values: [b/w, piece, sel]
        self.grid = []
        self.sel = ["n", "n"]
        b_sqr = [0, 0]
        w_sqr = [1, 0]

        # Build the columns...
        odd_col = []
        evn_col = []
        for i in range(4):
            odd_col.append(deepcopy(w_sqr))
            odd_col.append(deepcopy(b_sqr))
        for i in range(4):
            evn_col.append(deepcopy(b_sqr))
            evn_col.append(deepcopy(w_sqr))
        # Then build the whole grid.
        for i in range(4):
            self.grid.append(deepcopy(odd_col))
            self.grid.append(deepcopy(evn_col))

        # Load all the images.
        self.b_bishop = pygame.image.load("b_bishop.png").convert_alpha()
        self.b_bishop = pygame.transform.scale(self.b_bishop, self.square_size)

        self.b_king = pygame.image.load("b_king.png").convert_alpha()
        self.b_king = pygame.transform.scale(self.b_king, self.square_size)

        self.b_knight = pygame.image.load("b_knight.png").convert_alpha()
        self.b_knight = pygame.transform.scale(self.b_knight, self.square_size)

        self.b_pawn = pygame.image.load("b_pawn.png").convert_alpha()
        self.b_pawn = pygame.transform.scale(self.b_pawn, self.square_size)

        self.b_queen = pygame.image.load("b_queen.png").convert_alpha()
        self.b_queen = pygame.transform.scale(self.b_queen, self.square_size)

        self.b_rook = pygame.image.load("b_rook.png").convert_alpha()
        self.b_rook = pygame.transform.scale(self.b_rook, self.square_size)

        self.w_bishop = pygame.image.load("w_bishop.png").convert_alpha()
        self.w_bishop = pygame.transform.scale(self.w_bishop, self.square_size)

        self.w_king = pygame.image.load("w_king.png").convert_alpha()
        self.w_king = pygame.transform.scale(self.w_king, self.square_size)

        self.w_knight = pygame.image.load("w_knight.png").convert_alpha()
        self.w_knight = pygame.transform.scale(self.w_knight, self.square_size)

        self.w_pawn = pygame.image.load("w_pawn.png").convert_alpha()
        self.w_pawn = pygame.transform.scale(self.w_pawn, self.square_size)

        self.w_queen = pygame.image.load("w_queen.png").convert_alpha()
        self.w_queen = pygame.transform.scale(self.w_queen, self.square_size)

        self.w_rook = pygame.image.load("w_rook.png").convert_alpha()
        self.w_rook = pygame.transform.scale(self.w_rook, self.square_size)

    
    def set_board(self):
        '''
        Set the board in the initial state.
        '''
        # First the black pieces.
        self.grid[0][0][1] = "b_rook"
        self.grid[1][0][1] = "b_knight"
        self.grid[2][0][1] = "b_bishop"
        self.grid[3][0][1] = "b_queen"
        self.grid[4][0][1] = "b_king"
        self.grid[5][0][1] = "b_bishop"
        self.grid[6][0][1] = "b_knight"
        self.grid[7][0][1] = "b_rook"
        for i in range(8):
            self.grid[i][1][1] = "b_pawn"
        # Then the white pieces.
        self.grid[0][7][1] = "w_rook"
        self.grid[1][7][1] = "w_knight"
        self.grid[2][7][1] = "w_bishop"
        self.grid[3][7][1] = "w_queen"
        self.grid[4][7][1] = "w_king"
        self.grid[5][7][1] = "w_bishop"
        self.grid[6][7][1] = "w_knight"
        self.grid[7][7][1] = "w_rook"
        for i in range(8):
            self.grid[i][6][1] = "w_pawn"


    def draw_color(self, position, square):
        '''
        Draw either a white or black square.
        '''
        tile = pygame.Rect(position[0:2], self.square_size)
        # If the tile is a "1", draw white.
        if square[0] == 1:
            pygame.draw.rect(screen, white, tile)
        # Otherwise, draw a black one.
        elif square[0] == 0:
            pygame.draw.rect(screen, black, tile)
        else:
            print("color error:", square[0])


    def draw_piece(self, position, square):
        '''
        Draw the piece in grid[x][y][1] at the specified position.
        '''
        # If there is anything there, draw it.
        piece = 0
        if square[1] != 0:
            # Identify the piece...
            if False: # It bothered me that b_bishop was being treated differently than w_bishop.
                pass

            elif square[1] == "b_bishop":
                piece = self.b_bishop
            elif square[1] == "b_king":
                piece = self.b_king
            elif square[1] == "b_knight":
                piece = self.b_knight
            elif square[1] == "b_pawn":
                piece = self.b_pawn
            elif square[1] == "b_queen":
                piece = self.b_queen
            elif square[1] == "b_rook":
                piece = self.b_rook

            elif square[1] == "w_bishop":
                piece = self.w_bishop
            elif square[1] == "w_king":
                piece = self.w_king
            elif square[1] == "w_knight":
                piece = self.w_knight
            elif square[1] == "w_pawn":
                piece = self.w_pawn
            elif square[1] == "w_queen":
                piece = self.w_queen
            elif square[1] == "w_rook":
                piece = self.w_rook

            # ...then draw it.
            rect = piece.get_rect()
            rect = rect.move(position[0], position[1])
            screen.blit(piece, rect)
        else:
            pass


    def draw_selection(self, position, square, mouseover, click):
        '''
        Draw a highlight around the selected square.
        '''
        # Update the selection if a click occurs.
        if mouseover and click[0]:
            self.sel = [position[2], position[3]]
        else:
            pass

        # Draw the highlight if the mouse is somewhere else.
        highlight = position[0], position[1], self.square_size[0], self.square_size[1]
        if self.sel == position[2:4] and not mouseover:
            pygame.draw.rect(screen, yellow, highlight, 4)


    def draw_mouseover(self, position, mouseover):
        '''
        Draw a highlight around the square under the mouse.
        '''
        # Draw a greeen highlight around the square under the mouse.
        if mouseover:
            highlight = position[0], position[1], self.square_size[0], self.square_size[1]
            pygame.draw.rect(screen, green, highlight, 4)
        else:
            pass


    def draw(self, screen, mouse, click):
        '''
        Draws everything on the board.
        '''
        x_index = 0
        y_index = 0
        for column in self.grid:
            for square in column:
                # Translate grid coordinates to pixel coordinates.
                position = x_index * self.square_size[0], y_index * self.square_size[1], x_index, y_index
                # Check if the mouse is over this square.
                mouseover = position[0] < mouse[0] < position[0] + self.square_size[0]\
                        and position[1] < mouse[1] < position[1] + self.square_size[1]

                # First draw the colored square...
                self.draw_color(position, square)
                # ...then draw the chess piece...
                self.draw_piece(position, square)
                # ...then draw the selection highlight...
                self.draw_selection(position, square, mouseover, click)
                # ...then draw the mouseover highlight.
                self.draw_mouseover(position, mouseover)

                y_index += 1
            y_index = 0
            x_index += 1


    def move(self, turn, screen, mouse, click):
        '''
        Moves the selected piece to the selected square.
        '''
        x_index = 0
        y_index = 0
        for column in self.grid:
            for square in column:
                # Translate grid coordinates to pixel coordinates.
                position = x_index * self.square_size[0], y_index * self.square_size[1], x_index, y_index
                # Check if the mouse is over this square.
                mouseover = position[0] < mouse[0] < position[0] + self.square_size[0]\
                        and position[1] < mouse[1] < position[1] + self.square_size[1]

                # if a click occurs on a piece and there is nothing selected, select the clicked square.
                if mouseover and click[0] and (self.sel == ["n", "n"]) and (self.grid[x_index][y_index][1] != 0):
                    self.sel = [x_index, y_index]
                # if something is selected and a right click occurs, reset selection.
                elif click[2] and (self.sel != ["n", "n"]):
                    self.sel = ["n", "n"]
                # if a square is selected... 
                elif mouseover and click[0] and (self.sel != ["n", "n"]):
                    # ...and previously a piece was selected, and it is the correct turn, move the piece.
                    if self.sel != [x_index, y_index] and str(self.grid[self.sel[0]][self.sel[1]][1])[0] == turn:
                        self.grid[x_index][y_index][1] = deepcopy(self.grid[self.sel[0]][self.sel[1]][1])
                        self.grid[self.sel[0]][self.sel[1]][1] = 0
                        # Reset the selection and change turns.
                        self.sel = ["n", "n"]
                        if turn == "w":
                            turn = "b"
                        elif turn == "b":
                            turn = "w"
                else:
                    pass

                y_index += 1
            y_index = 0
            x_index += 1

            if (self.sel != ["n", "n"]):
                print(self.sel, turn, str(self.grid[self.sel[0]][self.sel[1]][1])[0])

            return turn


###########################################################

# Initialize the board object.
board = Board(screen)
# Set up the pieces in a matrix.
board.set_board()

# Main game loop
turn = "w"
while True:
    # Check the mouse.
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Move pieces.
    turn = board.move(turn, screen, mouse, click)

    # Draw the squares, pieces, and highlights.
    board.draw(screen, mouse, click)

    # Check to see if the user is trying to exit.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Finally, update the display.
    pygame.display.update()

