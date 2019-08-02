#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
GUI Chess
A graphical chess game.

R Jeffery
14 July 2019
'''


import os, pyglet, logging


def sign(x):
    '''Return +1 for positive numbers, -1 for negative numbers, and 0 for zero.'''
    assert type(x) == int, "{} is not an int. sign() only takes ints".format(x)

    if x == 0:
        return 0
    else:
        return x // abs(x)


class Movement(object):
    '''Stores movement information for clearer and more convenient movement operations.'''
    def __init__(self, board, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.dx = x2 - x1
        self.dy = y2 - y1
        self.piece = board.get_piece(x1, y1)
        self.piece_color = self.piece[0]
        self.destination = board.get_piece(x2, y2)


class Board(object):
    '''
    Keeps track of the pieces and the dimensions of the squares.
    '''
    def __init__(self):
        '''Set the board.'''
        start_configuration = [["BR","BN","BB","BQ","BK","BB","BN","BR"],\
                               ["BP","BP","BP","BP","BP","BP","BP","BP"],\
                               ["  ","  ","  ","  ","  ","  ","  ","  "],\
                               ["  ","  ","  ","  ","  ","  ","  ","  "],\
                               ["  ","  ","  ","  ","  ","  ","  ","  "],\
                               ["  ","  ","  ","  ","  ","  ","  ","  "],\
                               ["WP","WP","WP","WP","WP","WP","WP","WP"],\
                               ["WR","WN","WB","WQ","WK","WB","WN","WR"]]

        self.array = []
        for j in range(8):
            row = []
            for i in range(8):
                square = {"piece":start_configuration[j][i],\
                          "selection":0,\
                          "left":0, "right":0, "bottom":0, "top":0,\
                          "color":(0, 200, 100)}
                row.append(square)
            self.array.append(row)

    def get_piece(self, i, j):
        '''Return the value of the "piece" field at index i, j.'''
        return self.array[j][i]["piece"]

    def set_piece(self, i, j, piece):
        '''Assign the value of the "piece" field at index i, j.'''
        assert piece.isalpha() and len(piece) == 2,\
                "piece must be a string of two characters. {} is invalid.".format(piece)
        self.array[j][i]["piece"] = piece

    def set_size(self, major_dim, x_offset=0, y_offset=0):
        '''Define the dimensions of the board and all the squares in it.'''
        minor_dim = major_dim // 8
        for j, row in enumerate(self.array):
            for i, square in enumerate(row):
                # Define the dimensions of the square.
                square["left"]   = x_offset + minor_dim * i
                square["right"]  = x_offset + minor_dim * (i + 1)
                square["top"]    = y_offset - minor_dim * j
                square["bottom"] = y_offset - minor_dim * (j + 1)

    def set_colors(self, mouse_position):
        '''Set the color of each square--including mouseover and highlights.'''
        for j, row in enumerate(self.array):
            for i, square in enumerate(row):
                # Define the color of the square.
                if (square["left"] < mouse_position[0] < square["right"])\
                        and (square["bottom"] < mouse_position[1] < square["top"]):
                    square["color"] = (0, 255, 0)
                elif (i + j) % 2 == 0:
                    square["color"] = (255, 255, 255)
                else:
                    square["color"] = (0, 0, 0)

    def draw(self, batch, group=None):
        '''Load primitives into the batch.'''
        for row in self.array:
            for square in row:
                # Add the square to the list of things to draw.
                batch.add(4, pyglet.gl.GL_QUADS, group,\
                          ('v2i', (square["left"],  square["top"],\
                                   square["right"], square["top"],\
                                   square["right"], square["bottom"],\
                                   square["left"],  square["bottom"])),\
                          ('c3B', square["color"] * 4))


class Chess(object):
    '''
    The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces.
    '''
    def __init__(self):
        '''Setup the board and the graphics window, and wait for the start signal.'''
        self.window = pyglet.window.Window(width=600, height=700)
        self.window.set_caption('Python Chess')

        self.message = ""
        self.previous_state = ""
        self.current_state = "SETUP"
        self.board = Board()

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        self.mouse_position = (0, 0)
        self.mouse_click = (0, 0)

        @self.window.event
        def on_draw():
            if self.current_state != self.previous_state:
                self.message += "State changed from \"{}\" to \"{}\".\n".format(self.previous_state, self.current_state)
                self.change_state(self.current_state)

            # Update the output and display.
            self.draw_board()
            self.batch.draw()
            self.batch = pyglet.graphics.Batch() # Is this the right way to clear the batch? Seems clunky and inefficient.
            print(self.message)
            self.message = ""

        @self.window.event
        def on_key_press(key, modifiers):
            pass
            #self.message += "key press: key{}, mods{}\n".format(key, modifiers)

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_position = (x, y)
            self.message += "mouse position: {}\n".format(self.mouse_position)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.message += "mouse press: x{}, y{}, button{}, modifiers{}\n".format(x, y, button, modifiers)

    def change_state(self, new_state):
        '''Update the current and previous states.'''
        self.previous_state = self.current_state
        self.current_state = new_state

    def play(self):
        '''The main game'''
        # Set initial conditions.
        self.message += "Let the game begin!\n"
        self.change_state("WHITE")

        # Start the game loop.
        pyglet.app.run()

        # Print the final message.
        print("{}".format(self.message))

    def take_turn(self):
        '''Execute move, and update display'''
        # Execute the command.
        if command == "quit":
            self.message += "{} gave up and flipped the board.\n".format(self.current_state)
            self.change_state("NONE WINS")
        elif command == "pass":
            self.message += "{} forfeit their turn.\n".format(self.current_state)
            self.current_state = "WHITE" if self.current_state == "BLACK" else "BLACK"
        elif self.is_legal_move(command):
            move = Movement(self.board, command[1], command[0], command[4], command[3])
            captured_piece = move.destination
            self.message += "Move \"{}\" was executed by {}.\n".format(command, self.current_state)
            self.message += "{} captured {}.\n".format(move.piece, captured_piece)
            # Change board.
            self.board.set_piece(move.x2, move.y2, self.board.get_piece(move.y1, move.x1))
            self.board.set_piece(move.x1, move.y1, "")
            # Check for win conditions.
            if captured_piece == "WK":
                self.change_state("BLACK WINS")
            elif captured_piece == "BK":
                self.change_state("WHITE WINS")
            else:
                if self.current_state == "BLACK":
                    self.change_state("WHITE")
                else:
                    self.change_state("BLACK")
        else:
            self.message += "\"{}\" is not a valid command.\n".format(command)
            # Don't change state.

    def set_background(self):
        '''
        Calculate and define the sizes and shapes of the background elements.
        Return the dimensions of the checkerboard.
        '''
        width, height = self.window.get_size()
        margin = 16
        major_dim = height if height < width else width
        major_dim = major_dim - margin
        minor_dim = major_dim // 8

        # The y-index label.
        self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                       ('v2i', (0,      height,\
                                margin, height,\
                                margin, height - major_dim,\
                                0,      height - major_dim)),\
                       ('c3B', (120, 120, 120) * 4))
        # The x-index label.
        self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                       ('v2i', (0,     height - major_dim,\
                                width, height - major_dim,\
                                width, height - (major_dim + margin),\
                                0,     height - (major_dim + margin))),\
                       ('c3B', (120, 120, 120) * 4))
        # The message box.
        self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                       ('v2i', (0,     height - (major_dim + margin),\
                                width, height - (major_dim + margin),\
                                width, 0,\
                                0,     0)),\
                       ('c3B', (220, 220, 220) * 4))
        # The checkerboard.
        self.board.set_size(major_dim, x_offset=margin, y_offset=height)
        self.board.set_colors(self.mouse_position)
        self.board.draw(self.batch, group=self.background)

    def set_foreground(self):
        '''Prepare the foreground items for drawing.'''
        # The message board area
        width, height = self.window.get_size()
        margin = 16
        major_dim = height if height < width else width
        minor_dim = (major_dim - margin) // 8
        # The message
        pyglet.text.Label(text=self.message,\
                          font_name='Courier New',\
                          font_size=12,\
                          color=(0, 0, 0, 255),\
                          x=0, y=0,\
                          width=width,\
                          height=height - minor_dim*8 - margin,\
                          anchor_x='left',\
                          anchor_y='bottom',\
                          multiline=True,\
                          batch=self.batch,\
                          group=self.foreground)

    def draw_board(self):
        '''Display the board.'''
        self.set_background()
        self.set_foreground()

    def is_move_command(self, command):
        '''Checks if command is formatted like a move command.'''
        if len(command) == 5\
                and len(command.split()) == 2\
                and 0 <= int(command[0]) <= 7\
                and 0 <= int(command[1]) <= 7\
                and 0 <= int(command[3]) <= 7\
                and 0 <= int(command[4]) <= 7\
                :
            self.message += "Command \"{}\" is in move format.\n".format(command)
            return True
        else:
            self.message += "Move command \"{}\" not understood.\n".format(command)
            return False

    def is_legal_move(self, command):
        '''Checks if move is formatted like a move command, then checks for legality.'''
        # If this isn't even formatted like a move command, stop immediately.
        if not self.is_move_command(command):
            return False

        # Parse the move command.
        move = Movement(self.board, int(command[1]), int(command[0]), int(command[4]), int(command[3]))

        # Legality checks
        if move.piece_color != self.current_state[0]:
            self.message += "The {} at {}{} is not your piece to move.\n".format(move.piece, move.y1, move.x1)
            return False
        elif move.dx == 0 and move.dy == 0:
            self.message += "You must move the piece at least one space.\n"
            return False
        elif move.destination[0] == self.current_state[0]:
            self.message += "You cannot capture your own {}.\n".format(move.destination)
            return False
        else:
            # Apply the piece-specific rules.
            if move.piece[1] == "B"\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and abs(move.dx) == abs(move.dy):
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("B", move.piece)
                return True
            elif move.piece[1] == "R"\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and (move.dx == 0 or move.dy == 0):
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("R", move.piece)
                return True
            elif move.piece[1] == "Q"\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and ((abs(move.dx) == abs(move.dy)) or (move.dx == 0 or move.dy == 0)):
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("Q", move.piece)
                return True
            elif move.piece[1] == "K"\
                    and abs(move.dx) <= 1 and abs(move.dy) <= 1:
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("K", move.piece)
                return True
            elif move.piece[1] == "N"\
                    and ((abs(move.dx) == 1 and abs(move.dy) == 2)\
                    or (abs(move.dx) == 2 and abs(move.dy) == 1)):
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("N", move.piece)
                return True
            elif move.piece == "BP"\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and (move.dx == 0 and move.dy == 1 and move.destination == "")\
                    or (abs(move.dx) == 1 and move.dy == 1 and move.destination != "")\
                    or (move.y1 == 1 and move.dy == 2 and move.dx == 0):
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("BP", move.piece)
                return True
            elif move.piece == "WP"\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and (move.dx == 0 and move.dy == -1 and move.destination == "")\
                    or (abs(move.dx) == 1 and move.dy == -1 and move.destination != "")\
                    or (move.y1 == 6 and move.dy == -2 and move.dx == 0):
                self.message += "Rules for \"{}\" were applied to \"{}\".\n".format("WP", move.piece)
                return True
            else:
                self.message += "That is not a valid move for the {}.\n".format(move.piece)
                return False

    def collides(self, x1, y1, x2, y2):
        '''Determines whether there is an obstacle in the line of movement or not.'''
        dx = x2 - x1
        dy = y2 - y1
        x_range = [x1, x2]
        y_range = [y1, y2]
        piece = self.board[y1][x1]
        collision = False
        if x1 == x2:
            y_range.sort()
            for i in range(y_range[0] + 1, y_range[1]):
                obstacle = self.board[i][x1].strip()
                if obstacle != "":
                    collision = True
                    break
        elif y1 == y2:
            x_range.sort()
            for i in range(x_range[0] + 1, x_range[1]):
                obstacle = self.board[y1][i].strip()
                if obstacle != "":
                    collision = True
                    break
        elif abs(dx) == abs(dy):
            if x1 > x2:
                x_range.reverse()
                y_range.reverse()
            x_sign = sign(x_range[1] - x_range[0])
            y_sign = sign(y_range[1] - y_range[0])
            if x_sign == y_sign:
                for i, j in zip(range(x_range[0] + 1, x_range[1]), range(y_range[0] + 1, y_range[1])):
                    obstacle = self.board[j][i].strip()
                    if obstacle != "":
                        collision = True
                        break
            else:
                for i, j in zip(range(x_range[0] + 1, x_range[1]), range(1, abs(dy))):
                    j = y_range[0] - j
                    obstacle = self.board[j][i].strip()
                    if obstacle != "":
                        collision = True
                        break
        else:
            assert True, "The move \"{}{} {}{}\" can't be checked for collisions".format(x1, y1, x2, y2)

        if collision:
            self.message += "{} collided with {}.\n".format(piece, obstacle)
        return collision


def main():
    chess = Chess()
    chess.play()


# Only call main if program is run directly (not imported).
if __name__ == "__main__":
    os.system("clear")
    from sys import version
    print('Running with Python', version) # Double-check the version.

    main()
