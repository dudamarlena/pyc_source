# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_attractor.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = 'Tests for :mod:`cgp.phenotyping.attractor`.'
import numpy as np
from nose.tools import raises
from .. import cvodeint
from ..phenotyping import attractor

class Test(cvodeint.Cvodeint, attractor.AttractorMixin):
    pass


def ode(t, y, ydot, g_data):
    ydot[:] = -y


def test_exponential_decay():
    r"""
    :math:`y(t) = e^{-t}`, so that :math:`|y|=tol \Leftrightarrow t=\ln tol`.
    """
    test = Test(ode, t=[0, 1500], y=[1])
    tol = 1e-06
    t, y = test.eq(tol=tol)
    np.testing.assert_approx_equal(y, tol)
    np.testing.assert_approx_equal(t, -np.log(tol), significant=4)


def test_logistic_growth():
    test = Test(cvodeint.example_ode.logistic_growth, t=[0, 100], y=0.1)
    t, y, _flag = test.eq(tol=1e-08, last_only=False)
    np.testing.assert_allclose(y[(-1)], 1)
    np.testing.assert_allclose(t[(-1)], 20.687, rtol=0.0001)


def test_already_converged():
    test = Test(ode, t=[0, 100000.0], y=0)
    t, _y, _flag = test.eq(last_only=False)
    assert len(t) == 1


@raises(cvodeint.core.CvodeException)
def test_not_converged():
    test = Test(ode, t=[0, 1], y=[1])
    test.eq()