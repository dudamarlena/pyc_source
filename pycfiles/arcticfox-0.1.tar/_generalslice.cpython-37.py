# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/date/_generalslice.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 1812 bytes
from enum import Enum

class Intervals(Enum):
    OPEN_CLOSED, CLOSED_OPEN, OPEN_OPEN, CLOSED_CLOSED = range(1101, 1105)


OPEN_CLOSED, CLOSED_OPEN, OPEN_OPEN, CLOSED_CLOSED = INTERVALS = Intervals.__members__.values()

class GeneralSlice(object):
    """GeneralSlice"""

    def __init__(self, start, end, step=None, interval=CLOSED_CLOSED):
        self.start = start
        self.end = end
        self.step = step
        self.interval = interval

    @property
    def startopen(self):
        """True if the start of the range is open (item > start),
        False if the start of the range is closed (item >= start)."""
        return self.interval in (OPEN_CLOSED, OPEN_OPEN)

    @property
    def endopen(self):
        """True if the end of the range is open (item < end),
        False if the end of the range is closed (item <= end)."""
        return self.interval in (CLOSED_OPEN, OPEN_OPEN)