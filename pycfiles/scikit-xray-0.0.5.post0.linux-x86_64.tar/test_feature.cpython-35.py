# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_feature.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 5929 bytes
from __future__ import absolute_import, division, print_function
import numpy as np
from numpy.testing import assert_array_almost_equal
from nose.tools import assert_raises
import skxray.core.feature as feature

def _test_refine_helper(x_data, y_data, center, height, refine_method, refine_args):
    """
    helper function for testing
    """
    test_center, test_height = refine_method(x_data, y_data, **refine_args)
    assert_array_almost_equal(np.array([test_center, test_height]), np.array([center, height]))


def test_refine_methods():
    refine_methods = [
     feature.refine_quadratic,
     feature.refine_log_quadratic]
    test_data_gens = [
     lambda x, center, height, width: width * (x - center) ** 2 + height,
     lambda x, center, height, width: height * np.exp(-((x - center) / width) ** 2)]
    x = np.arange(128)
    for center in (15, 75, 110):
        for height in (5, 10, 100):
            for rf, dm in zip(refine_methods, test_data_gens):
                yield (
                 _test_refine_helper,
                 x, dm(x, center, height, 5), center, height, rf, {})


def test_filter_n_largest():
    gauss_gen = lambda x, center, height, width: height * np.exp(-((x - center) / width) ** 2)
    cands = np.array((10, 25, 50, 75, 100))
    x = np.arange(128, dtype=float)
    y = np.zeros_like(x)
    for c, h in zip(cands, (10, 15, 25, 30, 35)):
        y += gauss_gen(x, c, h, 3)

    for j in range(1, len(cands) + 2):
        out = feature.filter_n_largest(y, cands, j)
        if not len(out) == np.min([len(cands), j]):
            raise AssertionError

    assert_raises(ValueError, feature.filter_n_largest, y, cands, 0)
    assert_raises(ValueError, feature.filter_n_largest, y, cands, -1)


def test_filter_peak_height():
    gauss_gen = lambda x, center, height, width: height * np.exp(-((x - center) / width) ** 2)
    cands = np.array((10, 25, 50, 75, 100))
    heights = (10, 20, 30, 40, 50)
    x = np.arange(128, dtype=float)
    y = np.zeros_like(x)
    for c, h in zip(cands, heights):
        y += gauss_gen(x, c, h, 3)

    for j, h in enumerate(heights):
        out = feature.filter_peak_height(y, cands, h - 5, window=5)
        assert len(out) == len(heights) - j
        out = feature.filter_peak_height(y, cands, h + 5, window=5)
        if not len(out) == len(heights) - j - 1:
            raise AssertionError


def test_peak_refinement():
    gauss_gen = lambda x, center, height, width: height * np.exp(-((x - center) / width) ** 2)
    cands = np.array((10, 25, 50, 75, 100))
    heights = (10, 20, 30, 40, 50)
    x = np.arange(128, dtype=float)
    y = np.zeros_like(x)
    for c, h in zip(cands, heights):
        y += gauss_gen(x, c + 0.5, h, 3)

    loc, ht = feature.peak_refinement(x, y, cands, 5, feature.refine_log_quadratic)
    assert_array_almost_equal(loc, cands + 0.5, decimal=3)
    assert_array_almost_equal(ht, heights, decimal=3)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)