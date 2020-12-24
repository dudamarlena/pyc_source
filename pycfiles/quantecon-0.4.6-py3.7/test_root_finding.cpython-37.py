# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/optimize/tests/test_root_finding.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 2988 bytes
import numpy as np
from numpy.testing import assert_almost_equal, assert_allclose
from numba import njit
from quantecon.optimize import newton, newton_halley, newton_secant, bisect, brentq

@njit
def func(x):
    """
    Function for testing on.
    """
    return x ** 3 - 1


@njit
def func_prime(x):
    """
    Derivative for func.
    """
    return 3 * x ** 2


@njit
def func_prime2(x):
    """
    Second order derivative for func.
    """
    return 6 * x


@njit
def func_two(x):
    """
    Harder function for testing on.
    """
    return np.sin(4 * (x - 0.25)) + x + x ** 20 - 1


@njit
def func_two_prime(x):
    """
    Derivative for func_two.
    """
    return 4 * np.cos(4 * (x - 0.25)) + 20 * x ** 19 + 1


@njit
def func_two_prime2(x):
    """
    Second order derivative for func_two
    """
    return 380 * x ** 18 - 16 * np.sin(4 * (x - 0.25))


def test_newton_basic():
    """
    Uses the function f defined above to test the scalar maximization 
    routine.
    """
    true_fval = 1.0
    fval = newton(func, 5, func_prime)
    assert_almost_equal(true_fval, (fval.root), decimal=4)


def test_newton_basic_two():
    """
    Uses the function f defined above to test the scalar maximization 
    routine.
    """
    true_fval = 1.0
    fval = newton(func, 5, func_prime)
    assert_allclose(true_fval, (fval.root), rtol=1e-05, atol=0)


def test_newton_hard():
    """
    Harder test for convergence.
    """
    true_fval = 0.408
    fval = newton(func_two, 0.4, func_two_prime)
    assert_allclose(true_fval, (fval.root), rtol=1e-05, atol=0.01)


def test_halley_basic():
    """
    Basic test for halley method
    """
    true_fval = 1.0
    fval = newton_halley(func, 5, func_prime, func_prime2)
    assert_almost_equal(true_fval, (fval.root), decimal=4)


def test_halley_hard():
    """
    Harder test for halley method
    """
    true_fval = 0.408
    fval = newton_halley(func_two, 0.4, func_two_prime, func_two_prime2)
    assert_allclose(true_fval, (fval.root), rtol=1e-05, atol=0.01)


def test_secant_basic():
    """
    Basic test for secant option.
    """
    true_fval = 1.0
    fval = newton_secant(func, 5)
    assert_allclose(true_fval, (fval.root), rtol=1e-05, atol=0.001)


def test_secant_hard():
    """
    Harder test for convergence for secant function.
    """
    true_fval = 0.408
    fval = newton_secant(func_two, 0.4)
    assert_allclose(true_fval, (fval.root), rtol=1e-05, atol=0.01)


def run_check(method, name):
    a = -1
    b = np.sqrt(3)
    true_fval = 0.408
    r = method(func_two, a, b)
    assert_allclose(true_fval, (r.root), atol=0.01, rtol=1e-05, err_msg=('method %s' % name))


def test_bisect_basic():
    run_check(bisect, 'bisect')


def test_brentq_basic():
    run_check(brentq, 'brentq')


if __name__ == '__main__':
    import sys, nose
    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)