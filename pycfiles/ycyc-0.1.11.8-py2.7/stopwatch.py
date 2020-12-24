# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tools/stopwatch.py
# Compiled at: 2016-02-25 04:17:16
import time

class Stopwatch(object):
    """
    A sadness timer
    """

    def __init__(self):
        self.start_on = None
        self._duration = 0
        self._enable = False
        return

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, val):
        if val:
            self.start_on = time.time()
            self._enable = True
        else:
            self._duration = self.duration
            self._enable = False

    @property
    def duration(self):
        if self.enable:
            return time.time() - self.start_on + self._duration
        return self._duration

    def __enter__(self):
        self.enable = True
        return self

    def __exit__(self, typ, val, trbk):
        self.enable = False