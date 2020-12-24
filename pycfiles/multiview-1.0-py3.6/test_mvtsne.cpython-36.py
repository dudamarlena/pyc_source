# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\multiview\tests\test_mvtsne.py
# Compiled at: 2017-12-17 05:58:40
# Size of source mod 2**32: 1393 bytes
import numpy as np
from sklearn.utils.testing import assert_raises
import multiview.mvtsne as mvtsne

def test_mvtsne_error():
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False, False]
    mvtsne_est = mvtsne.MvtSNE(k=2)
    assert_raises(ValueError, mvtsne_est.fit, data, is_distance)
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 49, dtype=float).reshape((4, 6))
    data = [one, two]
    is_distance = [False, False]
    mvtsne_est = mvtsne.MvtSNE(k=2)
    assert_raises(ValueError, mvtsne_est.fit, data, is_distance)
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False]
    mvtsne_est = mvtsne.MvtSNE(k=(-2))
    assert_raises(ValueError, mvtsne_est.fit, data, is_distance)


def test_mvtsne():
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False]
    mvtsne_est = mvtsne.MvtSNE(k=2)
    mvtsne_est.fit(data, is_distance)