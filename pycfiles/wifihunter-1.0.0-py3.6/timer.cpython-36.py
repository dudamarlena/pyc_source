# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/handlers/timer.py
# Compiled at: 2020-01-15 14:18:24
# Size of source mod 2**32: 1054 bytes
import time

class Timer(object):

    def __init__(self, seconds):
        self.start_time = time.time()
        self.end_time = self.start_time + seconds

    def remaining(self):
        return max(0, self.end_time - time.time())

    def ended(self):
        return self.remaining() == 0

    def running_time(self):
        return time.time() - self.start_time

    def __str__(self):
        """ Time remaining in minutes (if > 1) and seconds, e.g. 5m23s"""
        return Timer.secs_to_str(self.remaining())

    @staticmethod
    def secs_to_str(seconds):
        """Human-readable seconds. 193 -> 3m13s"""
        if seconds < 0:
            return '-%ds' % seconds
        else:
            rem = int(seconds)
            hours = int(rem / 3600)
            mins = int(rem % 3600 / 60)
            secs = rem % 60
            if hours > 0:
                return '%dh%dm%ds' % (hours, mins, secs)
            if mins > 0:
                return '%dm%ds' % (mins, secs)
            return '%ds' % secs