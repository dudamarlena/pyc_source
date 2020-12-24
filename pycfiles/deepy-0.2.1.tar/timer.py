# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/timer.py
# Compiled at: 2016-04-20 00:05:45
import time

class Timer(object):
    """
    A timer for measure runing time.
    """

    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        return

    def end(self):
        """
        Stop the timer.
        """
        self.end_time = time.time()

    def report(self):
        """
        Report elapsed time.
        """
        if not self.end_time:
            self.end()
        print 'Time:', (self.end_time - self.start_time) / 60, 'mins'