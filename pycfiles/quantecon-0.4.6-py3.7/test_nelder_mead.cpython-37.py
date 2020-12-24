# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/optimize/tests/test_nelder_mead.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 9958 bytes
"""
Tests for `multivar_maximization.py`

"""
import numpy as np
from numba import njit
from numpy.testing import assert_allclose
from nose.tools import raises
from quantecon.optimize import nelder_mead
from ..nelder_mead import _nelder_mead_algorithm

@njit
def rosenbrock(x):
    f = 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2
    return -f


@njit
def powell(x):
    f = (x[0] + 10 * x[1]) ** 2 + 5 * (x[2] - x[3]) ** 2 + (x[1] - 2 * x[2]) ** 4 + 10 * (x[0] - x[3]) ** 4
    return -f


@njit
def mccormick(x):
    f = np.sin(x[0] + x[1]) + (x[0] - x[1]) ** 2 - 1.5 * x[0] + 2.5 * x[1] + 1
    return -f


@njit
def bohachevsky(x):
    f = x[0] ** 2 + x[1] ** 2 - 0.3 * np.cos(3 * np.pi * x[0]) - 0.4 * np.cos(4 * np.pi * x[1]) + 0.7
    return -f


@njit
def easom(x):
    f = -(np.cos(x[0]) * np.cos(x[1]) * np.exp(-(x[0] - np.pi) ** 2 - (x[1] - np.pi) ** 2))
    return -f


@njit
def perm_function(x, β):
    d = x.size
    f = 0
    for i in range(1, d + 1):
        temp = 0
        for j in range(1, d + 1):
            temp += (j + β) * (x[(j - 1)] ** i - 1 / j ** i)

        f += temp ** 2

    return -f


@njit
def rotated_hyper_ellipsoid(x):
    d = x.size
    f = 0
    for i in range(1, d + 1):
        for j in range(i):
            f += x[(j - 1)] ** 2

    return -f


@njit
def booth(x):
    f = (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2
    return -f


@njit
def zakharov(x):
    d = x.size
    _range = np.arange(1, d + 1)
    f = (x ** 2).sum() + (0.5 * x * _range).sum() ** 2 + (0.5 * x * _range).sum() ** 4
    return -f


@njit
def colville(x):
    f = 100 * (x[0] ** 2 - x[1]) ** 2 + (x[0] - 1) ** 2 + (x[2] - 1) ** 2 + 90 * (x[2] ** 2 - x[3]) ** 2 + 10.1 * ((x[1] - 1) ** 2 + (x[3] - 1) ** 2) + 19.8 * (x[1] - 1) * (x[3] - 1)
    return -f


@njit
def styblinski_tang(x):
    f = 0.5 * (x ** 4 - 16 * x ** 2 + 5 * x).sum()
    return -f


@njit
def goldstein_price(x):
    p1 = (x[0] + x[1] + 1) ** 2
    p2 = 19 - 14 * x[0] + 3 * x[0] ** 2 - 14 * x[1] + 6 * x[0] * x[1] + 3 * x[1] ** 2
    p3 = (2 * x[0] - 3 * x[1]) ** 2
    p4 = 18 - 32 * x[0] + 12 * x[0] ** 2 + 48 * x[1] - 36 * x[0] * x[1] + 27 * x[1] ** 2
    f = (1 + p1 * p2) * (30 + p3 * p4)
    return -f


@njit
def sum_squared(x):
    return -(x ** 2).sum()


@njit
def f(x):
    return -(x[0] ** 2 + x[0])


@njit
def g(x):
    if x[0] < 1:
        return -(0.75 * x[0] ** 2 - x[0] + 2)
    return -(0.5 * x[0] ** 2 - x[0] + 1)


@njit
def h(x):
    return -(abs(x[0]) + abs(x[1]))


class TestMaximization:

    def test_rosenbrock(self):
        sol = np.array([1.0, 1.0])
        fun = 0.0
        x0 = np.array([-2, 1])
        results = nelder_mead(rosenbrock, x0, tol_x=1e-20, tol_f=1e-20)
        assert_allclose((results.x), sol, atol=0.0001)
        assert_allclose((results.fun), fun, atol=0.0001)

    def test_powell(self):
        sol = np.zeros(4)
        fun = 0.0
        x0 = np.array([3.0, -1.0, 0.0, 1.0])
        results = nelder_mead(powell, x0, tol_x=1e-20, tol_f=1e-20)
        assert_allclose((results.x), sol, atol=0.0001)
        assert_allclose((results.fun), fun, atol=0.0001)

    def test_mccormick(self):
        sol = np.array([-0.54719, -1.54719])
        fun = 1.9133
        x0 = np.array([-1.0, -1.5])
        bounds = np.array([[-1.5, 4.0],
         [
          -3.0, 4.0]])
        results = nelder_mead(mccormick, x0, bounds=bounds)
        assert_allclose((results.x), sol, rtol=0.001)
        assert_allclose((results.fun), fun, rtol=0.001)

    def test_bohachevsky(self):
        sol = np.array([0.0, 0.0])
        fun = 0.0
        x0 = np.array([np.pi, -np.pi])
        results = nelder_mead(bohachevsky, x0)
        assert_allclose((results.x), sol, atol=0.0001)
        assert_allclose((results.fun), fun, atol=0.0001)

    def test_easom(self):
        sol = np.array([np.pi, np.pi])
        fun = 1.0
        x0 = np.array([5, -1])
        results = nelder_mead(easom, x0, tol_x=1e-20, tol_f=1e-20)
        assert_allclose((results.x), sol, atol=0.0001)
        assert_allclose((results.fun), fun, atol=0.0001)

    def test_perm_function(self):
        d = 4.0
        x0 = np.ones(int(d))
        bounds = np.array([[-d, d]] * int(d))
        sol = np.array([1 / d for d in range(1, int(d) + 1)])
        fun = 0.0
        results = nelder_mead(perm_function, x0, bounds=bounds, args=(1.0, ), tol_x=1e-30,
          tol_f=1e-30)
        assert_allclose((results.x), sol, atol=1e-07)
        assert_allclose((results.fun), fun, atol=1e-07)

    def test_rotated_hyper_ellipsoid(self):
        d = 5
        x0 = np.random.normal(size=d)
        bounds = np.array([[-65.536, 65.536]] * d)
        sol = np.zeros(d)
        fun = 0.0
        results = nelder_mead(rotated_hyper_ellipsoid, x0, bounds=bounds, tol_x=1e-30,
          tol_f=1e-30)
        assert_allclose((results.x), sol, atol=1e-07)
        assert_allclose((results.fun), fun, atol=1e-07)

    def test_booth(self):
        x0 = np.array([0.0, 0.0])
        sol = np.array([1.0, 3.0])
        fun = 0.0
        results = nelder_mead(booth, x0, tol_x=1e-20, tol_f=1e-20)
        assert_allclose((results.x), sol, atol=1e-07)
        assert_allclose((results.fun), fun, atol=1e-07)

    def test_zakharov(self):
        x0 = np.array([-3.0, 8.0, 1.0, 3.0, -0.5])
        bounds = np.array([[-5.0, 10.0]] * 5)
        sol = np.zeros(5)
        fun = 0.0
        results = nelder_mead(zakharov, x0, bounds=bounds, tol_f=1e-30, tol_x=1e-30)
        assert_allclose((results.x), sol, atol=1e-07)
        assert_allclose((results.fun), fun, atol=1e-07)

    def test_colville(self):
        x0 = np.array([-3.5, 9.0, 0.25, -1.0])
        bounds = np.array([[-10.0, 10.0]] * 4)
        sol = np.ones(4)
        fun = 0.0
        results = nelder_mead(colville, x0, bounds=bounds, tol_f=1e-35, tol_x=1e-35)
        assert_allclose(results.x, sol)
        assert_allclose((results.fun), fun, atol=1e-07)

    def test_styblinski_tang(self):
        d = 8
        x0 = -np.ones(d)
        bounds = np.array([[-5.0, 5.0]] * d)
        sol = np.array([-2.903534] * d)
        fun = 39.16599 * d
        results = nelder_mead(styblinski_tang, x0, bounds=bounds, tol_f=1e-35, tol_x=1e-35)
        assert_allclose((results.x), sol, rtol=0.0001)
        assert_allclose((results.fun), fun, rtol=1e-05)

    def test_goldstein_price(self):
        x0 = np.array([-1.5, 0.5])
        results = nelder_mead(goldstein_price, x0)
        sol = np.array([0.0, -1.0])
        fun = -3.0
        assert_allclose((results.x), sol, atol=1e-05)
        assert_allclose(results.fun, fun)

    def test_sum_squared(self):
        x0 = np.array([0.5, -np.pi, np.pi])
        sol = np.zeros(3)
        fun = 0.0
        results = nelder_mead(sum_squared, x0, tol_f=1e-50, tol_x=1e-50)
        assert_allclose((results.x), sol, atol=1e-05)
        assert_allclose((results.fun), fun, atol=1e-05)

    def test_corner_sol(self):
        sol = np.array([0.0])
        fun = 0.0
        x0 = np.array([10.0])
        bounds = np.array([[0.0, np.inf]])
        results = nelder_mead(f, x0, bounds=bounds, tol_f=1e-20)
        assert_allclose(results.x, sol)
        assert_allclose(results.fun, fun)

    def test_discontinuous(self):
        sol = np.array([1.0])
        fun = -0.5
        x0 = np.array([-10.0])
        results = nelder_mead(g, x0)
        assert_allclose(results.x, sol)
        assert_allclose(results.fun, fun)


@raises(ValueError)
def test_invalid_bounds_1():
    x0 = np.array([-2.0, 1.0])
    bounds = np.array([[10.0, -10.0], [10.0, -10.0]])
    nelder_mead(rosenbrock, x0, bounds=bounds)


@raises(ValueError)
def test_invalid_bounds_2():
    x0 = np.array([-2.0, 1.0])
    bounds = np.array([[10.0, -10.0, 10.0, -10.0]])
    nelder_mead(rosenbrock, x0, bounds=bounds)


@raises(ValueError)
def test_invalid_ρ():
    vertices = np.array([[-2.0, 1.0],
     [
      -2.1, 1.0],
     [
      -2.0, 1.05]])
    invalid_ρ = -1.0
    _nelder_mead_algorithm(rosenbrock, vertices, ρ=invalid_ρ)


@raises(ValueError)
def test_invalid_χ():
    vertices = np.array([[-2.0, 1.0],
     [
      -2.1, 1.0],
     [
      -2.0, 1.05]])
    invalid_χ = 0.5
    _nelder_mead_algorithm(rosenbrock, vertices, χ=invalid_χ)


@raises(ValueError)
def test_invalid_ρχ():
    vertices = np.array([[-2.0, 1.0],
     [
      -2.1, 1.0],
     [
      -2.0, 1.05]])
    ρ = 2
    χ = 1.5
    _nelder_mead_algorithm(rosenbrock, vertices, ρ=ρ, χ=χ)


@raises(ValueError)
def test_invalid_γ():
    vertices = np.array([[-2.0, 1.0],
     [
      -2.1, 1.0],
     [
      -2.0, 1.05]])
    invalid_γ = -1e-07
    _nelder_mead_algorithm(rosenbrock, vertices, γ=invalid_γ)


@raises(ValueError)
def test_invalid_σ():
    vertices = np.array([[-2.0, 1.0],
     [
      -2.1, 1.0],
     [
      -2.0, 1.05]])
    invalid_σ = 1.0000001
    _nelder_mead_algorithm(rosenbrock, vertices, σ=invalid_σ)


if __name__ == '__main__':
    import sys, nose
    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)