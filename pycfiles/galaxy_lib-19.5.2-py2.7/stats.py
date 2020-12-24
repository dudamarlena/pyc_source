# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/jobs/metrics/collectl/stats.py
# Compiled at: 2018-04-20 03:19:42
""" Primitive module for tracking running statistics without storing values in
memory.
"""

class StatisticsTracker(object):

    def __init__(self):
        self.min = None
        self.max = None
        self.count = 0
        self.sum = 0
        return

    def track(self, value):
        if self.min is None or value < self.min:
            self.min = value
        if self.max is None or value > self.max:
            self.max = value
        self.count += 1
        self.sum += value
        return

    @property
    def avg(self):
        if self.count > 0:
            return self.sum / self.count
        else:
            return
            return