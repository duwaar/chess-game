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


class Movement(object):
    '''Stores movement information for clearer and more convenient movement operations.'''
    def __init__(self, board, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.x2 = int(x2)
        self.y1 = int(y1)
        self.y2 = int(y2)

        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1
        self.piece = board[self.y1][self.x1]
        self.piece_color = self.piece[0]
        self.destination = board[self.y2][self.x2]
    
    def __str__(self):
        return '{}{} to {}{}'.format(self.x1, self.y1, self.x2, self.y2)


class Chess(object):
    '''
    The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces.
    '''
    def __init__(self):
        '''Set the board and wait for the start signal.'''
        self.message = ''
        self.board = [['BR','BN','BB','BQ','BK','BB','BN','BR'],\
                      ['BP','BP','BP','BP','BP','BP','BP','BP'],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['  ','  ','  ','  ','  ','  ','  ','  '],\
                      ['WP','WP','WP','WP','WP','WP','WP','WP'],\
                      ['WR','WN','WB','WQ','WK','WB','WN','WR']]
        
        self.selection = []

        '''
        self.window = pyglet.window.Window(width=600, height=700)
        self.window.set_caption('Python Chess')

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        self.mouse_position = (0, 0)
        self.mouse_click = (0, 0)

        @self.window.event
        def on_draw():
            self.draw_board()

        @self.window.event
        def on_key_press(key, modifiers):
            pass

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            pass

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            pass
        '''

    def play(self):
        '''The main game'''
        self.print_board()
        input('The board is set. Hit enter to begin.')
        self.message += 'Let the game begin!\n'
        os.system('clear')
        self.state = 'WHITE' # Because white always goes first.
        play = True
        while play:
            # Provide feedback to player(s).
            os.system('clear')
            print(self.message)
            self.message = ''

            # Update the game state.
            if self.state == 'NONE WINS'\
                    or self.state == 'WHITE WINS'\
                    or self.state == 'BLACK WINS':
                play = False
                self.message += '{}!'.format(self.state)
            elif self.state == 'BLACK' or self.state == 'WHITE':
                self.update()
            else:
                assert False, 'Impossible state {} requested.'.format(self.state)

        print('{}'.format(self.message))

    def update(self):
        '''Execute move, and update display'''
        self.print_board()
        # Get sanitized user input.
        command = input('{}, make your move: '.format(self.state)).strip().lower()
        #self.draw_board()

        # Execute the command.
        if command == 'quit':
            self.quit_game()
        elif command == 'pass':
            self.forfeit_turn()
        elif command == 'help':
            self.display_help()
        elif command == 'select':
            self.get_selection()
        elif command == 'move':
            self.execute_move()
        else:
            self.message += '\'{}\' is not a valid command.\n'.format(command)
            self.state = self.state # Don't change the state.
    
    def quit_game(self):
        ''' Terminate the game. '''
        self.message += '{} gave up and flipped the board.\n'.format(self.state)
        self.state = 'NONE WINS'
    
    def forfeit_turn(self):
        ''' Skip player's turn '''
        self.message += '{} forfeit their turn.\n'.format(self.state)
        self.state = 'WHITE' if self.state == 'BLACK' else 'BLACK'
        self.selection = []

    def display_help(self):
        ''' Show the help text. '''
        self.message += 'Enter one of the following commands: quit, help, pass, select, move.\n'
        self.state = self.state

    def get_selection(self):
        ''' Get selection input and store it. '''
        self.message += '{} selected a coordinate.\n'.format(self.state)
        coordinate = input('Select a coordinate on the board: ')
        assert coordinate.isnumeric(), 'Coordinate selection input is not a numeric string.'
        assert len(coordinate) == 2, 'Coordinate selection input has {} digits, not 2.'.format(len(coordinate))
        self.selection.append( (coordinate[0], coordinate[1]) )
    
    def execute_move(self):
        ''' Attempt to make a legal move with the stored coordinates. '''
        if self.is_legal_move():
            move = Movement(self.board,\
                self.selection[0][1],\
                self.selection[0][0],\
                self.selection[1][1],\
                self.selection[1][0],\
                )
            captured_piece = self.board[int(move.x1)][int(move.y1)]
            self.board[move.y2][move.x2] = self.board[move.y1][move.x1]
            self.board[move.y1][move.x1] = ''
            self.message += 'Move \'{}\' was executed by {}.\n'.format(str(move), self.state)
            self.message += '{} captured {}.\n'.format(move.piece, captured_piece)

            if captured_piece == 'WK':
                self.state = 'BLACK WINS'
            elif captured_piece == 'BK':
                self.state = 'WHITE WINS'
            else:
                self.state = 'WHITE' if self.state == 'BLACK' else 'BLACK'
        
        self.selection = []

    def print_board(self):
        '''Print the board in the terminal.'''
        for i, row in enumerate(self.board):
            print(i, row)
            #print(8-i, row)

        print('    ', end='')
        for i in range(0,8):
            print('{}     '.format(i), end='')
            #print('{}     '.format(chr(i+65)), end='')

        print()
        print('Selections: {}'.format(self.selection))
        print()

    def draw_board(self):
        ''' Generate the board graphics in the game window. '''
        # Basic dimensions
        width, height = self.window.get_size()
        margin = 16
        if width <= height:
            small_side = width
            large_side = height
        else:
            small_side = height
            large_side = width
        
        border = 16
        board_side = small_side - border
        square_side = board_side // 8

        # The background
        self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                ('v2i',    (0,      0,\
                            0,      height,\
                            width,  height,\
                            width,  0)),\
                ('c3B', (250, 250, 250) * 4))

        # The foreground
        pyglet.text.Label(text=self.message,\
                    font_name='Courier New',\
                    font_size=12,\
                    color=(0, 0, 0, 255),\
                    x=0, y=0,\
                    width=width,\
                    height=height - board_side - border,\
                    anchor_x='left',\
                    anchor_y='bottom',\
                    multiline=True,\
                    batch=self.batch,\
                    group=self.foreground)

    def is_legal_move(self):
        ''' Checks if move is allowed in chess. '''

        # Parse the move command.
        move = Movement(self.board,\
            self.selection[0][1],\
            self.selection[0][0],\
            self.selection[1][1],\
            self.selection[1][0])

        # Legality checks
        if move.piece_color != self.state[0]:
            self.message += 'The {} at {}{} is not your piece to move.\n'.format(move.piece, move.y1, move.x1)
            return False
        elif move.dx == 0 and move.dy == 0:
            self.message += 'You must move the piece at least one space.\n'
            return False
        elif move.destination[0] == self.state[0]:
            self.message += 'You cannot capture your own {}.\n'.format(move.destination)
            return False
        else:
            # Apply the piece-specific rules.
            if move.piece[1] == 'B'\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and abs(move.dx) == abs(move.dy):
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('B', move.piece)
                return True
            elif move.piece[1] == 'R'\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and (move.dx == 0 or move.dy == 0):
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('R', move.piece)
                return True
            elif move.piece[1] == 'Q'\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and ((abs(move.dx) == abs(move.dy)) or (move.dx == 0 or move.dy == 0)):
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('Q', move.piece)
                return True
            elif move.piece[1] == 'K'\
                    and abs(move.dx) <= 1 and abs(move.dy) <= 1:
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('K', move.piece)
                return True
            elif move.piece[1] == 'N'\
                    and ((abs(move.dx) == 1 and abs(move.dy) == 2)\
                    or (abs(move.dx) == 2 and abs(move.dy) == 1)):
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('N', move.piece)
                return True
            elif move.piece == 'BP'\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and (move.dx == 0 and move.dy == 1 and move.destination == '')\
                    or (abs(move.dx) == 1 and move.dy == 1 and move.destination != '')\
                    or (move.y1 == 1 and move.dy == 2 and move.dx == 0):
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('BP', move.piece)
                return True
            elif move.piece == 'WP'\
                    and not self.collides(move.x1, move.y1, move.x2, move.y2)\
                    and (move.dx == 0 and move.dy == -1 and move.destination == '')\
                    or (abs(move.dx) == 1 and move.dy == -1 and move.destination != '')\
                    or (move.y1 == 6 and move.dy == -2 and move.dx == 0):
                self.message += 'Rules for \'{}\' were applied to \'{}\'.\n'.format('WP', move.piece)
                return True
            else:
                self.message += 'That is not a valid move for the {}.\n'.format(move.piece)
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
            self.message += '{} collided with {}.\n'.format(piece, obstacle)
        return collision


def main():
    chess = Chess()
    chess.play()


# Only call main if program is run directly (not imported).
if __name__ == '__main__':
    os.system('clear')
    from sys import version
    print('Running with Python', version) # Double-check the version.

    main()
