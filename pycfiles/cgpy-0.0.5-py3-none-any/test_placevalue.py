# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_placevalue.py
# Compiled at: 2011-11-03 22:08:21
__doc__ = 'Tests for :mod:`cgp.utils.placevalue`.'
from numpy.testing import assert_equal, assert_raises
from ..utils.placevalue import Placevalue
p = Placevalue([4, 3, 2])

def test_init_properties():
    """Verify properties of Placevalue object."""
    assert_equal(p.n, [4, 3, 2])
    assert_equal(p.maxint, 24)
    assert_equal(p.posval, [6, 2, 1])
    assert_equal(Placevalue([4, 3, 2], msd_first=False).posval, [1, 4, 12])


def test_vec2int_digitrange():
    """Check range of digits."""
    assert_raises(OverflowError, p.vec2int, [0, 0, 2])


def test_int2vec_2d():
    """
    Check that int2vec(sequence) is 2-d even when there is only one position.
    
    Verify bugfix: If i is a sequence, the output should be a 2-d array 
    so that "for v in pv.int2vec(i)" works. Previously, this failed when 
    there was only one position.
    """
    a = Placevalue([3])
    assert_equal(a.int2vec(range(4)), [[0], [1], [2], [3]])


def test_vec2int_huge():
    """
    Verify that vec2int works even if maxint is huge.
    
    Placevalue.posval needs dtype=object so it will use Python's long integers.
    These work automagically with ufuncs like .sum(), and will not overflow 
    like e.g. np.int64.
    """
    for bits in (63, 64, 65):
        a = Placevalue([[2] * bits])
        v = [0] + [1] * (bits - 1)
        i = a.vec2int(v)
        yield (assert_equal, i, 2 ** (bits - 1) - 1)
        yield (assert_equal, a.int2vec(i), v)