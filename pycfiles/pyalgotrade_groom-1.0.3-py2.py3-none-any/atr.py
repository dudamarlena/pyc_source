# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/atr.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade import technical
from pyalgotrade.dataseries import bards

class ATREventWindow(technical.EventWindow):

    def __init__(self, period, useAdjustedValues):
        assert period > 1
        super(ATREventWindow, self).__init__(period)
        self.__useAdjustedValues = useAdjustedValues
        self.__prevClose = None
        self.__value = None
        return

    def _calculateTrueRange(self, value):
        ret = None
        if self.__prevClose is None:
            ret = value.getHigh(self.__useAdjustedValues) - value.getLow(self.__useAdjustedValues)
        else:
            tr1 = value.getHigh(self.__useAdjustedValues) - value.getLow(self.__useAdjustedValues)
            tr2 = abs(value.getHigh(self.__useAdjustedValues) - self.__prevClose)
            tr3 = abs(value.getLow(self.__useAdjustedValues) - self.__prevClose)
            ret = max(max(tr1, tr2), tr3)
        return ret

    def onNewValue(self, dateTime, value):
        tr = self._calculateTrueRange(value)
        super(ATREventWindow, self).onNewValue(dateTime, tr)
        self.__prevClose = value.getClose(self.__useAdjustedValues)
        if value is not None and self.windowFull():
            if self.__value is None:
                self.__value = self.getValues().mean()
            else:
                self.__value = (self.__value * (self.getWindowSize() - 1) + tr) / float(self.getWindowSize())
        return

    def getValue(self):
        return self.__value


class ATR(technical.EventBasedFilter):
    """Average True Range filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr

    :param barDataSeries: The BarDataSeries instance being filtered.
    :type barDataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.
    :param period: The average period. Must be > 1.
    :type period: int.
    :param useAdjustedValues: True to use adjusted Low/High/Close values.
    :type useAdjustedValues: boolean.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, barDataSeries, period, useAdjustedValues=False, maxLen=None):
        if not isinstance(barDataSeries, bards.BarDataSeries):
            raise Exception('barDataSeries must be a dataseries.bards.BarDataSeries instance')
        super(ATR, self).__init__(barDataSeries, ATREventWindow(period, useAdjustedValues), maxLen)