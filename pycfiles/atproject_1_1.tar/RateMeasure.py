# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: att/Client/RateMeasure.py
# Compiled at: 2017-03-18 13:14:56
from att.clock import clock
FACTOR = 0.999

class RateMeasure:

    def __init__(self):
        self.last = None
        self.time = 1.0
        self.got = 0.0
        self.remaining = None
        self.broke = False
        self.got_anything = False
        self.last_checked = None
        self.rate = 0
        self.lastten = False
        return

    def data_came_in(self, amount):
        if not self.got_anything:
            self.got_anything = True
            self.last = clock()
            return
        self.update(amount)

    def data_rejected(self, amount):
        pass

    def get_time_left(self, left):
        t = clock()
        if not self.got_anything:
            return
        else:
            if t - self.last > 15:
                self.update(0)
            try:
                remaining = left / self.rate
                if not self.lastten and remaining <= 10:
                    self.lastten = True
                if self.lastten:
                    return remaining
                delta = max(remaining / 20, 2)
                if self.remaining is None:
                    self.remaining = remaining
                elif abs(self.remaining - remaining) > delta:
                    self.remaining = remaining
                else:
                    self.remaining -= t - self.last_checked
            except ZeroDivisionError:
                self.remaining = None

            if self.remaining is not None and self.remaining < 0.1:
                self.remaining = 0.1
            self.last_checked = t
            return self.remaining

    def update(self, amount):
        t = clock()
        exp = int(t) - int(self.last)
        self.time *= FACTOR ** exp
        self.got *= FACTOR ** exp
        self.got += amount
        if t - self.last < 20:
            self.time += t - self.last
        self.last = t
        try:
            self.rate = self.got / self.time
        except ZeroDivisionError:
            pass