# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/compyte/array.py
# Compiled at: 2014-05-26 22:50:33
from __future__ import division
__copyright__ = 'Copyright (C) 2011 Andreas Kloeckner'
__license__ = '\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n'
import numpy as np

def f_contiguous_strides(itemsize, shape):
    if shape:
        strides = [
         itemsize]
        for s in shape[:-1]:
            strides.append(strides[(-1)] * s)

        return tuple(strides)
    else:
        return ()


def c_contiguous_strides(itemsize, shape):
    if shape:
        strides = [
         itemsize]
        for s in shape[:0:-1]:
            strides.append(strides[(-1)] * s)

        return tuple(strides[::-1])
    else:
        return ()


class ArrayFlags:

    def __init__(self, ary):
        self.f_contiguous = ary.strides == f_contiguous_strides(ary.dtype.itemsize, ary.shape)
        self.c_contiguous = ary.strides == c_contiguous_strides(ary.dtype.itemsize, ary.shape)
        self.forc = self.f_contiguous or self.c_contiguous


def get_common_dtype(obj1, obj2, allow_double):
    zero1 = np.zeros(1, dtype=obj1.dtype)
    try:
        zero2 = np.zeros(1, dtype=obj2.dtype)
    except AttributeError:
        zero2 = obj2

    result = (zero1 + zero2).dtype
    if not allow_double:
        if result == np.float64:
            result = np.dtype(np.float32)
        elif result == np.complex128:
            result = np.dtype(np.complex64)
    return result


def bound(a):
    high = a.bytes
    low = a.bytes
    for stri, shp in zip(a.strides, a.shape):
        if stri < 0:
            low += stri * (shp - 1)
        else:
            high += stri * (shp - 1)

    return (
     low, high)


def may_share_memory(a, b):
    if a is b:
        return True
    else:
        if a.__class__ is b.__class__:
            a_l, a_h = bound(a)
            b_l, b_h = bound(b)
            if b_l >= a_h or a_l >= b_h:
                return False
            return True
        return False


try:
    from numpy.lib.stride_tricks import as_strided as _as_strided
    _test_dtype = np.dtype([
     (
      'a', np.float64), ('b', np.float64)], align=True)
    _test_result = _as_strided(np.zeros(10, dtype=_test_dtype))
    if _test_result.dtype != _test_dtype:
        raise RuntimeError("numpy's as_strided is broken")
    as_strided = _as_strided
except:

    class _DummyArray(object):
        """ Dummy object that just exists to hang __array_interface__ dictionaries
        and possibly keep alive a reference to a base array.
        """

        def __init__(self, interface, base=None):
            self.__array_interface__ = interface
            self.base = base


    def as_strided(x, shape=None, strides=None):
        """ Make an ndarray from the given array with the given shape and strides.
        """
        if (shape is None or x.shape == shape) and (strides is None or x.strides == strides):
            return x
        if x.dtype.isbuiltin or shape is None:
            shape = x.shape
        strides = tuple(strides)
        from pytools import product
        if strides is not None and shape is not None and product(shape) == product(x.shape) and x.flags.forc:
            if strides == f_contiguous_strides(x.dtype.itemsize, shape):
                result = x.reshape(-1).reshape(*shape, **dict(order='F'))
                assert result.strides == strides
                return result
            if strides == c_contiguous_strides(x.dtype.itemsize, shape):
                result = x.reshape(-1).reshape(*shape, **dict(order='C'))
                if not result.strides == strides:
                    raise AssertionError
                    return result
            raise NotImplementedError("as_strided won't work on non-builtin arrays for now. See https://github.com/numpy/numpy/issues/2466")
        interface = dict(x.__array_interface__)
        if shape is not None:
            interface['shape'] = tuple(shape)
        if strides is not None:
            interface['strides'] = tuple(strides)
        return np.asarray(_DummyArray(interface, base=x))