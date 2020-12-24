# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/four_keys/four_keys_board_items.py
# Compiled at: 2019-04-21 17:56:51
from __future__ import absolute_import
from enum import IntEnum

class FourKeysBoardItems(IntEnum):
    EMPTY = 0
    WALL = 1
    KEY = 2
    PLAYER1 = 3
    PLAYER2 = 4
    PLAYER3 = 5
    PLAYER4 = 6
    PLAYER5 = 7
    PLAYER6 = 8
    PLAYER7 = 9
    PLAYER8 = 10
    OTHER_PLAYER = 11