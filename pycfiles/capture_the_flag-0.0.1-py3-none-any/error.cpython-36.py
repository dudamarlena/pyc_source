# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/documented/ctf/ctf/error.py
# Compiled at: 2020-04-19 14:38:43
# Size of source mod 2**32: 399 bytes


class IllegalMoveError(Exception):
    __doc__ = 'Raised when a user attempts to move a unit in an illegal\n    direction.\n\n    '


class OutOfTurnError(Exception):
    __doc__ = 'Raised when a user attempts to move a unit out of turn.'


class GameNotFoundError(Exception):
    __doc__ = 'Raised when a user attempts to move a piece or render a frame\n    before invoking `new_game`.\n\n    '