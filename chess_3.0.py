#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
cli-chess
A command-line chess game.

14 July 2019
'''

import os
import pyglet


def sign(x):
    '''Return +1 for positive numbers, -1 for negative numbers, and 0 for zero.'''
    assert type(x) == int, '{} is not an int. sign() only takes ints'

    if x == 0:
        return 0
    else:
        return x // abs(x)


class Chess(object):
    '''
    The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces.
    '''
    def __init__(self):
        '''Set the board and wait for the start signal.'''
        self.messages = []
        self.board = [['BR','BN','BB','BQ','BK','BB','BN','BR'],\
                      ['BP','BP','BP','BP','BP','BP','BP','BP'],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['WP','WP','WP','WP','WP','WP','WP','WP'],\
                      ['WR','WN','WB','WQ','WK','WB','WN','WR']]
        self.state = 'WHITE'
        self.selection = []
    
    def __repr__(self):
        '''Print the game in the terminal.'''
        return (self.board, self.state, self.selection, self.selection)
    
    def __str__(self):
        string = ''

        for i, row in enumerate(self.board):
            string += '{}   {}\n'.format(i, row)
        string += '     '
        for i in range(0,8):
            string += '{}     '.format(i)
        string += '\n'

        string += 'State: {}\n'.format(self.state)
        string += 'Selections: {}\n'.format(self.selection)
        
        string += 'Latest Messages:\n'
        for message in self.messages:
            string += '{}\n'.format(message)
        self.messages = []

        return string

    def _is_legal_move(self, x1, y1, x2, y2):
        ''' Checks if move is allowed in chess. '''
        moved_piece = self.board[y1][x1]
        captured_piece = self.board[y2][x2]
        dx = x2 - x1
        dy = y2 - y1

        # Legality checks
        if moved_piece[0] != self.state[0]:
            self.messages.append('The {} at {}{} is not your piece to move.'.format(moved_piece, x1, y1))
            return False
        elif dx == 0 and dy == 0:
            self.messages.append('You must move the piece at least one space.')
            return False
        elif captured_piece[0] == self.state[0]:
            self.messages.append('You cannot capture your own {}.'.format(captured_piece))
            return False
        else:
            # Apply the piece-specific rules.
            if moved_piece[1] == 'B'\
                    and not self._collides(x1, y1, x2, y2)\
                    and abs(dx) == abs(dy):
                self.messages.append('Rules for {} were applied to {}.'.format('B', moved_piece))
                return True
            elif moved_piece[1] == 'R'\
                    and not self._collides(x1, y1, x2, y2)\
                    and (dx == 0 or dy == 0):
                self.messages.append('Rules for {} were applied to {}.'.format('R', moved_piece))
                return True
            elif moved_piece[1] == 'Q'\
                    and not self._collides(x1, y1, x2, y2)\
                    and ((abs(dx) == abs(dy)) or (dx == 0 or dy == 0)):
                self.messages.append('Rules for {} were applied to {}.'.format('Q', moved_piece))
                return True
            elif moved_piece[1] == 'K'\
                    and abs(dx) <= 1 and abs(dy) <= 1:
                self.messages.append('Rules for {} were applied to {}.'.format('K', moved_piece))
                return True
            elif moved_piece[1] == 'N'\
                    and ((abs(dx) == 1 and abs(dy) == 2)\
                    or (abs(dx) == 2 and abs(dy) == 1)):
                self.messages.append('Rules for {} were applied to {}.'.format('N', moved_piece))
                return True
            elif moved_piece == 'BP'\
                    and not self._collides(x1, y1, x2, y2)\
                    and (dx == 0 and dy == 1 and captured_piece == '')\
                    or (abs(dx) == 1 and dy == 1 and captured_piece != '')\
                    or (y1 == 1 and dy == 2 and dx == 0):
                self.messages.append('Rules for {} were applied to {}.'.format('BP', moved_piece))
                return True
            elif moved_piece == 'WP'\
                    and not self._collides(x1, y1, x2, y2)\
                    and (dx == 0 and dy == -1 and captured_piece == '')\
                    or (abs(dx) == 1 and dy == -1 and captured_piece != '')\
                    or (y1 == 6 and dy == -2 and dx == 0):
                self.messages.append('Rules for {} were applied to {}.'.format('WP', moved_piece))
                return True
            else:
                self.messages.append('That is not a valid move for the {}.'.format(moved_piece))
                return False

    def _collides(self, x1, y1, x2, y2):
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
                if obstacle != '':
                    collision = True
                    break
        elif y1 == y2:
            x_range.sort()
            for i in range(x_range[0] + 1, x_range[1]):
                obstacle = self.board[y1][i].strip()
                if obstacle != '':
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
                    if obstacle != '':
                        collision = True
                        break
            else:
                for i, j in zip(range(x_range[0] + 1, x_range[1]), range(1, abs(dy))):
                    j = y_range[0] - j
                    obstacle = self.board[j][i].strip()
                    if obstacle != '':
                        collision = True
                        break
        else:
            assert True, 'The move "{}{} {}{}" cannot be checked for collisions'.format(x1, y1, x2, y2)

        if collision:
            self.messages.append('{} collided with {}.'.format(piece, obstacle))
        
        return collision

    def quit_game(self):
        ''' Terminate the game. '''
        self.messages.append('{} gave up and flipped the board.'.format(self.state))
        self.state = 'NONE WINS'
        self.messages.append('{}!'.format(self.state))
    
    def forfeit_turn(self):
        ''' Skip player's turn '''
        self.messages.append('{} forfeit their turn.'.format(self.state))
        self.state = 'WHITE' if self.state == 'BLACK' else 'BLACK'
        self.selection = []

    def display_help(self):
        ''' Show the help text. '''
        self.messages.append('Enter one of the following commands: quit, help, pass, select, move.')
        self.state = self.state

    def add_selection(self, coordinate):
        ''' Get selection input and store it. '''
        if not coordinate.isnumeric():
            self.messages.append('Coordinate selection input, {}, is not a numeric string.'.format(coordinate))
            return False
        elif len(coordinate) != 2:
            self.messages.append('Coordinate selection input has {} digits, not 2.'.format(len(coordinate)))
            return False
        elif not 0 <= int(coordinate[0]) <= 7 or not 0 <= int(coordinate[1]) <= 7:
            self.messages.append('{} is not within bounds of board.'.format(coordinate))
            return False
        else:
            self.messages.append('{} selected coordinate {}.'.format(self.state, coordinate))
            self.selection.append( (coordinate[0], coordinate[1]) )
            return True
    
    def execute_move(self, x1, y1, x2, y2):
        ''' Attempt to make a legal move with the entered coordinates. '''
        if self._is_legal_move(x1, y1, x2, y2):
            moved_piece = self.board[y1][x1]
            captured_piece = self.board[y2][x2]
            self.board[y2][x2] = moved_piece
            self.board[y1][x1] = '  '
            self.messages.append('Move {}{} to {}{} was executed by {}.'.format(x1, y1, x2, y2, self.state))
            self.messages.append('{} captured {}.'.format(moved_piece, captured_piece))

            if captured_piece == 'WK':
                self.state = 'BLACK WINS'
                self.messages.append('{}!'.format(self.state))
            elif captured_piece == 'BK':
                self.state = 'WHITE WINS'
                self.messages.append('{}!'.format(self.state))
            else:
                self.state = 'WHITE' if self.state == 'BLACK' else 'BLACK'
        else:
            self.messages.append('Illegal move attempted. No move was executed.')

        self.selection = []


def main():
    chess = Chess()
    print(chess)

    chess.execute_move(4,6,4,4)
    print(chess)
    chess.execute_move(6,0,5,2)
    print(chess)
    chess.execute_move(3,7,3,4)
    print(chess)
    chess.execute_move(3,7,5,5)
    print(chess)
    chess.execute_move(5,2,4,4)
    print(chess)
    chess.execute_move(5,5,5,1)
    print(chess)
    chess.forfeit_turn()
    chess.execute_move(5,1,4,0)
    print(chess)


# Only call main if program is run directly (not imported).
if __name__ == '__main__':
    os.system('clear')
    from sys import version
    print('Running with Python', version) # Double-check the version.

    main()
