# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\board_positions\board_rect.py
# Compiled at: 2020-02-12 00:39:37
# Size of source mod 2**32: 2479 bytes
import pygame
import miniworldmaker.app as app
from miniworldmaker.board_positions import board_position

class BoardRect(pygame.Rect):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.board = app.App.board

    def is_tile(self):
        if self.width == self.board.tile_size:
            if self.height == self.board.tile_size:
                return True
        return False

    def borders(self):
        """
        Gets all borders the rect ist touching.

        Returns: A list of borders as strings: "left", "bottom", "right", or "top"

        """
        borders = []
        if self.topleft[0] <= 0:
            borders.append('left')
        if self.topleft[1] + self.height >= self.board.height:
            borders.append('bottom')
        if self.topleft[0] + self.width >= self.board.width:
            borders.append('right')
        if self.topleft[1] <= 0:
            borders.append('top')
        return borders

    def is_on_board(self):
        topleft_on_board = board_position.BoardPosition(self.left, self.top).is_on_board()
        bottom_right_on_board = board_position.BoardPosition(self.right, self.bottom).is_on_board()
        return topleft_on_board or bottom_right_on_board

    def colors(self, rect_borders=None):
        colors = []
        for x in range(self.width):
            if not rect_borders is None:
                if 'left' in rect_borders:
                    color = self.board.background.color_at((self.x + x, self.y))
                    if color not in colors:
                        colors.append(color)
                if rect_borders is None or 'right' in rect_borders:
                    color = self.board.background.color_at((self.x + x, self.y + self.height))
                    if color not in colors:
                        colors.append(color)

        for y in range(self.height):
            if not rect_borders is None:
                if 'top' in rect_borders:
                    color = self.board.background.color_at((self.x, self.y + y))
                    if color not in colors:
                        colors.append(color)
                if rect_borders is None or 'bottom' in rect_borders:
                    color = self.board.background.color_at((self.x + self.width, self.y + y))
                    if color not in colors:
                        colors.append(color)

        return colors