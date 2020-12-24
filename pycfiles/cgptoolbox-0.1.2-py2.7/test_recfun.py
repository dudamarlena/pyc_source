# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_recfun.py
# Compiled at: 2012-02-06 03:58:36
"""Tests for :mod:`cgp.utils.recfun`."""
import numpy as np
from nose.tools import raises
from cgp.utils import recfun
a = np.array([(0, 1)], dtype=[('a', float), ('b', float)])
b = np.array([(2, 3)], dtype=[('c', float), ('d', float)])

@raises(TypeError)
def test_cbind_empty():
    recfun.cbind()


def test_cbind_void():
    """Check that ()-shaped arrays are OK."""
    recfun.cbind(a[0], b[0])


def test_cbind_squeeze():
    """Check that trailing singleton dimensions are squeezed."""
    recfun.cbind(np.tile(a, 2), np.tile(b, 2).reshape(2, 1))