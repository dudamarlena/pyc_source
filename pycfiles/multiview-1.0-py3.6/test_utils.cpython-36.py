# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\multiview\tests\test_utils.py
# Compiled at: 2017-12-21 13:53:05
# Size of source mod 2**32: 2369 bytes
import numpy as np
from numpy.testing import assert_array_almost_equal
import multiview.utils as utils

def test_hbeta():
    data = np.arange(25, dtype=float).reshape((5, 5))
    H, P = utils.Hbeta(data, 2)
    real_H = 100.145867
    real_P = np.array([
     [0.864664717, 0.117019644, 0.0158368867,
      0.00214328955, 0.000290062698],
     [
      3.92557174e-05, 5.31268363e-06, 7.18993544e-07,
      9.7305195e-08, 1.31688261e-08],
     [
      1.78220681e-09, 2.41195464e-10, 3.26422564e-11,
      4.41764902e-12, 5.97863781e-13],
     [
      8.09120641e-14, 1.09502571e-14, 1.48195615e-15,
      2.00560955e-16, 2.71429737e-17],
     [
      3.67340203e-18, 4.97140904e-19, 6.72807051e-20,
      9.10545327e-21, 1.2322891e-21]])
    assert_array_almost_equal(H, real_H, decimal=4)
    assert_array_almost_equal(P, real_P, decimal=4)


def test_x2p():
    data = np.arange(25, dtype=float).reshape((5, 5))
    P, beta = utils.x2p(data)
    real_P = np.array([[0.0, 0.25, 0.25, 0.25, 0.25],
     [
      0.25, 0.0, 0.25, 0.25, 0.25],
     [
      0.25, 0.25, 0.0, 0.25, 0.25],
     [
      0.25, 0.25, 0.25, 0.0, 0.25],
     [
      0.25, 0.25, 0.25, 0.25, 0.0]])
    real_beta = np.array([8.8817842e-16, 8.8817842e-16, 8.8817842e-16,
     8.8817842e-16, 8.8817842e-16])
    assert_array_almost_equal(P, real_P, decimal=4)
    assert_array_almost_equal(beta, real_beta, decimal=10)


def test_whiten():
    data = np.array([[1, 2, 3, 4], [4, 3, 2, 1], [2, 4, 1, 3], [1, 3, 2, 4]])
    whitened = utils.whiten(data)
    real_whitened = np.array([
     [0.963475981, 1.11961253, 1.49011612e-08,
      0.0],
     [
      -1.55893688, 0.691958598, 0.0,
      0.0],
     [
      -0.184007539, -1.46559183,
      -1.49011612e-08, 0.0],
     [
      0.779468442, -0.345979299, 0.0,
      0.0]])
    assert_array_almost_equal(whitened, real_whitened, decimal=0)