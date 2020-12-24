# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/tests/test_matrix_eqn.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 913 bytes
"""
Tests for quantecon.util

"""
import numpy as np
from numpy.testing import assert_allclose
from quantecon import matrix_eqn as qme

def test_solve_discrete_lyapunov_zero():
    """Simple test where X is all zeros"""
    A = np.eye(4) * 0.95
    B = np.zeros((4, 4))
    X = qme.solve_discrete_lyapunov(A, B)
    assert_allclose(X, np.zeros((4, 4)))


def test_solve_discrete_lyapunov_B():
    """Simple test where X is same as B"""
    A = np.ones((2, 2)) * 0.5
    B = np.array([[0.5, -0.5], [-0.5, 0.5]])
    X = qme.solve_discrete_lyapunov(A, B)
    assert_allclose(B, X)


def test_solve_discrete_lyapunov_complex():
    """Complex test, A is companion matrix"""
    A = np.array([[complex(0.5, 0.3), complex(0.1, 0.1)],
     [
      1, 0]])
    B = np.eye(2)
    X = qme.solve_discrete_lyapunov(A, B)
    assert_allclose((np.dot(np.dot(A, X), A.conj().transpose()) - X), (-B), atol=1e-15)