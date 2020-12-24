# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/Selection.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1006 bytes
from vaitk import core

class Selection:

    def __init__(self):
        self.clear()
        self.changed = core.VSignal(self)

    def isValid(self):
        return self._start_line is not None and self._end_line is not None

    def clear(self):
        self._start_line = None
        self._end_line = None

    @property
    def num_lines(self):
        return self.high_line - self.low_line + 1

    @property
    def low_line(self):
        x = (self._start_line, self._end_line)
        return min(x)

    @property
    def high_line(self):
        x = (self._start_line, self._end_line)
        return max(x)

    @property
    def start_line(self):
        return self._start_line

    @start_line.setter
    def start_line(self, start_line):
        self._start_line = start_line
        self.changed.emit()

    @property
    def end_line(self):
        return self._end_line

    @end_line.setter
    def end_line(self, end_line):
        self._end_line = end_line
        self.changed.emit()