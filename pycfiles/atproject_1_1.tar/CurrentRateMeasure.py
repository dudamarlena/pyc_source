# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: att/Client/CurrentRateMeasure.py
# Compiled at: 2017-03-18 13:15:02
from att.clock import clock

class Measure:

    def __init__(self, max_rate_period, fudge=1):
        self.max_rate_period = max_rate_period
        self.ratesince = clock() - fudge
        self.last = self.ratesince
        self.rate = 0.0
        self.total = 0

    def update_rate(self, amount):
        self.total += amount
        t = clock()
        self.rate = (self.rate * (self.last - self.ratesince) + amount) / (t - self.ratesince + 0.0001)
        self.last = t
        if self.ratesince < t - self.max_rate_period:
            self.ratesince = t - self.max_rate_period

    def get_rate(self):
        self.update_rate(0)
        return self.rate

    def get_rate_noupdate(self):
        return self.rate

    def time_until_rate(self, newrate):
        if self.rate <= newrate:
            return 0
        t = clock() - self.ratesince
        return self.rate * t / newrate - t

    def get_total(self):
        return self.total