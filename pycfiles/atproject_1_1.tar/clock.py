# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: att/clock.py
# Compiled at: 2017-03-18 13:13:32
"""Provide a non-decreasing clock() function.

In Windows, time.clock() provides number of seconds from first call, so use
that.

In Unix, time.clock() is CPU time, and time.time() reports system time, which
may not be non-decreasing."""
import time, sys
_MAXFORWARD = 100
_FUDGE = 1

class RelativeTime(object):
    """Non-decreasing time implementation for Unix"""

    def __init__(self):
        self.time = time.time()
        self.offset = 0

    def get_time(self):
        """Calculate a non-decreasing time representation"""
        systemtime = time.time()
        now = systemtime + self.offset
        if self.time < now < self.time + _MAXFORWARD:
            self.time = now
        else:
            self.time += _FUDGE
            self.offset = self.time - systemtime
        return self.time


if sys.platform != 'win32':
    clock = RelativeTime().get_time
else:
    from time import clock