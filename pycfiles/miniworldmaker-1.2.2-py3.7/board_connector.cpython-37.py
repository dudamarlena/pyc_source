# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\tokens\board_connector.py
# Compiled at: 2019-08-09 04:14:43
# Size of source mod 2**32: 1367 bytes
import math

class BoardConnector:

    def __init__(self, token, board):
        super().__init__()
        self.token = token
        self.board = board

    def remove_from_board(self):
        """Removes a token from board
        """
        self.board.tokens.remove(self.token)
        self.token.board = None

    def point_towards_position(self, destination) -> float:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = self.token.rect.center
        x = destination[0] - pos[0]
        y = destination[1] - pos[1]
        if x != 0:
            m = y / x
            if x < 0:
                self.token.direction = math.degrees(math.atan(m)) - 90
            else:
                self.token.direction = math.degrees(math.atan(m) + 90)
            return self.token.direction
        m = 0
        if destination[1] > self.token.position[1]:
            self.token.direction = 180
            return self.token.direction
        self.token.direction = 0
        return self.token.direction