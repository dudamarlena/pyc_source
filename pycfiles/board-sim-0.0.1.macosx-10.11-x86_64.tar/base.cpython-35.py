# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/board-sim/core/base.py
# Compiled at: 2016-09-10 17:41:57
# Size of source mod 2**32: 1462 bytes
from collections import deque, namedtuple

class Circuit:

    def __init__(self):
        self.components = []


class ComponentBase:

    def __init__(self):
        self.out = deque(maxlen=1)
        self.data_in = deque(maxlen=1)
        self.prev_state = vars(self)
        self.flags = None

    def update(self):
        pass