# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\shape_helpers.py
# Compiled at: 2015-05-08 08:32:01
import numpy as np

def is_dims_array(a):
    """Determines if argument is a Numpy ndarray of integers"""
    if not isinstance(a, np.ndarray):
        return False
    if a.ndim != 1:
        return False
    if a.size > 32:
        return False
    if not np.issubdtype(a.dtype, np.int):
        return False
    if a.size == 0:
        return True
    return True


def is_non_zero_dims_array(a):
    """Determines if argument is a Numpy ndarray of non-zero integers"""
    if not is_dims_array(a):
        return False
    if np.count_non_zero(a) == len(a):
        return True
    return False


def is_non_negative_dims_array(a):
    """Determines if argument is a Numpy ndarray of non-negative integers"""
    if not is_dims_array(a):
        return False
    if np.amin(a) >= 0:
        return True
    return False


def is_positive_dims_array(a):
    """Determines if argument is a Numpy ndarray of positive integers"""
    if not is_dims_array(a):
        return False
    if np.amin(a) > 0:
        return True
    return False


def is_valid_hyperslab_spec(shape, first, last, step):
    """
    Determines if (first, last, step) describe a valid hyperslab selection
    on shape.

    CAUTION: we assume that shape is 0-based and that the hyperslab is 1-based
    """
    if not is_positive_dims_array(shape):
        return False
    else:
        rk = len(shape)
        if first is not None:
            if not is_positive_dims_array(first):
                return False
            if len(first) != rk:
                return False
        if last is not None:
            if not is_positive_dims_array(last):
                return False
            if len(last) != rk:
                return False
        if step is not None:
            if not is_positive_dims_array(step):
                return False
            if len(step) != rk:
                return False
        if first is not None and last is not None:
            if not np.greater_equal(last, first).all():
                return False
        if step is not None and last is not None:
            if np.greater_equal(step, last).all():
                return False
        return True


def get_dimensions(size):
    """
    'size' is a list of lists and we have to construct
    dims and maxdims lists from it
    """
    if not isinstance(size, list):
        raise TypeError('List expected.')
    dims = []
    maxdims = []
    if len(size) == 1:
        if not isinstance(size[0], list):
            raise TypeError('List expected.')
        num_col = len(size[0])
        if num_col == 0 or num_col > 32:
            return
        for j in range(len(size[0])):
            if not isinstance(size[0][j], int):
                raise TypeError('Integer expected.')
            if size[0][j] > 0:
                dims.append(size[0][j])
                maxdims.append(size[0][j])
            elif size[0][j] < 0:
                dims.append(-size[0][j])
                maxdims.append(None)
            else:
                return

    else:
        num_row = len(size)
        if num_row > 32:
            return
        for i in range(len(size)):
            if not isinstance(size[i], list):
                raise TypeError('List expected.')
            if len(size[i]) != 1:
                return
            if not isinstance(size[i][0], int):
                raise TypeError('Integer expected.')
            if len(size[i]) != 1:
                return
            if size[i][0] > 0:
                dims.append(size[i][0])
                maxdims.append(size[i][0])
            elif size[i][0] < 0:
                dims.append(-size[i][0])
                maxdims.append(None)
            else:
                return

    return (
     dims, maxdims)


def get_chunk_dimensions(chunk):
    """
    We expect a string of the form '[d1 d2 d3 ... dN]'
    """
    if not isinstance(chunk, str):
        raise TypeError('String expected.')
    s = chunk.strip()
    if s[0] != '[' or s[(-1)] != ']':
        return
    s = s[1:-1]
    s1 = s.split()
    chunk = []
    for i in range(len(s1)):
        if s1[i].strip() != '':
            try:
                d = int(s1[i].strip())
                if d > 0:
                    chunk.append(d)
                else:
                    return
            except:
                continue

    return tuple(chunk)


def lol_2_ndarray(lol):
    """
    Converts a list of lists into a Numpy ndarray.

    Returns a tuple with the Numpy ndarray and an error message.
    """
    a = None
    ret = '\x00'
    try:
        nd = np.asarray(lol, dtype=np.int32)
        a = np.reshape(nd, (nd.size,))
    except:
        ret = 'Not an integer array.'

    return (a, ret)


def try_intarray(x):
    """
    Converts a float or list or list of lists into an ndarray of int32.

    Returns a tuple with the ndarray and an error message.
    """
    if x is None or not isinstance(x, (float, list)):
        raise TypeError('Invalid argument type. Expected float or list.')
    a = None
    ret = '\x00'
    try:
        a = np.asarray(x, dtype=np.int32).flatten()
    except:
        ret = 'Unable to convert the argment to an integer array.'

    return (a, ret)


def normalize_first(first, shape):
    """
    FIRST must be a non-negative array of the same length as SHAPE.

    Switch from 1-based to 0-based indexing as part of the normalization
    """
    if not isinstance(shape, tuple) and len(shape) > 0 and len(shape) < 32:
        raise TypeError("Invalid 'shape' found.")
    if first is None:
        return tuple([ 0 for i in shape ])
    if not isinstance(first, (float, list)):
        raise TypeError("'first' must be an integer or integer array.")
    else:
        npfirst, ret = try_intarray(first)
        if npfirst is None:
            raise TypeError("'first' must be an integer or integer array.")
        elif len(npfirst) != len(shape):
            raise TypeError("Invalid 'first' position.")
        else:
            if np.greater_equal(npfirst, 1).all():
                return tuple([ i - 1 for i in npfirst ])
            raise TypeError("'first' must be a non-negative array.")
    return


def normalize_last(last, shape):
    """
    LAST must be a positive array of the same length as SHAPE.
    """
    if not isinstance(shape, tuple) and len(shape) > 0 and len(shape) < 32:
        raise TypeError("Invalid 'shape' found.")
    if last is None:
        return tuple([ shape[i] for i in range(len(shape)) ])
    if not isinstance(last, (float, list)):
        raise TypeError("'last' must be an integer or integer array.")
    else:
        nplast, ret = try_intarray(last)
        if nplast is None:
            raise TypeError("'last' must be an integer or integer array.")
        elif len(nplast) != len(shape):
            raise TypeError("Invalid 'last' position.")
        else:
            if np.greater_equal(nplast, 1).all():
                return tuple([ i for i in nplast ])
            raise TypeError("'last' must be a positive array.")
    return


def normalize_step(step, shape):
    if not isinstance(shape, tuple) and len(shape) > 0 and len(shape) < 32:
        raise TypeError("Invalid 'shape' found.")
    if step is None:
        return tuple([ 1 for i in shape ])
    if not isinstance(step, (float, list)):
        raise TypeError("'step' must be an integer or integer array.")
    else:
        npstep, ret = try_intarray(step)
        if npstep is None:
            raise TypeError("'step' must be an integer or integer array.")
        elif len(npstep) != len(shape):
            raise TypeError("Invalid 'step' found.")
        else:
            if np.greater_equal(npstep, 1).all():
                return tuple([ i for i in npstep ])
            raise TypeError("'step' must be a positive array.")
    return


def can_reshape(shape, maxshape):
    """
    Determines if SHAPE is "less or equal" to MAXSHAPE

    Caution: a None entry in maxshape means unlimited.
    """
    if not isinstance(shape, tuple) or not isinstance(maxshape, tuple):
        return False
    if len(shape) != len(maxshape):
        return False
    else:
        if None in shape:
            return False
        ret = True
        for i in range(len(shape)):
            if maxshape[i] is None or shape[i] <= maxshape[i]:
                continue
            else:
                break

        return ret


def tuple_to_excel(shape):
    """
    Convert a tuple into Excel array notation
    """
    if not isinstance(shape, tuple):
        raise TypeError("Invalid 'shape' found.")
    if len(shape) > 0:
        ret = '{ '
        size = len(shape)
        for i in range(size):
            ret += str(shape[i])
            if i < size - 1:
                ret += ', '

        ret += ' }'
        return ret
    else:
        return '{}'