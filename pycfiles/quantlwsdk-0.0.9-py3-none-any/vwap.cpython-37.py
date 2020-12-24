# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\vwap.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 2529 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical
from pyalgotrade.dataseries import bards

class VWAPEventWindow(technical.EventWindow):

    def __init__(self, windowSize, useTypicalPrice):
        super(VWAPEventWindow, self).__init__(windowSize, dtype=object)
        self._VWAPEventWindow__useTypicalPrice = useTypicalPrice

    def getValue(self):
        ret = None
        if self.windowFull():
            cumTotal = 0
            cumVolume = 0
            for bar in self.getValues():
                if self._VWAPEventWindow__useTypicalPrice:
                    cumTotal += bar.getTypicalPrice() * bar.getVolume()
                else:
                    cumTotal += bar.getPrice() * bar.getVolume()
                cumVolume += bar.getVolume()

            ret = cumTotal / float(cumVolume)
        return ret


class VWAP(technical.EventBasedFilter):
    __doc__ = 'Volume Weighted Average Price filter.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.\n    :param period: The number of values to use to calculate the VWAP.\n    :type period: int.\n    :param useTypicalPrice: True if the typical price should be used instead of the closing price.\n    :type useTypicalPrice: boolean.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, useTypicalPrice=False, maxLen=None):
        assert isinstance(dataSeries, bards.BarDataSeries), 'dataSeries must be a dataseries.bards.BarDataSeries instance'
        super(VWAP, self).__init__(dataSeries, VWAPEventWindow(period, useTypicalPrice), maxLen)