# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/reporter/timer.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 537 bytes
import time

class Timer:

    def __init__(self):
        self._start = None
        self._duration = None

    def start(self):
        self._start = time.time()
        return self

    def stop(self):
        self._duration = time.time() - self._start if self.duration is None else self._duration
        return self.duration

    @property
    def duration(self):
        return self._duration

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()