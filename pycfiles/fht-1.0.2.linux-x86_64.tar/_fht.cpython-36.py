# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/fht/_fht.py
# Compiled at: 2017-06-20 09:40:47
# Size of source mod 2**32: 5481 bytes
"""Implements the fast Hadamard transform"""
__all__ = ['fht', 'fht1', 'fht2', 'fht3', 'is_power_of_two']
import numpy as np
from . import _C_fht_int, _C_fht_long, _C_fht_float, _C_fht_double

def fht(arr, **kargs):
    """Fast Hadamard transform
    
    Notes
    -----
    Calls fht1, fht2 or fht3 function according to the dimension of arr
    
    See also
    --------
    fht1, fht2, fht3: specialized function depending of the dimension of arr

    Exemple
    -------
    >>> fht(np.asarray([2, 0, 0, 0]))
    array([ 1.,  1.,  1.,  1.])
    """
    if arr.ndim == 1:
        return fht1(arr)
    else:
        if arr.ndim == 2:
            return fht2(arr, **kargs)
        if arr.ndim == 3:
            return fht3(arr, **kargs)
    raise NotImplemented('fht not implemented for dimension > 3')


def fht1(arr, dtype=None):
    """1-dimensional fast hadamard transform
    Input
    -----
    arr: 1-dimensional array
    
    Output
    ------
    oarr : 1-dimensional array of the size of arr

    Notes
    -----
    It is normalized so applying twice is equivalent to identity
    """
    if arr.ndim != 1:
        raise ValueError('Expected 1-dimensional array')
    elif not is_power_of_two(arr.shape[0]):
        raise ValueError('array shape must be a power of two')
    elif dtype is None:
        dtype = arr.dtype
    else:
        oarr = np.empty((arr.shape), dtype=dtype)
        if dtype == np.float32:
            _C_fht1 = _C_fht_float.fht1_float
            if arr.dtype is not np.float32:
                iarr = arr.astype(np.float32)
        else:
            if dtype == np.float64:
                _C_fht1 = _C_fht_double.fht1_double
                if arr.dtype is not np.float64:
                    iarr = arr.astype(np.float64)
            else:
                if dtype == np.int32:
                    _C_fht1 = _C_fht_int.fht1_int
                    if arr.dtype is not np.int32:
                        iarr = arr.astype(np.int32)
                else:
                    if dtype == np.int64:
                        _C_fht1 = _C_fht_long.fht1_long
                        if arr.dtype is not np.int64:
                            iarr = arr.astype(np.int64)
                    else:
                        raise ValueError('data type not supported')
    _C_fht1(iarr, oarr)
    return (oarr / np.sqrt(arr.size)).astype(dtype)


def fht2(arr, axes=(0, 1), dtype=None):
    """2-dimensional fast hadamard transform

    Input
    -----
    arr: 2-dimensional array
    axes : (int or tuplue) axes along which is applied the 1d transform
    
    Output
    ------
    oarr : 2-dimensional array of the size of arr

    Notes
    -----
    It is normalized so applying twice is equivalent to identity
    """
    if axes == (0, 1) or axes == (1, 0):
        return fht1(arr.flatten()).reshape(arr.shape)
    else:
        if not (axes == 0 or axes == 1):
            raise ValueError('axes is either (0, 1) or 0 or 1')
        else:
            if arr.ndim != 2:
                raise ValueError('Expected 2-dimensional array')
            if not is_power_of_two(arr.shape[axes]):
                raise ValueError('array shape along axes must be a power of two')
            iarr = arr.swapaxes(1, axes)
            if dtype is None:
                dtype = iarr.dtype
        oarr = np.empty((iarr.shape), dtype=dtype)
        if dtype == np.float32:
            _C_fht2 = _C_fht_float.fht2_float
            if arr.dtype is not np.float32:
                iarr = arr.astype(np.float32)
        elif dtype == np.float64:
            _C_fht2 = _C_fht_double.fht2_double
            if arr.dtype is not np.float64:
                iarr = arr.astype(np.float64)
        else:
            if dtype == np.int32:
                _C_fht2 = _C_fht_int.fht2_int
                if arr.dtype is not np.int32:
                    iarr = arr.astype(np.int32)
            else:
                if dtype == np.int64:
                    _C_fht2 = _C_fht_long.fht2_long
                    if arr.dtype is not np.int64:
                        iarr = arr.astype(np.int64)
                else:
                    raise ValueError('data type not supported')
            _C_fht2(iarr, oarr)
        return (oarr / np.sqrt(arr.shape[axes])).swapaxes(1, axes).astype(dtype)


def fht3(arr, axes=(0, 1, 2), dtype=None):
    """3-dimensional fast hadamard transform

    Input
    -----
    arr: 3-dimensional array
    axes : (int or tuple) axes along which is applied the 1d transform
    
    Output
    ------
    oarr : 3-dimensional array of the size of arr

    Notes
    -----
    It is normalized so applying twice is equivalent to identity
    """
    if np.all(np.sort(axes) == (0, 1, 2)):
        return fht1(arr.flatten()).reshape(arr.shape)
    else:
        if np.all(np.sort(axes) == (0, 1)):
            shape = (
             np.prod(arr.shape[0:2]), arr.shape[2])
            axes = 0
        else:
            if np.all(np.sort(axes) == (1, 2)):
                shape = (
                 arr.shape[0], np.prod(arr.shape[1:]))
                axes = 1
            else:
                if np.all(np.sort(axes) == (0, 2)):
                    iarr = arr.swapaxes(1, 2)
                    oarr = fht3(iarr, axes=(0, 1))
                    return oarr.swapaxes(1, 2)
                if axes == 0:
                    shape = (
                     arr.shape[0], np.prod(arr.shape[1:]))
                    axes = 0
                else:
                    if axes == 2:
                        shape = (
                         np.prod(arr.shape[0:2]), arr.shape[2])
                        axes = 1
                    else:
                        if axes == 1:
                            iarr = arr.swapaxes(1, 2)
                            oarr = fht3(iarr, axes=2)
                            return oarr.swapaxes(1, 2)
        return fht2((arr.reshape(shape)), axes=axes, dtype=dtype).reshape(arr.shape)


def is_power_of_two(input_integer):
    """Test if an integer is a power of two"""
    if input_integer == 1:
        return False
    else:
        return input_integer != 0 and input_integer & input_integer - 1 == 0