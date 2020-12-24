# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_correlation.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 5507 bytes
from __future__ import absolute_import, division, print_function
import logging, numpy as np
from numpy.testing import assert_array_almost_equal, assert_almost_equal
from nose.tools import assert_raises
from skimage import data
import skxray.core.correlation as corr, skxray.core.roi as roi, skxray.core.utils as utils
logger = logging.getLogger(__name__)

def test_correlation():
    num_levels = 4
    num_bufs = 8
    num_qs = 2
    img_dim = (50, 50)
    roi_data = np.array(([10, 20, 12, 14], [40, 10, 9, 10]), dtype=np.int64)
    indices = roi.rectangles(roi_data, img_dim)
    img_stack = np.random.randint(1, 5, size=(500, ) + img_dim)
    g2, lag_steps = corr.multi_tau_auto_corr(num_levels, num_bufs, indices, img_stack)
    assert_array_almost_equal(lag_steps, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8,
     10, 12, 14, 16, 20, 24, 28,
     32, 40, 48, 56]))
    assert_array_almost_equal(g2[1:, 0], 1.0, decimal=2)
    assert_array_almost_equal(g2[1:, 1], 1.0, decimal=2)


def test_image_stack_correlation():
    num_levels = 1
    num_bufs = 2
    coins = data.camera()
    coins_stack = []
    for i in range(4):
        coins_stack.append(coins)

    coins_mesh = np.zeros_like(coins)
    coins_mesh[coins < 30] = 1
    coins_mesh[coins > 50] = 2
    g2, lag_steps = corr.multi_tau_auto_corr(num_levels, num_bufs, coins_mesh, coins_stack)
    assert_almost_equal(True, np.all(g2[:, 0], axis=0))
    assert_almost_equal(True, np.all(g2[:, 1], axis=0))
    num_buf = 5
    assert_raises(ValueError, lambda : corr.multi_tau_auto_corr(num_levels, num_buf, coins_mesh, coins_stack))
    mesh = np.zeros_like(coins)
    assert_raises(ValueError, lambda : corr.multi_tau_auto_corr(num_levels, num_bufs, mesh, coins_stack))


def test_auto_corr_scat_factor():
    num_levels, num_bufs = (3, 4)
    tot_channels, lags = utils.multi_tau_lags(num_levels, num_bufs)
    beta = 0.5
    relaxation_rate = 10.0
    baseline = 1.0
    g2 = corr.auto_corr_scat_factor(lags, beta, relaxation_rate, baseline)
    assert_array_almost_equal(g2, np.array([1.5, 1.0, 1.0, 1.0, 1.0,
     1.0, 1.0, 1.0]), decimal=8)