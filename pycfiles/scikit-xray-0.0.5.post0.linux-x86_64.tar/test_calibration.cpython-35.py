# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_calibration.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4493 bytes
from __future__ import absolute_import, division, print_function
import numpy as np, skxray.core.calibration as calibration, skxray.core.calibration as core

def _draw_gaussian_rings(shape, calibrated_center, r_list, r_width):
    R = core.radial_grid(calibrated_center, shape)
    I = np.zeros_like(R)
    for r in r_list:
        tmp = 100 * np.exp(-((R - r) / r_width) ** 2)
        I += tmp

    return I


def test_refine_center():
    center = np.array((500, 550))
    I = _draw_gaussian_rings((1000, 1001), center, [
     50, 75, 100, 250, 500], 5)
    nx_opts = [
     None, 300]
    for nx in nx_opts:
        out = calibration.refine_center(I, center + 1, (1, 1), phi_steps=20, nx=nx, min_x=10, max_x=300, window_size=5, thresh=0, max_peaks=4)
        if not np.all(np.abs(center - out) < 0.1):
            raise AssertionError


def test_blind_d():
    gaus = lambda x, center, height, width: height * np.exp(-((x - center) / width) ** 2)
    name = 'Si'
    wavelength = 0.18
    window_size = 5
    threshold = 0.1
    cal = calibration.calibration_standards[name]
    tan2theta = np.tan(cal.convert_2theta(wavelength))
    D = 200
    expected_r = D * tan2theta
    bin_centers = np.linspace(0, 50, 2000)
    I = np.zeros_like(bin_centers)
    for r in expected_r:
        I += gaus(bin_centers, r, 100, 0.2)

    d, dstd = calibration.estimate_d_blind(name, wavelength, bin_centers, I, window_size, len(expected_r), threshold)
    assert np.abs(d - D) < 1e-06


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)