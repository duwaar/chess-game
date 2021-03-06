#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
A chess game.

Elaine Jeffery
4 February 2020
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


class ChessGame(object):
    '''
    The Chess object holds the game's state, playing pieces, board, and methods for moving and
    capturing pieces.
    '''
    def __init__(self):
        '''Set the board and wait for the start signal.'''
        self.messages = []
        self.board = [
                ['WR','WN','WB','WK','WQ','WB','WN','WR'],
                ['WP','WP','WP','WP','WP','WP','WP','WP'],
                ['  ','  ','  ','  ','  ','  ','  ','  '],
                ['  ','  ','  ','  ','  ','  ','  ','  '],
                ['  ','  ','  ','  ','  ','  ','  ','  '],
                ['  ','  ','  ','  ','  ','  ','  ','  '],
                ['BP','BP','BP','BP','BP','BP','BP','BP'],
                ['BR','BN','BB','BK','BQ','BB','BN','BR'],
                ]
        self.state = 'WHITE'
        self.selection = []
    
    def __repr__(self):
        '''Print the game in the terminal.'''
        return (self.board, self.state, self.selection, self.messages)
    
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
        
        string += 'Buffered Messages:\n'
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
                    and ((dx == 0\
                            and dy == -1\
                            and captured_piece == '  ')\
                        or (abs(dx) == 1\
                            and dy == -1\
                            and captured_piece != '  ')\
                        or (y1 == 6\
                            and dy == -2\
                            and dx == 0)):
                self.messages.append('Rules for {} were applied to {}.'.format('BP', moved_piece))
                return True
            elif moved_piece == 'WP'\
                    and not self._collides(x1, y1, x2, y2)\
                    and ((dx == 0\
                            and dy == 1\
                            and captured_piece == '  ')\
                        or (abs(dx) == 1\
                            and dy == 1\
                            and captured_piece != '  ')\
                        or (y1 == 1\
                            and dy == 2\
                            and dx == 0)):
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

    def read_messages(self, num):
        ''' Returns the specified number of messages from the end of the queue. '''
        return self.messages[-num:]

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
        if self.state != 'WHITE' and self.state != 'BLACK':
            self.messages.append('The game is over! {}!'.format(self.state))
            return False
        if type(coordinate) != tuple or len(coordinate) != 2:
            self.messages.append('Received {}. Expected a tuple (x, y).'.format(coordinate))
            return False
        elif not 0 <= int(coordinate[0]) <= 7 or not 0 <= int(coordinate[1]) <= 7:
            self.messages.append('Tuple {} is not within bounds of board.'.format(coordinate))
            return False
        else:
            self.messages.append('{} selected coordinate {}.'.format(self.state, coordinate))
            self.selection.append( (coordinate[0], coordinate[1]) )
            if len(self.selection) > 1:
                x1, y1 = self.selection[0]
                x2, y2 = self.selection[1]
                self.execute_move(x1, y1, x2, y2)
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


class ChessApp(pyglet.window.Window):
    ''' Generates the graphics and gets the user input for the chess game. '''
    def __init__(self):
        super().__init__(width=520, height=700, visible=False)

        self.set_caption('Python Chess')
        icon = pyglet.image.load('assets/icon.png', decoder=pyglet.image.codecs.png.PNGImageDecoder())
        self.set_icon(icon)

        width, height = self.get_size()
        self.margin = 16
        self.board_side = min([width, height]) - self.margin
        self.board_bottom = height - self.board_side
        self.board_left = self.margin
        self.square_side = self.board_side // 8

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.draw_sprites = []

        self.mouse_position = (0, 0)
        self.mouse_press = (0, 0)

        self.chess_game = ChessGame()
        self.piece_images = self._load_piece_images()

        @self.event
        def on_draw():
            self._draw_background()
            self._draw_foreground()
            self.batch.draw()

            self.batch = pyglet.graphics.Batch()
            self.draw_sprites = []

        @self.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_position = (x, y)

        @self.event
        def on_mouse_press(x, y, button, mods):
            self.mouse_press = (x, y)
            coordinate = self._pixel_to_square((x, y))
            self.chess_game.add_selection(coordinate)
        
        self.set_visible(visible=True)
        
    def _load_piece_images(self):
        piece_names = [
                ('BQ','b_queen.png'),
                ('BK','b_king.png'),
                ('BP','b_pawn.png'),
                ('BN','b_knight.png'),
                ('BR','b_rook.png'),
                ('BB','b_bishop.png'),
                ('WQ','w_queen.png'),
                ('WK','w_king.png'),
                ('WP','w_pawn.png'),
                ('WN','w_knight.png'),
                ('WR','w_rook.png'),
                ('WB','w_bishop.png'),
                ]
        
        piece_images = {}
        for name in piece_names:
            file_name = 'assets/' + name[1]
            image = pyglet.image.load(file_name, decoder=pyglet.image.codecs.png.PNGImageDecoder())
            piece_images[name[0]] = image

        return piece_images

    def _pixel_to_square(self, coordinate):
        square_i = (coordinate[0] - self.board_left)    // self.square_side
        square_j = (coordinate[1] - self.board_bottom)  // self.square_side
        return square_i, square_j

    def _draw_background(self):
        width, height = self.get_size()
        # Draw a border for the chess board.
        self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                ('v2i', (0,     height,\
                         width, height,\
                         width, height - self.board_side - self.margin,\
                         0,     height - self.board_side - self.margin)),\
                ('c3B', (120, 120, 120) * 4))
        
        # Draw the squares on the board.
        mouseover = self._pixel_to_square(self.mouse_position)
        for i in range(8):
            for j in range(8):
                square_bottom   = self.square_side *  j      + self.board_bottom
                square_top      = self.square_side * (j + 1) + self.board_bottom
                square_left     = self.square_side *  i      + self.board_left
                square_right    = self.square_side * (i + 1) + self.board_left
                
                if mouseover[0] == i and mouseover[1] == j:
                    square_color = (0, 240, 0)
                elif (i + j) % 2 == 0:
                    square_color = (240, 240, 255)
                else:
                    square_color = (0, 0, 0)
                
                self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                        ('v2i', (square_left,  square_bottom,\
                                 square_right, square_bottom,\
                                 square_right, square_top,\
                                 square_left,  square_top)),\
                        ('c3B', square_color * 4))
        
        # Draw the message box.
        self.batch.add(4, pyglet.gl.GL_QUADS, self.background,\
                ('v2i', (0,     0,\
                         width, 0,\
                         width, height - self.board_side - self.margin,\
                         0,     height - self.board_side - self.margin)),\
                ('c3B', (210, 210, 210) * 4))
        
    def _draw_foreground(self):
        # Draw the pieces
        for j, row in enumerate(self.chess_game.board):
            for i, piece in enumerate(row):
                if piece.strip() != '':
                    sprite = pyglet.sprite.Sprite(
                            self.piece_images[piece],
                            batch=self.batch,
                            group=self.foreground)
                    rescale = self.square_side / sprite.width
                    sprite.scale = rescale

                    piece_left      = self.board_left   + i * self.square_side
                    piece_bottom    = self.board_bottom + j * self.square_side
                    sprite.update(x=piece_left, y=piece_bottom)

                    self.draw_sprites.append(sprite)

        # Draw the messages
        messages = ''
        for new_message in self.chess_game.read_messages(9):
            messages = messages + '-> ' + new_message + '\n'
        pyglet.text.Label(
                text=messages,
                font_name='Courier New',
                font_size=12,
                color=(0, 0, 0, 255),
                anchor_x='left', x=0, width=self.width,
                anchor_y='bottom', y=0, height=(self.height - self.board_side - self.margin),
                multiline=True,
                batch=self.batch,
                group=self.foreground)
   
    def play(self):
        ''' Start the application. '''
        pyglet.app.run()


def main():
    game = ChessApp()
    game.play()


# Only call main if program is run directly (not imported).
if __name__ == '__main__':
    os.system('clear')
    from sys import version
    print('Running with Python', version) # Double-check the version.

    main()
