# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\queries\windows.py
# Compiled at: 2013-12-18 14:05:11
from ..logs import Log
from ..maths import Math
from ..multiset import Multiset
from ..stats import Z_moment, stats2z_moment, z_moment2stats

class AggregationFunction(object):

    def __init__(self):
        """
        RETURN A ZERO-STATE AGGREGATE
        """
        Log.error('not implemented yet')

    def add(self, value):
        """
        ADD value TO AGGREGATE
        """
        Log.error('not implemented yet')

    def merge(self, agg):
        """
        ADD TWO AGGREGATES TOGETHER
        """
        Log.error('not implemented yet')

    def end(self):
        """
        RETURN AGGREGATE
        """
        pass


class Exists(AggregationFunction):

    def __init__(self):
        object.__init__(self)
        self.total = False

    def add(self, value):
        if value == None:
            return
        else:
            self.total = True
            return

    def merge(self, agg):
        if agg.total:
            self.total = True

    def end(self):
        return self.total


class WindowFunction(AggregationFunction):

    def __init__(self):
        """
        RETURN A ZERO-STATE AGGREGATE
        """
        Log.error('not implemented yet')

    def sub(self, value):
        """
        REMOVE value FROM AGGREGATE
        """
        Log.error('not implemented yet')


class Stats(WindowFunction):

    def __init__(self):
        object.__init__(self)
        self.total = Z_moment(0, 0, 0)

    def add(self, value):
        if value == None:
            return
        else:
            self.total += stats2z_moment(value)
            return

    def sub(self, value):
        if value == None:
            return
        else:
            self.total -= stats2z_moment(value)
            return

    def merge(self, agg):
        self.total += agg.total

    def end(self):
        return z_moment2stats(self.total)


class Min(WindowFunction):

    def __init__(self):
        object.__init__(self)
        self.total = Multiset()

    def add(self, value):
        if value == None:
            return
        else:
            self.total.add(value)
            return

    def sub(self, value):
        if value == None:
            return
        else:
            self.total.remove(value)
            return

    def end(self):
        return Math.min(self.total)


class Max(WindowFunction):

    def __init__(self):
        object.__init__(self)
        self.total = Multiset()

    def add(self, value):
        if value == None:
            return
        else:
            self.total.add(value)
            return

    def sub(self, value):
        if value == None:
            return
        else:
            self.total.remove(value)
            return

    def end(self):
        return Math.max(self.total)


class Count(WindowFunction):

    def __init__(self):
        object.__init__(self)
        self.total = 0

    def add(self, value):
        if value == None:
            return
        else:
            self.total += 1
            return

    def sub(self, value):
        if value == None:
            return
        else:
            self.total -= 1
            return

    def end(self):
        return self.total


class Sum(WindowFunction):

    def __init__(self):
        object.__init__(self)
        self.total = 0

    def add(self, value):
        if value == None:
            return
        else:
            self.total += value
            return

    def sub(self, value):
        if value == None:
            return
        else:
            self.total -= value
            return

    def end(self):
        return self.total