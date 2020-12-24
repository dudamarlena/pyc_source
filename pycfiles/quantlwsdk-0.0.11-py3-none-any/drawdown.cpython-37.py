# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\stratanalyzer\drawdown.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 3041 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import stratanalyzer
import datetime

class DrawDownHelper(object):

    def __init__(self):
        self._DrawDownHelper__highWatermark = None
        self._DrawDownHelper__lowWatermark = None
        self._DrawDownHelper__lastLow = None
        self._DrawDownHelper__highDateTime = None
        self._DrawDownHelper__lastDateTime = None

    def getDuration(self):
        return self._DrawDownHelper__lastDateTime - self._DrawDownHelper__highDateTime

    def getMaxDrawDown(self):
        return (self._DrawDownHelper__lowWatermark - self._DrawDownHelper__highWatermark) / float(self._DrawDownHelper__highWatermark)

    def getCurrentDrawDown(self):
        return (self._DrawDownHelper__lastLow - self._DrawDownHelper__highWatermark) / float(self._DrawDownHelper__highWatermark)

    def update(self, dateTime, low, high):
        if not low <= high:
            raise AssertionError
        else:
            self._DrawDownHelper__lastLow = low
            self._DrawDownHelper__lastDateTime = dateTime
            if self._DrawDownHelper__highWatermark is None or high >= self._DrawDownHelper__highWatermark:
                self._DrawDownHelper__highWatermark = high
                self._DrawDownHelper__lowWatermark = low
                self._DrawDownHelper__highDateTime = dateTime
            else:
                self._DrawDownHelper__lowWatermark = min(self._DrawDownHelper__lowWatermark, low)


class DrawDown(stratanalyzer.StrategyAnalyzer):
    __doc__ = 'A :class:`pyalgotrade.stratanalyzer.StrategyAnalyzer` that calculates\n    max. drawdown and longest drawdown duration for the portfolio.'

    def __init__(self):
        super(DrawDown, self).__init__()
        self._DrawDown__maxDD = 0
        self._DrawDown__longestDDDuration = datetime.timedelta()
        self._DrawDown__currDrawDown = DrawDownHelper()

    def calculateEquity(self, strat):
        return strat.getBroker().getEquity()

    def beforeOnBars(self, strat, bars):
        equity = self.calculateEquity(strat)
        self._DrawDown__currDrawDown.update(bars.getDateTime(), equity, equity)
        self._DrawDown__longestDDDuration = max(self._DrawDown__longestDDDuration, self._DrawDown__currDrawDown.getDuration())
        self._DrawDown__maxDD = min(self._DrawDown__maxDD, self._DrawDown__currDrawDown.getMaxDrawDown())

    def getMaxDrawDown(self):
        """Returns the max. (deepest) drawdown."""
        return abs(self._DrawDown__maxDD)

    def getLongestDrawDownDuration(self):
        """Returns the duration of the longest drawdown.

        :rtype: :class:`datetime.timedelta`.

        .. note::
            Note that this is the duration of the longest drawdown, not necessarily the deepest one.
        """
        return self._DrawDown__longestDDDuration