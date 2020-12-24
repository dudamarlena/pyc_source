# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\technical\kdj.py
# Compiled at: 2019-07-23 05:21:08
# Size of source mod 2**32: 2339 bytes
from pyalgotrade.technical import ma
from pyalgotrade.technical import highlow
from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards
from pyalgotrade import commonHelpBylw

class KDJ:
    __doc__ = '\n    '

    def __init__(self, barDataSeries, N, M1, M2, useAdjustedValues=False, maxLen=None):
        if not isinstance(barDataSeries, bards.BarDataSeries):
            raise Exception('barDataSeries must be a dataseries.bards.BarDataSeries instance')
        else:
            if not N > 0:
                raise AssertionError
            elif not M1 > 0:
                raise AssertionError
            assert M2 > 0
        self._KDJ__useAdjustedValues = useAdjustedValues
        self._KDJ__K = dataseries.SequenceDataSeries(maxLen)
        self._KDJ__D = ma.SMA(self._KDJ__K, M2, maxLen)
        self._KDJ__J = dataseries.SequenceDataSeries(maxLen)
        self._KDJ__rsvLLWindow = highlow.HighLowEventWindow(N, True)
        self._KDJ__rsvHHWindow = highlow.HighLowEventWindow(N, False)
        self._KDJ__KWindow = ma.SMAEventWindow(M1)
        barDataSeries.getNewValueEvent().subscribe(self._KDJ__onNewValue)

    def __onNewValue(self, dataSeries, dateTime, value):
        self._KDJ__rsvLLWindow.onNewValue(dateTime, value.getLow(self._KDJ__useAdjustedValues))
        self._KDJ__rsvHHWindow.onNewValue(dateTime, value.getHigh(self._KDJ__useAdjustedValues))
        if self._KDJ__rsvLLWindow.windowFull():
            currClose = value.getClose(self._KDJ__useAdjustedValues)
            currLL = self._KDJ__rsvLLWindow.getValue()
            currHH = self._KDJ__rsvHHWindow.getValue()
            rsv = commonHelpBylw.round_up((currClose - currLL) * 100 / (currHH - currLL), 2)
            self._KDJ__KWindow.onNewValue(dateTime, rsv)
            if self._KDJ__KWindow.windowFull():
                k = self._KDJ__KWindow.getValue()
                self._KDJ__K.appendWithDateTime(dateTime, k)
                if k is not None:
                    if len(self._KDJ__D) > 1:
                        if self._KDJ__D[(-1)] is not None:
                            j = commonHelpBylw.round_up(3 * k - 2 * self._KDJ__D[(-1)], 2)
                            self._KDJ__J.appendWithDateTime(dateTime, j)

    def getK(self):
        return self._KDJ__K

    def getD(self):
        return self._KDJ__D

    def getJ(self):
        return self._KDJ__J