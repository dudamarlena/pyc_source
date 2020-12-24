# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\technical\lw_crossSeries.py
# Compiled at: 2019-07-20 10:03:40
# Size of source mod 2**32: 2526 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import dataseries

class crossSignals(dataseries.SequenceDataSeries):
    __doc__ = '\n    这个地方，为什么入参要是2个序列，因为这里是要判断任意两个序列的交叉。如果在\n    类里面来生产序列，你不知道未来 是什么序列进来。一般可能是close的 ma 两个序列来判断交叉\n\n    但是有时候，可能需要判断2个ema序列交叉。那在类里面写死就不好。\n    '

    def __init__(self, dataSeries1, dataSeries2, maxLen=None):
        super(crossSignals, self).__init__(maxLen)
        self._crossSignals__ds1 = dataSeries1
        self._crossSignals__ds2 = dataSeries2
        dataSeries2.getNewValueEvent().subscribe(self._crossSignals__onNewValue)

    def __onNewValue(self, dataSeries, dateTime, value):
        if len(self._crossSignals__ds1) >= 2 and len(self._crossSignals__ds2) >= 2:
            dtFromDs1 = self._crossSignals__ds1.getDateTimes()[(-1)]
            dtFromDs2 = self._crossSignals__ds2.getDateTimes()[(-1)]
            assert dtFromDs1 == dtFromDs2
            sedtFromDs1 = self._crossSignals__ds1.getDateTimes()[(-2)]
            sedtFromDs2 = self._crossSignals__ds2.getDateTimes()[(-2)]
            assert sedtFromDs1 == sedtFromDs2
            newValue = 0
            if self._crossSignals__ds1[(-2)] is not None and self._crossSignals__ds2[(-2)] is not None:
                if self._crossSignals__ds1[(-2)] < self._crossSignals__ds2[(-2)]:
                    if self._crossSignals__ds1[(-1)] >= self._crossSignals__ds2[(-1)]:
                        newValue = 1
                if self._crossSignals__ds1[(-2)] > self._crossSignals__ds2[(-2)]:
                    if self._crossSignals__ds1[(-1)] <= self._crossSignals__ds2[(-1)]:
                        newValue = -1
                self.appendWithDateTime(dtFromDs1, newValue)