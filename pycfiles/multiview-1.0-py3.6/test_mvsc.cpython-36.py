# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\multiview\tests\test_mvsc.py
# Compiled at: 2017-12-17 05:58:43
# Size of source mod 2**32: 2751 bytes
import numpy as np
from numpy.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_raises
import multiview.mvsc as mvsc

def test_laplacian_ng():
    data = np.arange(25, dtype=float).reshape((5, 5))
    laplacian = mvsc.laplacian_ng(data)
    real_laplacian = np.array([[0.0, 0.0534, 0.0816, 0.1028, 0.1206],
     [
      0.2672, 0.1714, 0.1527, 0.1466, 0.145],
     [
      0.4082, 0.24, 0.2, 0.182, 0.1723],
     [
      0.5144, 0.2933, 0.238, 0.2117, 0.1964],
     [
      0.603, 0.3384, 0.2708, 0.2378, 0.2181]])
    assert_array_almost_equal(laplacian, real_laplacian, decimal=4)


def test_suggested_sigma():
    data = np.arange(25, dtype=float).reshape((5, 5))
    s_sigma = mvsc.suggested_sigma(data)
    real_s_sigma = 7.0
    assert_array_almost_equal(s_sigma, real_s_sigma, decimal=4)


def test_gaussian_similarity():
    data = np.arange(25, dtype=float).reshape((5, 5))
    similarity = mvsc.distance_gaussian_similarity(data, 2)
    print(similarity)
    real_similarity = np.array([[1.0, 0.8824, 0.6065, 0.3246, 0.1353],
     [
      0.0439, 0.011, 0.0021, 0.0003, 0.0],
     [
      0.0, 0.0, 0.0, 0.0, 0.0],
     [
      0.0, 0.0, 0.0, 0.0, 0.0],
     [
      0.0, 0.0, 0.0, 0.0, 0.0]])
    assert_array_almost_equal(similarity, real_similarity, decimal=4)


def test_mvsc_error():
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False, False]
    mvsc_est = mvsc.MVSC(k=2)
    assert_raises(ValueError, mvsc_est.fit, data, is_distance)
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 49, dtype=float).reshape((4, 6))
    data = [one, two]
    is_distance = [False, False]
    mvsc_est = mvsc.MVSC(k=2)
    assert_raises(ValueError, mvsc_est.fit, data, is_distance)
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False]
    mvsc_est = mvsc.MVSC(k=(-2))
    assert_raises(ValueError, mvsc_est.fit, data, is_distance)


def test_mvsc():
    one = np.arange(25, dtype=float).reshape((5, 5))
    two = np.arange(25, 50, dtype=float).reshape((5, 5))
    data = [one, two]
    is_distance = [False, False]
    mvsc_est = mvsc.MVSC(k=2)
    mvsc_est.fit(data, is_distance)