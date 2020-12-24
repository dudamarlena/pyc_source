# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/Writers/progressTimer.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 866 bytes
"""
Created on July 26, 2018

@author: jimk
"""
import time

class ProgressTimer:
    __doc__ = '\n    Class to calculate counts and rates\n    '
    etStart: time
    calls: int
    total: int
    print_interval: int

    def __init__(self, total, interval=15):
        self.calls = 0
        self.print_interval = interval
        self.total = total
        self.etStart = None

    def tick(self):
        """
        Increments the counter, prints rate info
        :return:
        """
        if self.calls == 0:
            self.etStart = time.perf_counter()
        self.calls += 1
        if self.calls % self.print_interval == 0:
            y = time.perf_counter()
            print(' %d calls ( %3.2f %%).  Rate: %5.2f /sec' % (
             self.calls, 100 * self.calls / self.total, self.print_interval / (y - self.etStart)))
            self.etStart = y