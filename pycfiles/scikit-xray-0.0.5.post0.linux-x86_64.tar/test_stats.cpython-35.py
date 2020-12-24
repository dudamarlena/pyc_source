# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_stats.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 547 bytes
from skxray.core.stats import statistics_1D
import numpy as np
from numpy.testing import assert_array_almost_equal

def test_statistics_1D():
    x = np.linspace(0, 1, 100)
    y = np.arange(100)
    nx = 10
    edges, val = statistics_1D(x, y, nx=nx)
    assert_array_almost_equal(edges, np.linspace(0, 1, nx + 1, endpoint=True))
    assert_array_almost_equal(val, np.sum(y.reshape(nx, -1), axis=1) / 10.0)