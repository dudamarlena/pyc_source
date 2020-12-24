# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\cumret.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 1912 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical

class CumRetEventWindow(technical.EventWindow):

    def __init__(self):
        super(CumRetEventWindow, self).__init__(2)
        self._CumRetEventWindow__prevCumRet = 0

    def getValue(self):
        ret = None
        if self.windowFull():
            values = self.getValues()
            prev = values[0]
            actual = values[1]
            netReturn = (actual - prev) / float(prev)
            ret = (1 + self._CumRetEventWindow__prevCumRet) * (1 + netReturn) - 1
            self._CumRetEventWindow__prevCumRet = ret
        return ret


class CumulativeReturn(technical.EventBasedFilter):
    __doc__ = 'This filter calculates cumulative returns over another dataseries.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, maxLen=None):
        super(CumulativeReturn, self).__init__(dataSeries, CumRetEventWindow(), maxLen)