# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\boards\physics_board.py
# Compiled at: 2020-02-02 15:32:46
# Size of source mod 2**32: 859 bytes
from miniworldmaker.boards import pixel_board
from miniworldmaker.connectors import physics_connector

class PhysicsBoard(pixel_board.PixelBoard):

    def add_to_board(self, token, position):
        super().add_to_board(token, position)
        if not hasattr(token, 'setup_physics'):

            @token.register
            def setup_physics(self):
                pass

    def _add_board_connector(self, token, position):
        token.board_connector = physics_connector.PhysicsBoardConnector(token, self)
        token.topleft = (position[0], position[1])