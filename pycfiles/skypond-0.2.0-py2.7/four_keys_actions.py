# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/four_keys/four_keys_actions.py
# Compiled at: 2019-04-21 17:56:55
from __future__ import absolute_import
from enum import IntEnum

class FourKeysActions(IntEnum):
    NOTHING = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    DROP_KEY = 6
    ATTACK = 7