#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Description.

R Jeffery
Date
"""

#import pygame
#pygame.init()
import os


class Chess(object):
    """The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces."""
    def __init__(self):
        """Start in the setup state, and go from there."""
        self.state = "SETUP"

    def setup(self):
        """Set the board."""
        self.board = [["BR","BK","BB","BQ","BK","BB","BK","BR"],\
                      ["BP","BP","BP","BP","BP","BP","BP","BP"],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["WP","WP","WP","WP","WP","WP","WP","WP"],\
                      ["WR","WK","WB","WQ","WK","WB","WK","WR"]]

        self.state = "WHITE" # Because white always goes first.

    def play(self):
        """The main game loop"""
        while self.state != "NONE WIN"\
                and self.state != "WHITE WIN"\
                and self.state != "BLACK WIN"\
                :
            print("game state: {}".format(self.state))

            # Update the game state.
            if self.state == "SETUP":
                self.setup()
            elif self.state == "BLACK" or self.state == "WHITE":
                self.draw_board()
                self.move()
            else:
                assert False, "Impossible state {} requested.".format(self.state)

        print("{} is the winner!".format(self.state.split()[0]))

    def draw_board(self):
        """Print the board in the terminal."""
        for i, row in enumerate(self.board):
            print(8-i, row)

        print("    ", end="")
        for i in range(0,8):
            print("{}     ".format(chr(i+65)), end="")

        print()

    def move(self):
        """Execute move, and update display"""
        # Sanitize the user input.
        move = input("{}, make your move: ".format(self.state)).strip().lower()

        # Clear screen for next turn.
        os.system("clear")

        # Execute the move.
        if move == "quit":
            print("Quitting chess.")
            self.state = "NONE WIN"
        elif self.is_legal_move(move):
            print("Move \"{}\" executed by \"{}\".".format(move, self.state))
            self.state = "WHITE" if self.state == "BLACK" else "BLACK"
        else:
            print("\"{}\" is not a legal move. You must make a legal move or quit.".format(move))
            self.state = self.state # Don't change the state.

    def is_legal_move(self, move):
        """Checks if move is formatted like a move command, then checks for legality."""
        if len(move) == 5 and len(move.split()) == 2:
            return True
        else:
            return False


def main():
    chess = Chess()
    chess.play()


# Only call main if program is run directly (not imported).
if __name__ == "__main__":
    os.system("clear")
    from sys import version
    print('Running with Python', version) # Double-check the version.

    main()
