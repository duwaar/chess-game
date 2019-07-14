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
        """Set the board and wait for the start signal."""
        self.message = "Let the game begin!"
        self.board = [["BR","BN","BB","BQ","BK","BB","BN","BR"],\
                      ["BP","BP","BP","BP","BP","BP","BP","BP"],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["  ","  ","  ","  ","  ","  ","  ","  "],\
                      ["WP","WP","WP","WP","WP","WP","WP","WP"],\
                      ["WR","WN","WB","WQ","WK","WB","WN","WR"]]
        self.draw_board()
        input("The board is set. Hit enter to begin.")
        os.system("clear")
        self.state = "WHITE" # Because white always goes first.

    def play(self):
        """The main game loop"""
        while self.state != "NONE WINS"\
                and self.state != "WHITE WINS"\
                and self.state != "BLACK WINS"\
                :
            # Provide feedback to player(s).
            os.system("clear")
            print("{}".format(self.message))
            self.message = ""

            # Update the game state.
            if self.state == "BLACK" or self.state == "WHITE":
                self.draw_board()
                self.move()
            else:
                assert False, "Impossible state {} requested.".format(self.state)

        print("{}!".format(self.state))

    def draw_board(self):
        """Print the board in the terminal."""
        for i, row in enumerate(self.board):
            print(i, row)
            #print(8-i, row)

        print("    ", end="")
        for i in range(0,8):
            print("{}     ".format(i), end="")
            #print("{}     ".format(chr(i+65)), end="")

        print()

    def move(self):
        """Execute move, and update display"""
        # Get sanitized user input.
        move = input("{}, make your move: ".format(self.state)).strip().lower()

        # Execute the move.
        if move == "quit":
            print("Quitting chess.")
            self.state = "NONE WINS"
        elif self.is_legal_move(move):
            self.board[int(move[3])][int(move[4])] = self.board[int(move[0])][int(move[1])]
            self.board[int(move[0])][int(move[1])] = "  "
            self.message += "Move \"{}\" executed by \"{}\".\n".format(move, self.state)
            self.state = "WHITE" if self.state == "BLACK" else "BLACK"
        else:
            self.message += "\"{}\" is not a legal move. You must make a legal move or quit.\n".format(move)
            self.state = self.state # Don't change the stat.

    def is_legal_move(self, move):
        """Checks if move is formatted like a move command, then checks for legality."""
        if len(move) == 5\
                and len(move.split()) == 2\
                and self.board[int(move[0])][int(move[1])].strip() != ""\
                :
                #and 0 <= int(move[0]) <= 7\
                #and 0 <= int(move[1]) <= 7\
                #and 0 <= int(move[3]) <= 7\
                #and 0 <= int(move[4]) <= 7\
                #:
            piece = self.board[int(move[0])][int(move[1])]
            if piece[0] != self.state[0]:
                self.message += "You cannot move your opponent's pieces.\n"
                return False
            return True
        else:
            self.message += "Input not understood.\n"
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
