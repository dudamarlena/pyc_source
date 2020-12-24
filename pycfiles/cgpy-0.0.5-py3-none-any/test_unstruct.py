# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_unstruct.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = 'Tests for :mod:`cgp.utils.unstruct`.'
import numpy as np
from cgp.utils.unstruct import unstruct

def test_dimensions():
    """Check relationship between dimensions of x and unstruct(x)."""
    x = np.arange(24).view(dtype=[ (i, int) for i in 'ab' ]).reshape(3, 4)
    u = unstruct(x)
    u[:] += 10
    np.testing.assert_equal(x['a'], u[(Ellipsis, 0)])
    np.testing.assert_equal(x[0][0].item(), u[0][0])


def test_dtypes():
    """Verify that unstruct() handles different dtypes correctly."""
    for fieldtype in (np.int8, np.int32, float):
        dtype = [ (i, fieldtype) for i in 'ab' ]
        x = np.arange(4, dtype=fieldtype).view(dtype)
        yield (np.testing.assert_equal, unstruct(x), [[0, 1], [2, 3]])


def test_zero_rank():
    """
    Handle intricacies of zero-rank arrays.
    
    `Zero-rank arrays 
    <http://projects.scipy.org/numpy/wiki/ZeroRankArray>`_ 
    are tricky; they can be structured, yet be of type numpy.void.

    Here, x0 and x1 are almost, but not completely, the same:
    
    >>> fieldtype = np.int32   # ensure same result on 32- and 64-bit platforms
    >>> dtype = [("a", fieldtype), ("b", fieldtype)]
    >>> x0 = np.array([(0, 1)], dtype=dtype)[0]
    >>> x1 = np.array((0, 1), dtype=dtype)

    Despite a lot of equalities below, x0 and x1 are of different type.
    
    >>> (x0 == x1) and (x0.shape == x1.shape) and (x0.dtype == x1.dtype)
    True
    >>> x0
    (0, 1)
    >>> x1
    array((0, 1), dtype=[('a', '<i4'), ('b', '<i4')])
    >>> type(x0), type(x1)
    (<type 'numpy.void'>, <type 'numpy.ndarray'>)
    
    Unstructuring them was tricky, but finally works.
    
    >>> unstruct(x0)
    array([0, 1]...)
    >>> unstruct(x1)
    array([0, 1]...)
    """
    fieldtype = np.int32
    dtype = [('a', fieldtype), ('b', fieldtype)]
    x0 = np.array([(0, 1)], dtype=dtype)[0]
    x1 = np.array((0, 1), dtype=dtype)
    np.testing.assert_equal(unstruct(x0), unstruct(x1))