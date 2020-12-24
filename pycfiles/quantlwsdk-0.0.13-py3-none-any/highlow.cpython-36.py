# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\technical\highlow.py
# Compiled at: 2019-06-05 03:26:15
# Size of source mod 2**32: 2668 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical

class HighLowEventWindow(technical.EventWindow):

    def __init__(self, windowSize, useMin):
        super(HighLowEventWindow, self).__init__(windowSize)
        self._HighLowEventWindow__useMin = useMin

    def getValue(self):
        ret = None
        if self.windowFull():
            values = self.getValues()
            if self._HighLowEventWindow__useMin:
                ret = values.min()
            else:
                ret = values.max()
        return ret


class High(technical.EventBasedFilter):
    __doc__ = 'This filter calculates the highest value.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use to calculate the highest value.\n    :type period: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, maxLen=None):
        super(High, self).__init__(dataSeries, HighLowEventWindow(period, False), maxLen)


class Low(technical.EventBasedFilter):
    __doc__ = 'This filter calculates the lowest value.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use to calculate the lowest value.\n    :type period: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, maxLen=None):
        super(Low, self).__init__(dataSeries, HighLowEventWindow(period, True), maxLen)