# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/cdf/entry.py
# Compiled at: 2010-11-11 15:27:36
import interface as cdf, internal, typing

class entry:

    def __init__(self, value, simple=False):
        self._data = None
        self._cdfType = None
        self._numElements = None
        if self._type(value, simple):
            self._data = value
        return

    def _type(self, value, simple=True):
        if isinstance(value, str) or isinstance(value, unicode):
            self._cdfType = internal.CDF_CHAR
            self._numElements = len(value)
        elif isinstance(value, int) or isinstance(value, long):
            self._cdfType = internal.CDF_INT4
            self._numElements = 1
        elif isinstance(value, float):
            self._cdfType = internal.CDF_REAL8
            self._numElements = 1
        elif isinstance(value, tuple):
            oldType = None
            for item in value:
                newType = self._type(item)
                if newType[1] != 1:
                    raise cdf.CoherenceError
                newType = newType[0]
                if oldType is None:
                    oldType = newType
                elif oldType != newType:
                    joinedType = typing.joinCdfType(oldType, newType)
                    if joinedType is not None:
                        oldType = joinedType
                    else:
                        raise cdf.CoherenceError

            if oldType is not None:
                self._cdfType = oldType
                self._numElements = len(value)
            else:
                raise ValueError
        elif isinstance(value, list) and not simple:
            types = []
            nums = []
            for item in value:
                try:
                    (t, n) = self._type(item)
                    types.append(t)
                    nums.append(n)
                except TypeError:
                    raise cdf.CoherenceError

            self._cdfType = types
            self._numElements = nums
        else:
            print 'Unknown type for data'
            print value
            print value.__class__
            print type(value)
            self._cdfType = None
            self._numElements = None
            raise ValueError
        return (self._cdfType, self._numElements)

    def _write(self, num1, token1, num2, token2, type, num3, value):
        internal.CDFlib(internal.SELECT_, internal.ATTR_, num1, token1, num2, internal.PUT_, token2, type, num3, value)

    def write(self, token1, token2, attrNum, entryNum=None):
        if entryNum is None:
            data = self._data
            types = self._cdfType
            nums = self._numElements
            if not isinstance(data, list):
                data = [
                 self._data]
                types = [self._cdfType]
                nums = [self._numElements]
            for i in xrange(0, len(data)):
                self._write(attrNum, token1, i, token2, types[i], nums[i], data[i])

        else:
            self._write(attrNum, token1, entryNum, token2, self._cdfType, self._numElements, self._data)
        return