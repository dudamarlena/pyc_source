# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/sqlitext.py
# Compiled at: 2011-09-20 08:48:55
"""Extend sqlite aggregate functions"""
from math import isnan

def to_float(value):
    """Return None if value is not a valid float."""
    try:
        ret = float(value)
        if isnan(ret):
            ret = None
    except ValueError:
        ret = None

    return ret


class Percentile(object):

    def __init__(self, percentile):
        self.percentile = percentile
        self.items = []

    def step(self, value):
        v = to_float(value)
        if v is not None:
            self.items.append(v)
        return

    def finalize(self):
        if len(self.items) < 1:
            return None
        else:
            index = int(len(self.items) * self.percentile)
            self.items.sort()
            return self.items[index]


class P10(Percentile):

    def __init__(self):
        Percentile.__init__(self, 0.1)


class Median(Percentile):

    def __init__(self):
        Percentile.__init__(self, 0.5)


class P90(Percentile):

    def __init__(self):
        Percentile.__init__(self, 0.9)


class P95(Percentile):

    def __init__(self):
        Percentile.__init__(self, 0.95)


class P98(Percentile):

    def __init__(self):
        Percentile.__init__(self, 0.98)


class StdDev(object):
    """Sample standard deviation"""

    def __init__(self):
        self.items = []

    def step(self, value):
        v = to_float(value)
        if v is not None:
            self.items.append(v)
        return

    def finalize(self):
        if len(self.items) < 1:
            return None
        else:
            items = self.items
            total = sum(items)
            avg = total / len(items)
            print 'tot: %f, avg: %f' % (total, avg)
            sdsq = sum([ (i - avg) ** 2 for i in items ])
            ret = (sdsq / (len(items) - 1 or 1)) ** 0.5
            return ret


class First(object):
    """Sample standard deviation"""

    def __init__(self):
        self.first = None
        return

    def step(self, value):
        if self.first is None and value:
            self.first = value
        return

    def finalize(self):
        return self.first


def interval(start, period, t):
    return start + int(t - start) / int(period) * period


def fl_label(step, number, rtype, description):
    """Build a funkload label."""
    if description:
        lb = description
    else:
        lb = rtype
    ret = '%3.3d-%3.3d %s' % (step, number, lb)
    return ret


def add_aggregates(db):
    db.create_aggregate('p10', 1, P10)
    db.create_aggregate('med', 1, Median)
    db.create_aggregate('p90', 1, P90)
    db.create_aggregate('p95', 1, P95)
    db.create_aggregate('p98', 1, P98)
    db.create_aggregate('stddev', 1, P98)
    db.create_aggregate('first', 1, First)
    db.create_function('interval', 3, interval)
    db.create_function('fl_label', 4, fl_label)