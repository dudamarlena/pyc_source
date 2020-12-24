# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/tests/test_lyapunov.py
# Compiled at: 2018-05-14 00:27:06
# Size of source mod 2**32: 447 bytes
"""
Tests for ricatti.py

"""
import numpy as np
from numpy.testing import assert_allclose
from quantecon.matrix_eqn import solve_discrete_lyapunov

def test_dlyap_simple_ones():
    A = np.zeros((4, 4))
    B = np.ones((4, 4))
    sol = solve_discrete_lyapunov(A, B)
    assert_allclose(sol, np.ones((4, 4)))


def test_dlyap_scalar():
    a = 0.5
    b = 0.75
    sol = solve_discrete_lyapunov(a, b)
    assert_allclose(sol, np.ones((1, 1)))