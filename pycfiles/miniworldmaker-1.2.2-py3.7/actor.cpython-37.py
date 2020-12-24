# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\tokens\actor.py
# Compiled at: 2019-08-09 04:14:19
# Size of source mod 2**32: 305 bytes
import miniworldmaker.tokens.token as board_token

class Actor(board_token.Token):
    __doc__ = ' Initializes a new actor\n\n    An actor is a specialized token.\n\n    Args:\n        position: The position on the board as tuple.\n        If None, the actor will not be placed on the board.\n\n    '