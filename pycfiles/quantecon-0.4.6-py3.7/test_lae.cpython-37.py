# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/tests/test_lae.py
# Compiled at: 2018-11-25 18:01:46
# Size of source mod 2**32: 1073 bytes
"""
Tests for lae.py

TODO: write (economically) meaningful tests for this module

"""
from nose.tools import assert_equal
import numpy as np
from scipy.stats import lognorm
from quantecon import LAE
s = 0.2
delta = 0.1
a_sigma = 0.4
alpha = 0.4
phi = lognorm(a_sigma)

def p(x, y):
    d = s * x ** alpha
    return phi.pdf((y - (1 - delta) * x) / d) / d


n_a, n_b, n_y = (50, (5, 5), 20)
a = np.random.rand(n_a) + 0.01
b = (np.random.rand)(*n_b) + 0.01
y = np.linspace(0, 10, 20)
lae_a = LAE(p, a)
lae_b = LAE(p, b)

def test_x_flattened():
    """lae: is x flattened and reshaped"""
    assert_equal(lae_b.X.shape[(-1)], 1)
    assert_equal(lae_a.X.shape[(-1)], 1)


def test_x_2d():
    """lae: is x 2d"""
    assert_equal(lae_a.X.ndim, 2)
    assert_equal(lae_b.X.ndim, 2)


def test_call_shapes():
    """lae: shape of call to lae"""
    assert_equal(lae_a(y).shape, (n_y,))
    assert_equal(lae_b(y).shape, (n_y,))