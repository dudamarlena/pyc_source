# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/clock.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 485 bytes
import time

class Clock:

    def __init__(self, is_flat_out=False):
        self.is_flat_out = is_flat_out
        self._time = time.time()

    def time(self):
        if self.is_flat_out:
            return self._time
        else:
            return time.time()

    def sleep(self, delta_time):
        delta_time = max(delta_time, 0)
        if not self.is_flat_out:
            time.sleep(delta_time)
        else:
            self._time += delta_time