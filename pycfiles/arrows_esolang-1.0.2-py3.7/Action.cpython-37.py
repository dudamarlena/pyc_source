# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrows_esolang/Action.py
# Compiled at: 2019-10-31 01:39:26
# Size of source mod 2**32: 321 bytes
from enum import Enum

class ActionType(Enum):
    END = 0
    ADD = 1
    PUSH_LEFT = 2
    SUBTRACT_LEFT = 3
    PUSH_RIGHT = 4
    SUBTRACT_RIGHT = 5
    PRINT = 6
    READ = 7


class Action(object):

    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value