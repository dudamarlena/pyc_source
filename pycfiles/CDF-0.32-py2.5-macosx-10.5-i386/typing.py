# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/cdf/typing.py
# Compiled at: 2010-11-11 15:27:36
import copy, datetime, numpy
from . import internal

class epoch(datetime.datetime):

    def __new__(cls, value=None):
        if isinstance(value, datetime.datetime):
            year = value.year
            month = value.month
            day = value.day
            hour = value.hour
            minute = value.minute
            second = value.second
            microsecond = value.microsecond
        else:
            (year, month, day, hour, minute, second, millisecond) = internal.EPOCHbreakdown(value)
            microsecond = millisecond * 1000
        return super(epoch, cls).__new__(cls, year, month, day, hour, minute, second, microsecond)

    def __deepcopy__(self, memo):
        dup = type(self)(self)
        return dup

    def to_float64(self):
        ret = internal.computeEPOCH(self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond / 1000)[0]
        return ret

    def __str__(self):
        return "'" + self.isoformat() + "'"

    def __repr__(self):
        return str(self)


class epoch16(epoch):
    pass


_typeConversions = {numpy.byte: internal.CDF_BYTE, 
   numpy.int8: internal.CDF_INT1, 
   numpy.int16: internal.CDF_INT2, 
   numpy.int32: internal.CDF_INT4, 
   numpy.int64: internal.CDF_REAL8, 
   numpy.uint8: internal.CDF_UINT1, 
   numpy.uint16: internal.CDF_UINT2, 
   numpy.uint32: internal.CDF_UINT4, 
   numpy.float32: internal.CDF_REAL4, 
   numpy.float64: internal.CDF_REAL8, 
   epoch: internal.CDF_EPOCH, 
   epoch16: internal.CDF_EPOCH16, 
   numpy.object_: internal.CDF_EPOCH, 
   numpy.string_: internal.CDF_CHAR, 
   numpy.unicode_: internal.CDF_CHAR, 
   internal.CDF_BYTE: numpy.byte, 
   internal.CDF_INT1: numpy.int8, 
   internal.CDF_INT2: numpy.int16, 
   internal.CDF_INT4: numpy.int32, 
   internal.CDF_UINT1: numpy.uint8, 
   internal.CDF_UINT2: numpy.uint16, 
   internal.CDF_UINT4: numpy.uint32, 
   internal.CDF_REAL4: numpy.float32, 
   internal.CDF_REAL8: numpy.float64, 
   internal.CDF_FLOAT: numpy.float32, 
   internal.CDF_DOUBLE: numpy.float64, 
   internal.CDF_EPOCH: epoch, 
   internal.CDF_EPOCH16: epoch16, 
   internal.CDF_CHAR: numpy.string_, 
   internal.CDF_UCHAR: numpy.string_}
_numpyTypeContains = {numpy.byte: [], numpy.int8: [
              numpy.byte], 
   numpy.int16: [
               numpy.int8, numpy.uint8], 
   numpy.int32: [
               numpy.int16, numpy.uint16], 
   numpy.int64: [
               numpy.int32, numpy.uint32], 
   numpy.uint8: [
               numpy.byte], 
   numpy.uint16: [
                numpy.uint8], 
   numpy.uint32: [
                numpy.uint16], 
   numpy.float32: [
                 numpy.int64], 
   numpy.float64: [
                 numpy.float32], 
   numpy.string_: [
                 numpy.string_, numpy.unicode_]}

def _typeContainsOther(one, two, memo=None):
    if one == two:
        return True
    else:
        if memo is None:
            memo = {}
            memo[one] = False
        for type in _numpyTypeContains[one]:
            if type not in memo:
                memo[type] = None
                memo[type] = _typeContainsOther(type, two, memo)
            if memo[type]:
                return True

        return False
    return


def joinNumpyType(*args):
    ret = None
    for dtype in args:
        if not isinstance(dtype, numpy.dtype):
            dtype = numpy.dtype(dtype)
        if ret is None:
            ret = dtype
        elif _typeContainsOther(dtype.type, ret.type) and dtype.itemsize >= ret.itemsize:
            ret = dtype
        elif not _typeContainsOther(ret.type, dtype.type) or dtype.itemsize > ret.itemsize:
            candidates = []
            for type in _numpyTypeContains:
                if _typeContainsOther(type, ret.type) and _typeContainsOther(type, dtype.type):
                    candidates.append(type)

            if len(candidates) > 0:
                ret = numpy.dtype(candidates[0])
            else:
                ret = None
            break

    return ret


def joinCdfType(*args):
    return _typeConversions[joinNumpyType(*[ _typeConversions[type] for type in args ]).type]


class uniformCdfTyped:
    pass