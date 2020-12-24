# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\dataseries\aligned.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 4040 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import dataseries

def datetime_aligned(ds1, ds2, maxLen=None):
    """
    Returns two dataseries that exhibit only those values whose datetimes are in both dataseries.

    :param ds1: A DataSeries instance.
    :type ds1: :class:`DataSeries`.
    :param ds2: A DataSeries instance.
    :type ds2: :class:`DataSeries`.
    :param maxLen: The maximum number of values to hold for the returned :class:`DataSeries`.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """
    aligned1 = dataseries.SequenceDataSeries(maxLen)
    aligned2 = dataseries.SequenceDataSeries(maxLen)
    Syncer(ds1, ds2, aligned1, aligned2)
    return (aligned1, aligned2)


class Syncer(object):

    def __init__(self, sourceDS1, sourceDS2, destDS1, destDS2):
        self._Syncer__values1 = []
        self._Syncer__values2 = []
        self._Syncer__destDS1 = destDS1
        self._Syncer__destDS2 = destDS2
        sourceDS1.getNewValueEvent().subscribe(self._Syncer__onNewValue1)
        sourceDS2.getNewValueEvent().subscribe(self._Syncer__onNewValue2)

    def __findPosForDateTime(self, values, dateTime):
        ret = None
        i = len(values) - 1
        while i >= 0:
            if values[i][0] == dateTime:
                ret = i
                break
            else:
                if values[i][0] < dateTime:
                    break
            i -= 1

        return ret

    def __onNewValue1(self, dataSeries, dateTime, value):
        pos2 = self._Syncer__findPosForDateTime(self._Syncer__values2, dateTime)
        if pos2 is not None:
            self._Syncer__append(dateTime, value, self._Syncer__values2[pos2][1])
            self._Syncer__values1 = []
            self._Syncer__values2 = self._Syncer__values2[pos2 + 1:]
        else:
            self._Syncer__values1.append((dateTime, value))

    def __onNewValue2(self, dataSeries, dateTime, value):
        pos1 = self._Syncer__findPosForDateTime(self._Syncer__values1, dateTime)
        if pos1 is not None:
            self._Syncer__append(dateTime, self._Syncer__values1[pos1][1], value)
            self._Syncer__values1 = self._Syncer__values1[pos1 + 1:]
            self._Syncer__values2 = []
        else:
            self._Syncer__values2.append((dateTime, value))

    def __append(self, dateTime, value1, value2):
        self._Syncer__destDS1.appendWithDateTime(dateTime, value1)
        self._Syncer__destDS2.appendWithDateTime(dateTime, value2)