# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/optimize/tests/test_scalar_max.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 1447 bytes
"""
Tests for scalar maximization.

"""
import numpy as np
from numpy.testing import assert_almost_equal
from nose.tools import raises
from numba import njit
from quantecon.optimize import brent_max

@njit
def f(x):
    """
    A function for testing on.
    """
    return -(x + 2.0) ** 2 + 1.0


def test_f():
    """
    Uses the function f defined above to test the scalar maximization
    routine.
    """
    true_fval = 1.0
    true_xf = -2.0
    xf, fval, info = brent_max(f, -2, 2)
    assert_almost_equal(true_fval, fval, decimal=4)
    assert_almost_equal(true_xf, xf, decimal=4)


@njit
def g(x, y):
    """
    A multivariate function for testing on.
    """
    return -x ** 2 + y


def test_g():
    """
    Uses the function g defined above to test the scalar maximization
    routine.
    """
    y = 5
    true_fval = 5.0
    true_xf = -0.0
    xf, fval, info = brent_max(g, (-10), 10, args=(y,))
    assert_almost_equal(true_fval, fval, decimal=4)
    assert_almost_equal(true_xf, xf, decimal=4)


@raises(ValueError)
def test_invalid_a_brent_max():
    brent_max(f, -np.inf, 2)


@raises(ValueError)
def test_invalid_b_brent_max():
    brent_max(f, -2, np.inf)


@raises(ValueError)
def test_invalid_a_b_brent_max():
    brent_max(f, 1, 0)


if __name__ == '__main__':
    import sys, nose
    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)