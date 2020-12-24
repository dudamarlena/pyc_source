# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/vwap.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical
from pyalgotrade.dataseries import bards

class VWAPEventWindow(technical.EventWindow):

    def __init__(self, windowSize, useTypicalPrice):
        super(VWAPEventWindow, self).__init__(windowSize, dtype=object)
        self.__useTypicalPrice = useTypicalPrice

    def getValue(self):
        ret = None
        if self.windowFull():
            cumTotal = 0
            cumVolume = 0
            for bar in self.getValues():
                if self.__useTypicalPrice:
                    cumTotal += bar.getTypicalPrice() * bar.getVolume()
                else:
                    cumTotal += bar.getPrice() * bar.getVolume()
                cumVolume += bar.getVolume()

            ret = cumTotal / float(cumVolume)
        return ret


class VWAP(technical.EventBasedFilter):
    """Volume Weighted Average Price filter.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.
    :param period: The number of values to use to calculate the VWAP.
    :type period: int.
    :param useTypicalPrice: True if the typical price should be used instead of the closing price.
    :type useTypicalPrice: boolean.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, period, useTypicalPrice=False, maxLen=None):
        assert isinstance(dataSeries, bards.BarDataSeries), 'dataSeries must be a dataseries.bards.BarDataSeries instance'
        super(VWAP, self).__init__(dataSeries, VWAPEventWindow(period, useTypicalPrice), maxLen)

    def getPeriod(self):
        return self.getWindowSize()