# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/fitting/tests/test_background.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4017 bytes
from __future__ import absolute_import, division, print_function
import numpy as np
from numpy.testing import assert_allclose
from skxray.core.fitting import snip_method

def test_snip_method():
    """
    test of background function from xrf fit
    """
    xmin = 0
    xmax = 3000
    xval = np.arange(-20, 20, 0.1)
    std = 0.01
    yval1 = np.exp(-xval ** 2 / 2 / std ** 2)
    yval2 = np.exp(-(xval - 10) ** 2 / 2 / std ** 2)
    yval3 = np.exp(-(xval + 10) ** 2 / 2 / std ** 2)
    a0 = 1.0
    a1 = 0.1
    a2 = 0.5
    bg_true = a0 * np.exp(-xval * a1 + a2)
    yval = yval1 + yval2 + yval3 + bg_true
    bg = snip_method(yval, 0.0, 1.0, 0.0, xmin=xmin, xmax=3000, spectral_binning=None, width=0.1)
    cutval = 15
    bg_true_part = bg_true[cutval:-cutval]
    bg_cal_part = bg[cutval:-cutval]
    assert_allclose(bg_true_part, bg_cal_part, rtol=0.001, atol=0.1)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)