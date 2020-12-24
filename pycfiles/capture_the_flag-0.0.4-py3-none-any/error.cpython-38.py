# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/capture-the-flag/capture-the-flag/ctf/error.py
# Compiled at: 2020-04-26 14:02:35
# Size of source mod 2**32: 399 bytes


class IllegalMoveError(Exception):
    __doc__ = 'Raised when a user attempts to move a unit in an illegal\n    direction.\n\n    '


class OutOfTurnError(Exception):
    __doc__ = 'Raised when a user attempts to move a unit out of turn.'


class GameNotFoundError(Exception):
    __doc__ = 'Raised when a user attempts to move a piece or render a frame\n    before invoking `new_game`.\n\n    '