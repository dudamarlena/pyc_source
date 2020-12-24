# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/date/_generalslice.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 1812 bytes
from enum import Enum

class Intervals(Enum):
    OPEN_CLOSED, CLOSED_OPEN, OPEN_OPEN, CLOSED_CLOSED = range(1101, 1105)


OPEN_CLOSED, CLOSED_OPEN, OPEN_OPEN, CLOSED_CLOSED = INTERVALS = Intervals.__members__.values()

class GeneralSlice(object):
    __doc__ = 'General slice object, supporting open/closed ranges:\n\n    =====  ====  ============================  ===============================\n    start  end  interval                      Meaning\n    -----  ----  ----------------------------  -------------------------------\n    None   None                                any item\n    a      None  CLOSED_CLOSED or CLOSED_OPEN  item >= a\n    a      None  OPEN_CLOSED or OPEN_OPEN      item > a\n    None   b     CLOSED_CLOSED or OPEN_CLOSED  item <= b\n    None   b     CLOSED_OPEN or OPEN_OPEN      item < b\n    a      b     CLOSED_CLOSED                 item >= a and item <= b\n    a      b     OPEN_CLOSED                   item > a and item <= b\n    a      b     CLOSED_OPEN                   item >= a and item < b\n    a      b     OPEN_OPEN                     item > a and item < b\n    =====  ====  ============================  ===============================\n    '

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