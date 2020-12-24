# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\roc.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 2207 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical

class ROCEventWindow(technical.EventWindow):

    def __init__(self, windowSize):
        super(ROCEventWindow, self).__init__(windowSize)

    def getValue(self):
        ret = None
        if self.windowFull():
            prev = self.getValues()[0]
            actual = self.getValues()[(-1)]
            if actual is not None:
                if prev is not None:
                    diff = float(actual - prev)
                    if diff == 0:
                        ret = float(0)
                    else:
                        if prev != 0:
                            ret = diff / prev
        return ret


class RateOfChange(technical.EventBasedFilter):
    __doc__ = 'Rate of change filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:rate_of_change_roc_and_momentum.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param valuesAgo: The number of values back that a given value will compare to. Must be > 0.\n    :type valuesAgo: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, valuesAgo, maxLen=None):
        assert valuesAgo > 0
        super(RateOfChange, self).__init__(dataSeries, ROCEventWindow(valuesAgo + 1), maxLen)