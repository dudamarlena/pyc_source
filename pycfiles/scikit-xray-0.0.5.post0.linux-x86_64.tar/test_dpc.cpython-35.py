# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_dpc.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 7143 bytes
"""
This is a unit/integrated testing script for dpc.py, which conducts
Differential Phase Contrast (DPC) imaging based on Fourier-shift fitting.

"""
from __future__ import absolute_import, division, print_function
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
import skxray.core.dpc as dpc

def test_image_reduction_default():
    """
    Test image reduction when default parameters (roi and bad_pixels) are used.

    """
    img = np.arange(100).reshape(10, 10)
    xsum = [
     450, 460, 470, 480, 490, 500, 510, 520, 530, 540]
    ysum = [45, 145, 245, 345, 445, 545, 645, 745, 845, 945]
    xline, yline = dpc.image_reduction(img)
    assert_array_equal(xline, xsum)
    assert_array_equal(yline, ysum)


def test_image_reduction():
    """
    Test image reduction when the following parameters are used:
    roi = (3, 3, 5, 5) and bad_pixels = [(0, 1), (4, 4), (7, 8)];
    roi = (0, 0, 20, 20);
    bad_pixels = [(1, -1), (-1, 1)].

    """
    img = np.arange(100).reshape(10, 10)
    roi_0 = (3, 3, 5, 5)
    roi_1 = (0, 0, 20, 20)
    bad_pixels_0 = [(0, 1), (4, 4), (7, 8)]
    bad_pixels_1 = [(1, -1), (-1, 1)]
    xsum = [
     265, 226, 275, 280, 285]
    ysum = [175, 181, 275, 325, 375]
    xsum_bp = [450, 369, 470, 480, 490, 500, 510, 520, 530, 521]
    ysum_bp = [45, 126, 245, 345, 445, 545, 645, 745, 845, 854]
    xsum_roi = [450, 460, 470, 480, 490, 500, 510, 520, 530, 540]
    ysum_roi = [45, 145, 245, 345, 445, 545, 645, 745, 845, 945]
    xline, yline = dpc.image_reduction(img, roi_0, bad_pixels_0)
    xline_bp, yline_bp = dpc.image_reduction(img, bad_pixels=bad_pixels_1)
    xline_roi, yline_roi = dpc.image_reduction(img, roi=roi_1)
    assert_array_equal(xline, xsum)
    assert_array_equal(yline, ysum)
    assert_array_equal(xline_bp, xsum_bp)
    assert_array_equal(yline_bp, ysum_bp)
    assert_array_equal(xline_roi, xsum_roi)
    assert_array_equal(yline_roi, ysum_roi)


def test_rss_factory():
    """
    Test _rss_factory.

    """
    length = 10
    v = [2, 3]
    xdata = np.arange(length)
    beta = complex(0.0, 1.0) * (np.arange(length) - length // 2)
    ydata = xdata * v[0] * np.exp(v[1] * beta)
    rss = dpc._rss_factory(length)
    residue = rss(v, xdata, ydata)
    assert_almost_equal(residue, 0)


def test_dpc_fit():
    """
    Test dpc_fit.
    
    """
    start_point = [
     1, 0]
    length = 100
    solver = 'Nelder-Mead'
    xdata = np.arange(length)
    beta = complex(0.0, 1.0) * (np.arange(length) - length // 2)
    rss = dpc._rss_factory(length)
    v = [
     1.02, -0.00023]
    ydata = xdata * v[0] * np.exp(v[1] * beta)
    res = dpc.dpc_fit(rss, xdata, ydata, start_point, solver)
    assert_array_almost_equal(res, v)
    v = [
     0.88, -0.0048]
    ydata = xdata * v[0] * np.exp(v[1] * beta)
    res = dpc.dpc_fit(rss, xdata, ydata, start_point, solver)
    assert_array_almost_equal(res, v)
    v = [
     0.98, 0.0068]
    ydata = xdata * v[0] * np.exp(v[1] * beta)
    res = dpc.dpc_fit(rss, xdata, ydata, start_point, solver)
    assert_array_almost_equal(res, v)
    v = [
     0.95, 0.0032]
    ydata = xdata * v[0] * np.exp(v[1] * beta)
    res = dpc.dpc_fit(rss, xdata, ydata, start_point, solver)
    assert_array_almost_equal(res, v)


def test_dpc_end_to_end():
    """
    Integrated test for DPC based on dpc_runner.
    
    """
    start_point = [
     1, 0]
    pixel_size = (55, 55)
    focus_to_det = 1460000.0
    scan_rows = 2
    scan_cols = 2
    scan_xstep = 0.1
    scan_ystep = 0.1
    energy = 19.5
    roi = None
    padding = 0
    weighting = 1
    bad_pixels = None
    solver = 'Nelder-Mead'
    img_size = (40, 40)
    scale = True
    negate = True
    ref_image = np.ones(img_size)
    image_sequence = np.ones((scan_rows * scan_cols, img_size[0], img_size[1]))
    phi, a = dpc.dpc_runner(ref_image, image_sequence, start_point, pixel_size, focus_to_det, scan_rows, scan_cols, scan_xstep, scan_ystep, energy, padding, weighting, solver, roi, bad_pixels, negate, scale)
    assert_array_almost_equal(phi, np.zeros((scan_rows, scan_cols)))
    assert_array_almost_equal(a, np.ones((scan_rows, scan_cols)))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)