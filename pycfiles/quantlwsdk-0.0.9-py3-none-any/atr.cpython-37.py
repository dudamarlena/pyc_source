# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\atr.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 3474 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical
from pyalgotrade.dataseries import bards

class ATREventWindow(technical.EventWindow):

    def __init__(self, period, useAdjustedValues):
        assert period > 1
        super(ATREventWindow, self).__init__(period)
        self._ATREventWindow__useAdjustedValues = useAdjustedValues
        self._ATREventWindow__prevClose = None
        self._ATREventWindow__value = None

    def _calculateTrueRange(self, value):
        ret = None
        if self._ATREventWindow__prevClose is None:
            ret = value.getHigh(self._ATREventWindow__useAdjustedValues) - value.getLow(self._ATREventWindow__useAdjustedValues)
        else:
            tr1 = value.getHigh(self._ATREventWindow__useAdjustedValues) - value.getLow(self._ATREventWindow__useAdjustedValues)
            tr2 = abs(value.getHigh(self._ATREventWindow__useAdjustedValues) - self._ATREventWindow__prevClose)
            tr3 = abs(value.getLow(self._ATREventWindow__useAdjustedValues) - self._ATREventWindow__prevClose)
            ret = max(max(tr1, tr2), tr3)
        return ret

    def onNewValue(self, dateTime, value):
        tr = self._calculateTrueRange(value)
        super(ATREventWindow, self).onNewValue(dateTime, tr)
        self._ATREventWindow__prevClose = value.getClose(self._ATREventWindow__useAdjustedValues)
        if value is not None:
            if self.windowFull():
                if self._ATREventWindow__value is None:
                    self._ATREventWindow__value = self.getValues().mean()
                else:
                    self._ATREventWindow__value = (self._ATREventWindow__value * (self.getWindowSize() - 1) + tr) / float(self.getWindowSize())

    def getValue(self):
        return self._ATREventWindow__value


class ATR(technical.EventBasedFilter):
    __doc__ = 'Average True Range filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr\n\n    :param barDataSeries: The BarDataSeries instance being filtered.\n    :type barDataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.\n    :param period: The average period. Must be > 1.\n    :type period: int.\n    :param useAdjustedValues: True to use adjusted Low/High/Close values.\n    :type useAdjustedValues: boolean.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, barDataSeries, period, useAdjustedValues=False, maxLen=None):
        if not isinstance(barDataSeries, bards.BarDataSeries):
            raise Exception('barDataSeries must be a dataseries.bards.BarDataSeries instance')
        super(ATR, self).__init__(barDataSeries, ATREventWindow(period, useAdjustedValues), maxLen)