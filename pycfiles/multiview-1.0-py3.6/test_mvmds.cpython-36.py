# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\multiview\tests\test_mvmds.py
# Compiled at: 2017-12-17 05:58:50
# Size of source mod 2**32: 1877 bytes
import numpy as np
from numpy.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_raises
import multiview.mvmds as mvmds

def test_preprocess_mds():
    data = np.arange(25, dtype=float).reshape((5, 5))
    preprocessed_data = mvmds.preprocess_mvmds(data)
    sim = np.array([[40.0, 20.0, 0.0, -20.0, -40.0],
     [
      20.0, 10.0, 0.0, -10.0, -20.0],
     [
      0.0, 0.0, 0.0, 0.0, 0.0],
     [
      -20.0, -10.0, 0.0, 10.0, 20.0],
     [
      -40.0, -20.0, 0.0, 20.0, 40.0]])
    assert_array_almost_equal(preprocessed_data, sim, decimal=3)


def test_mvmds_error():
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False, False]
    mvmds_est = mvmds.MVMDS(k=2)
    assert_raises(ValueError, mvmds_est.fit, data, is_distance)
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 49, dtype=float).reshape((4, 6))
    data = [one, two]
    is_distance = [False, False]
    mvmds_est = mvmds.MVMDS(k=2)
    assert_raises(ValueError, mvmds_est.fit, data, is_distance)
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False]
    mvmds_est = mvmds.MVMDS(k=(-2))
    assert_raises(ValueError, mvmds_est.fit, data, is_distance)


def test_mvmds():
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False]
    mvmds_est = mvmds.MVMDS(k=2)
    mvmds_est.fit(data, is_distance)