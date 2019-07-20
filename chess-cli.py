#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
A command-line chess game.

14 July 2019
"""

import os


class Chess(object):
    """The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces."""
    def __init__(self):
        """Set the board and wait for the start signal."""
        self.message = "Let the game begin!\n"
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
                self.update()
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

    def update(self):
        """Execute move, and update display"""
        # Get sanitized user input.
        command = input("{}, make your move: ".format(self.state)).strip().lower()

        # Execute the command.
        if command == "quit":
            print("Quitting chess.")
            self.state = "NONE WINS"
        elif command == "help":
            self.message += "There is no help available at this time.\n"
        elif self.is_legal_move(command):
            self.board[int(command[3])][int(command[4])] = self.board[int(command[0])][int(command[1])]
            self.board[int(command[0])][int(command[1])] = "  "
            self.message += "Move \"{}\" executed by \"{}\".\n".format(command, self.state)
            self.state = "WHITE" if self.state == "BLACK" else "BLACK"
        else:
            self.message += "\"{}\" is not a valid command.\n".format(command)
            self.state = self.state # Don't change the state.

    def is_legal_move(self, command):
        """Checks if move is formatted like a move command, then checks for legality."""
        # Is this a valid move command?
        if len(command) == 5\
                and len(command.split()) == 2\
                and 0 <= int(command[0]) <= 7\
                and 0 <= int(command[1]) <= 7\
                and 0 <= int(command[3]) <= 7\
                and 0 <= int(command[4]) <= 7\
                :
            x1 = int(command[1])
            x2 = int(command[4])
            y1 = int(command[0])
            y2 = int(command[3])
            piece = self.board[y1][x1]
            destination = self.board[y2][x2]
            dx = x2 - x1
            dy = y2 - y1

            # Is the move legal?
            if piece[0] != self.state[0]:
                self.message += "The {} is not your piece to move.\n".format(piece)
                return False
            #elif not self.collides(x1, x2, y1, y2):
            #    self.message += "You cannot capture your own {}.\n".format(destination)
            #    return False
            elif piece[0] == destination[0]:
                self.message += "You cannot capture your own {}.\n".format(destination)
                return False
            elif and dx == 0 and dy == 0:
                self.message += "You must move the piece at least one space.\n"
                return False
            else:
                # Apply the piece-specific rules.
                if piece[1] == "B"\
                        and abs(dx) == abs(dy):
                    return True
                elif piece[1] == "R"\
                        and (dx == 0 or dy == 0):
                    return True
                elif piece[1] == "Q"\
                        and (abs(dx) == abs(dy) or dx == 0 or dy == 0):
                    return True
                elif piece[1] == "K"\
                        and abs(dx) <= 1 and abs(dy) <= 1:
                    return True
                elif piece[1] == "N"\
                        and ((abs(dx) == 1 and abs(dy) == 2) or (abs(dx) == 2 and abs(dy) == 1)):
                    return True
                elif piece == "BP"\
                        and (dx == 0 and dy == 1 and destination.strip() == "")\
                        or (abs(dx) == 1 and dy == 1 and destination.strip() != "")\
                        or (y1 == 1 and dy == 2 and dx == 0):
                    return True
                else:
                    return False
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
