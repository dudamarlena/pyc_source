# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/dataseries/aligned.py
# Compiled at: 2016-11-29 01:45:48
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
        self.__values1 = []
        self.__values2 = []
        self.__destDS1 = destDS1
        self.__destDS2 = destDS2
        sourceDS1.getNewValueEvent().subscribe(self.__onNewValue1)
        sourceDS2.getNewValueEvent().subscribe(self.__onNewValue2)

    def __findPosForDateTime(self, values, dateTime):
        ret = None
        i = len(values) - 1
        while i >= 0:
            if values[i][0] == dateTime:
                ret = i
                break
            elif values[i][0] < dateTime:
                break
            i -= 1

        return ret

    def __onNewValue1(self, dataSeries, dateTime, value):
        pos2 = self.__findPosForDateTime(self.__values2, dateTime)
        if pos2 is not None:
            self.__append(dateTime, value, self.__values2[pos2][1])
            self.__values1 = []
            self.__values2 = self.__values2[pos2 + 1:]
        else:
            self.__values1.append((dateTime, value))
        return

    def __onNewValue2(self, dataSeries, dateTime, value):
        pos1 = self.__findPosForDateTime(self.__values1, dateTime)
        if pos1 is not None:
            self.__append(dateTime, self.__values1[pos1][1], value)
            self.__values1 = self.__values1[pos1 + 1:]
            self.__values2 = []
        else:
            self.__values2.append((dateTime, value))
        return

    def __append(self, dateTime, value1, value2):
        self.__destDS1.appendWithDateTime(dateTime, value1)
        self.__destDS2.appendWithDateTime(dateTime, value2)