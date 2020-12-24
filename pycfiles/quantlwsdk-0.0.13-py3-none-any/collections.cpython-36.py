# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\utils\collections.py
# Compiled at: 2019-06-05 03:26:22
# Size of source mod 2**32: 3921 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import numpy as np

def lt(v1, v2):
    if v1 is None:
        return True
    else:
        if v2 is None:
            return False
        return v1 < v2


def intersect(values1, values2, skipNone=False):
    ix1 = []
    ix2 = []
    values = []
    i1 = 0
    i2 = 0
    while i1 < len(values1) and i2 < len(values2):
        v1 = values1[i1]
        v2 = values2[i2]
        if v1 == v2:
            if v1 is not None or skipNone is False:
                ix1.append(i1)
                ix2.append(i2)
                values.append(v1)
                i1 += 1
                i2 += 1
        if lt(v1, v2):
            i1 += 1
        else:
            i2 += 1

    return (
     values, ix1, ix2)


class NumPyDeque(object):

    def __init__(self, maxLen, dtype=float):
        assert maxLen > 0, 'Invalid maximum length'
        self._NumPyDeque__values = np.empty(maxLen, dtype=dtype)
        self._NumPyDeque__maxLen = maxLen
        self._NumPyDeque__nextPos = 0

    def getMaxLen(self):
        return self._NumPyDeque__maxLen

    def append(self, value):
        if self._NumPyDeque__nextPos < self._NumPyDeque__maxLen:
            self._NumPyDeque__values[self._NumPyDeque__nextPos] = value
            self._NumPyDeque__nextPos += 1
        else:
            self._NumPyDeque__values[0:-1] = self._NumPyDeque__values[1:]
            self._NumPyDeque__values[self._NumPyDeque__nextPos - 1] = value

    def data(self):
        if self._NumPyDeque__nextPos < self._NumPyDeque__maxLen:
            ret = self._NumPyDeque__values[0:self._NumPyDeque__nextPos]
        else:
            ret = self._NumPyDeque__values
        return ret

    def resize(self, maxLen):
        assert maxLen > 0, 'Invalid maximum length'
        values = np.empty(maxLen, dtype=(self._NumPyDeque__values.dtype))
        lastValues = self._NumPyDeque__values[0:self._NumPyDeque__nextPos]
        values[0:min(maxLen, len(lastValues))] = lastValues[-1 * min(maxLen, len(lastValues)):]
        self._NumPyDeque__values = values
        self._NumPyDeque__maxLen = maxLen
        if self._NumPyDeque__nextPos >= self._NumPyDeque__maxLen:
            self._NumPyDeque__nextPos = self._NumPyDeque__maxLen

    def __len__(self):
        return self._NumPyDeque__nextPos

    def __getitem__(self, key):
        return self.data()[key]


class ListDeque(object):

    def __init__(self, maxLen):
        assert maxLen > 0, 'Invalid maximum length'
        self._ListDeque__values = []
        self._ListDeque__maxLen = maxLen

    def getMaxLen(self):
        return self._ListDeque__maxLen

    def append(self, value):
        self._ListDeque__values.append(value)
        if len(self._ListDeque__values) > self._ListDeque__maxLen:
            self._ListDeque__values.pop(0)

    def data(self):
        return self._ListDeque__values

    def resize(self, maxLen):
        assert maxLen > 0, 'Invalid maximum length'
        self._ListDeque__maxLen = maxLen
        self._ListDeque__values = self._ListDeque__values[-1 * maxLen:]

    def __len__(self):
        return len(self._ListDeque__values)

    def __getitem__(self, key):
        return self._ListDeque__values[key]