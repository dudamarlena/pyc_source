# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/utils/collections.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import numpy as np

def lt(v1, v2):
    if v1 is None:
        return True
    else:
        if v2 is None:
            return False
        else:
            return v1 < v2

        return


def intersect(values1, values2, skipNone=False):
    ix1 = []
    ix2 = []
    values = []
    i1 = 0
    i2 = 0
    while i1 < len(values1) and i2 < len(values2):
        v1 = values1[i1]
        v2 = values2[i2]
        if v1 == v2 and (v1 is not None or skipNone is False):
            ix1.append(i1)
            ix2.append(i2)
            values.append(v1)
            i1 += 1
            i2 += 1
        elif lt(v1, v2):
            i1 += 1
        else:
            i2 += 1

    return (values, ix1, ix2)


class NumPyDeque(object):

    def __init__(self, maxLen, dtype=float):
        assert maxLen > 0, 'Invalid maximum length'
        self.__values = np.empty(maxLen, dtype=dtype)
        self.__maxLen = maxLen
        self.__nextPos = 0

    def getMaxLen(self):
        return self.__maxLen

    def append(self, value):
        if self.__nextPos < self.__maxLen:
            self.__values[self.__nextPos] = value
            self.__nextPos += 1
        else:
            self.__values[0:(-1)] = self.__values[1:]
            self.__values[self.__nextPos - 1] = value

    def data(self):
        if self.__nextPos < self.__maxLen:
            ret = self.__values[0:self.__nextPos]
        else:
            ret = self.__values
        return ret

    def resize(self, maxLen):
        assert maxLen > 0, 'Invalid maximum length'
        values = np.empty(maxLen, dtype=self.__values.dtype)
        lastValues = self.__values[0:self.__nextPos]
        values[0:(min(maxLen, len(lastValues)))] = lastValues[-1 * min(maxLen, len(lastValues)):]
        self.__values = values
        self.__maxLen = maxLen
        if self.__nextPos >= self.__maxLen:
            self.__nextPos = self.__maxLen

    def __len__(self):
        return self.__nextPos

    def __getitem__(self, key):
        return self.data()[key]


class ListDeque(object):

    def __init__(self, maxLen):
        assert maxLen > 0, 'Invalid maximum length'
        self.__values = []
        self.__maxLen = maxLen

    def getMaxLen(self):
        return self.__maxLen

    def append(self, value):
        self.__values.append(value)
        if len(self.__values) > self.__maxLen:
            self.__values.pop(0)

    def data(self):
        return self.__values

    def resize(self, maxLen):
        assert maxLen > 0, 'Invalid maximum length'
        self.__maxLen = maxLen
        self.__values = self.__values[-1 * maxLen:]

    def __len__(self):
        return len(self.__values)

    def __getitem__(self, key):
        return self.__values[key]