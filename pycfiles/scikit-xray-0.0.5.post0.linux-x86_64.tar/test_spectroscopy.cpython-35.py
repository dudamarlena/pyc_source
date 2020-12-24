# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_spectroscopy.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 5892 bytes
from __future__ import absolute_import, division, print_function
import numpy as np
from nose.tools import assert_raises
from numpy.testing import assert_array_almost_equal
from skxray.core.spectroscopy import align_and_scale, integrate_ROI, integrate_ROI_spectrum

def synthetic_data(E, E0, sigma, alpha, k, beta):
    """
    return synthetic data of the form
    d = alpha * e ** (-(E - e0)**2 / (2 * sigma ** 2) + beta * sin(k * E)

    Parameters
    ----------
    E : ndarray
        The energies to compute values at

    E0 : float
       Location of the peak

    sigma : float
       Width of the peak

    alpha : float
       Height of peak

    k : float
       Frequency of oscillations

    beta : float
       Magnitude of oscillations
    """
    return alpha * np.exp(-(E - E0) ** 2 / (2 * sigma ** 2)) + beta * (1 + np.sin(k * E))


def test_align_and_scale_smoketest():
    E = np.linspace(0, 50, 1000)
    e_list = []
    c_list = []
    for j in range(25, 35, 2):
        e_list.append(E)
        c_list.append(synthetic_data(E, j + j / 100, j / 10, 1000, 2 * np.pi * 6 / 50, 60))

    e_cor_list, c_cor_list = align_and_scale(e_list, c_list)


def test_integrate_ROI_errors():
    E = np.arange(100)
    C = np.ones_like(E)
    assert_raises(ValueError, integrate_ROI, E, C, [
     32, 1], [2, 10])
    assert_raises(ValueError, integrate_ROI, E, C, -1, 2)
    assert_raises(ValueError, integrate_ROI, E, C, 2, 110)
    assert_raises(ValueError, integrate_ROI, E, C, [
     32, 1], [2, 10, 32])
    assert_raises(ValueError, integrate_ROI, C, C, 2, 10)
    E[2] = 50
    E[50] = 2
    assert_raises(ValueError, integrate_ROI, E, C, 2, 60)


def test_integrate_ROI_compute():
    E = np.arange(100)
    C = np.ones_like(E)
    assert_array_almost_equal(integrate_ROI(E, C, 5.5, 6.5), 1)
    assert_array_almost_equal(integrate_ROI(E, C, 5.5, 11.5), 6)
    assert_array_almost_equal(integrate_ROI(E, C, [5.5, 17], [11.5, 23]), 12)


def test_integrate_ROI_spectrum_compute():
    C = np.ones(100)
    E = np.arange(101)
    assert_array_almost_equal(integrate_ROI_spectrum(E, C, 5, 6), 1)
    assert_array_almost_equal(integrate_ROI_spectrum(E, C, 5, 11), 6)
    assert_array_almost_equal(integrate_ROI_spectrum(E, C, [5, 17], [11, 23]), 12)


def test_integrate_ROI_reverse_input():
    E = np.arange(100)
    C = E[::-1]
    E_rev = E[::-1]
    C_rev = C[::-1]
    assert_array_almost_equal(integrate_ROI(E_rev, C_rev, [5.5, 17], [11.5, 23]), integrate_ROI(E, C, [5.5, 17], [11.5, 23]))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)