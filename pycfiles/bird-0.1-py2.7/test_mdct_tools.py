# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/bird/tests/test_mdct_tools.py
# Compiled at: 2014-10-25 04:28:21
import numpy as np
from numpy.testing import assert_array_almost_equal
from bird.mdct_tools import mdct, imdct

def test_mdct():
    """Test mdct and imdct tight frame property"""
    sfreq = 1000.0
    f = 7.0
    x1 = np.sin(2.0 * np.pi * f * np.arange(128, dtype=float) / sfreq)
    x2 = np.sin(2.0 * np.pi * f * np.arange(512, dtype=float) / sfreq)
    rng = np.random.RandomState(42)
    x3 = rng.standard_normal(x1.shape)
    wsize = 32
    for x in [x1, x2, x3]:
        X = mdct(x, wsize)
        xp = imdct(X, wsize)
        assert_array_almost_equal(x, xp, decimal=12)