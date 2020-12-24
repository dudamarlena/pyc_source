# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/stratanalyzer/drawdown.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import stratanalyzer
import datetime

class DrawDownHelper(object):

    def __init__(self):
        self.__highWatermark = None
        self.__lowWatermark = None
        self.__lastLow = None
        self.__highDateTime = None
        self.__lastDateTime = None
        return

    def getDuration(self):
        return self.__lastDateTime - self.__highDateTime

    def getMaxDrawDown(self):
        return (self.__lowWatermark - self.__highWatermark) / float(self.__highWatermark)

    def getCurrentDrawDown(self):
        return (self.__lastLow - self.__highWatermark) / float(self.__highWatermark)

    def update(self, dateTime, low, high):
        assert low <= high
        self.__lastLow = low
        self.__lastDateTime = dateTime
        if self.__highWatermark is None or high >= self.__highWatermark:
            self.__highWatermark = high
            self.__lowWatermark = low
            self.__highDateTime = dateTime
        else:
            self.__lowWatermark = min(self.__lowWatermark, low)
        return


class DrawDown(stratanalyzer.StrategyAnalyzer):
    """A :class:`pyalgotrade.stratanalyzer.StrategyAnalyzer` that calculates
    max. drawdown and longest drawdown duration for the portfolio."""

    def __init__(self):
        super(DrawDown, self).__init__()
        self.__maxDD = 0
        self.__longestDDDuration = datetime.timedelta()
        self.__currDrawDown = DrawDownHelper()

    def calculateEquity(self, strat):
        return strat.getBroker().getEquity()

    def beforeOnBars(self, strat, bars):
        equity = self.calculateEquity(strat)
        self.__currDrawDown.update(bars.getDateTime(), equity, equity)
        self.__longestDDDuration = max(self.__longestDDDuration, self.__currDrawDown.getDuration())
        self.__maxDD = min(self.__maxDD, self.__currDrawDown.getMaxDrawDown())

    def getMaxDrawDown(self):
        """Returns the max. (deepest) drawdown."""
        return abs(self.__maxDD)

    def getLongestDrawDownDuration(self):
        """Returns the duration of the longest drawdown.

        :rtype: :class:`datetime.timedelta`.

        .. note::
            Note that this is the duration of the longest drawdown, not necessarily the deepest one.
        """
        return self.__longestDDDuration