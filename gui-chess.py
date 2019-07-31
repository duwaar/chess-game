#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
A command-line chess game.

14 July 2019
'''

import os, pyglet


def sign(x):
    '''Return +1 for positive numbers, -1 for negative numbers, and 0 for zero.'''
    assert type(x) == int, "{} is not an int. sign() only takes ints"

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
        self.piece = board[y1][x1]
        self.piece_color = self.piece[0]
        self.destination = board[y2][x2]


class Chess(object):
    '''
    The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces.
    '''
    def __init__(self):
        '''Setup the board and the graphics window, and wait for the start signal.'''
        self.message = ""
        self.previous_state = "SETUP"
        self.current_state = "WHITE"
        self.board = [["BR","BN","BB","BQ","BK","BB","BN","BR"],\
                      ["BP","BP","BP","BP","BP","BP","BP","BP"],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["WP","WP","WP","WP","WP","WP","WP","WP"],\
                      ["WR","WN","WB","WQ","WK","WB","WN","WR"]]

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        self.window = pyglet.window.Window(width=800, height=800)
        self.window.set_caption('Python Chess')

        @self.window.event
        def on_draw():
            if self.current_state == self.previous_state:
                self.previous_state = self.current_state
                # Draw in the pyglet window.
                self.draw_board()
                self.batch.draw()

            # Print in the command line.
            print()
            print(self.message)
            self.message = ""

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.message += "mouse motion: x{}, y{}, dx{}, dy{}\n".format(x, y, dx, dy)

        @self.window.event
        def on_mouse_press(key, modifiers):
            self.message += "mouse press: key{}, mod{}\n".format(key, modifiers)

    def change_state(self, new_state):
        '''Update the current and previous states.'''
        self.previous_state = self.current_state
        self.current_state = new_state

    def play(self):
        '''The main game'''
        # Set initial conditions.
        self.message += "Let the game begin!\n\n"
        self.change_state("WHITE")

        # Start the game loop.
        pyglet.app.run()

        # Print the final message.
        print("{}".format(self.message))

    def update(self):
        '''Execute move, and update display'''
        self.draw_board()
        # Get sanitized user input.
        command = input("{}, make your move: ".format(self.current_state)).strip().lower()

        # Execute the command.
        if command == "quit":
            self.message += "{} gave up and flipped the board.\n".format(self.current_state)
            self.change_state("NONE WINS")
        elif command == "pass":
            self.message += "{} forfeit their turn.\n".format(self.current_state)
            self.current_state = "WHITE" if self.current_state == "BLACK" else "BLACK"
        elif command == "help":
            self.message += "There is no help available at this time.\n"
            # Don't change state.
        elif self.is_legal_move(command):
            move = Movement(self.board, command[1], command[0], command[4], command[3])
            captured_piece = move.destination
            self.board[move.y2][move.x2] = self.board[move.y1][move.x1]
            self.board[move.y1][move.x1] = ""
            self.message += "Move \"{}\" was executed by {}.\n".format(command, self.current_state)
            self.message += "{} captured {}.\n".format(move.piece, captured_piece)

            if captured_piece == "WK":
                self.change_state("BLACK WINS")
            elif captured_piece == "BK":
                self.change_state("WHITE WINS")
            else:
                self.change_state("WHITE") if self.current_state == "BLACK" else "BLACK"
        else:
            self.message += "\"{}\" is not a valid command.\n".format(command)
            # Don't change the state.

    def draw_board(self):
        '''Display the board.'''
        # Print the board in the command line.
        for i, row in enumerate(self.board):
            print(i, row)
            #print(8-i, row)

        print("    ", end="")
        for i in range(0,8):
            print("{}     ".format(i), end="")
            #print("{}     ".format(chr(i+65)), end="")

        print()

        # Draw the board in the pyglet window.
        height, window = self.window.get_size()
        for j, row in enumerate(self.board):
            for i, column in enumerate(row):
                if (i + j) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)


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
