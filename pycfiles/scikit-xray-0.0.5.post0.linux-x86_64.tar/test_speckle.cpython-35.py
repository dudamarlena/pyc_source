# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_speckle.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4626 bytes
from __future__ import absolute_import, division, print_function
import logging, numpy as np
from numpy.testing import assert_array_almost_equal, assert_almost_equal
from skimage.morphology import convex_hull_image
from .. import speckle as xsvs
from .. import roi
from skxray.testing.decorators import skip_if
logger = logging.getLogger(__name__)

def test_xsvs():
    images = []
    for i in range(5):
        int_array = np.tril((i + 2) * np.ones(10))
        int_array[int_array == 0] = i + 1
        images.append(int_array)

    images_sets = [np.asarray(images)]
    roi_data = np.array(([4, 2, 2, 2], [0, 5, 4, 4]), dtype=np.int64)
    label_array = roi.rectangles(roi_data, shape=images[0].shape)
    prob_k_all, std = xsvs.xsvs(images_sets, label_array, timebin_num=2, number_of_img=5, max_cts=None)
    assert_array_almost_equal(prob_k_all[(0, 0)], np.array([0.0, 0.0, 0.2, 0.2, 0.4]))
    assert_array_almost_equal(prob_k_all[(0, 1)], np.array([0.0, 0.2, 0.2, 0.2, 0.4]))


def test_normalize_bin_edges():
    num_times = 3
    num_rois = 2
    mean_roi = np.array([2.5, 4.0])
    max_cts = 5
    bin_edges, bin_cen = xsvs.normalize_bin_edges(num_times, num_rois, mean_roi, max_cts)
    assert_array_almost_equal(bin_edges[(0, 0)], np.array([0.0, 0.4, 0.8,
     1.2, 1.6]))
    assert_array_almost_equal(bin_edges[(2, 1)], np.array([0.0, 0.0625, 0.125,
     0.1875, 0.25, 0.3125,
     0.375, 0.4375, 0.5,
     0.5625, 0.625, 0.6875,
     0.75, 0.8125, 0.875,
     0.9375, 1.0, 1.0625,
     1.125, 1.1875]))
    assert_array_almost_equal(bin_cen[(0, 0)], np.array([0.2, 0.6, 1.0, 1.4]))