# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/christian/documented/ctf/ctf/error.py
# Compiled at: 2020-04-19 14:38:43
# Size of source mod 2**32: 399 bytes


class IllegalMoveError(Exception):
    """IllegalMoveError"""
    pass


class OutOfTurnError(Exception):
    """OutOfTurnError"""
    pass


class GameNotFoundError(Exception):
    """GameNotFoundError"""
    pass