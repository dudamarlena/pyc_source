# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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