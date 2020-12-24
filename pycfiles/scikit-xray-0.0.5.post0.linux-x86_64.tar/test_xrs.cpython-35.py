# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/constants/tests/test_xrs.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 3735 bytes
from __future__ import absolute_import, division, print_function
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_equal
from skxray.core.constants.xrs import HKL, calibration_standards
from skxray.core.utils import q_to_d, d_to_q

def smoke_test_powder_standard():
    name = 'Si'
    cal = calibration_standards[name]
    assert name == cal.name
    for d, hkl, q in cal:
        assert_array_almost_equal(d_to_q(d), q)
        assert_array_almost_equal(q_to_d(q), d)
        assert_array_equal(np.linalg.norm(hkl), hkl.length)

    assert_equal(str(cal), 'Calibration standard: Si')
    assert_equal(len(cal), 11)


def test_hkl():
    a = HKL(1, 1, 1)
    b = HKL('1', '1', '1')
    c = HKL(h='1', k='1', l='1')
    d = HKL(1.5, 1.5, 1.75)
    assert_equal(a, b)
    assert_equal(a, c)
    assert_equal(a, d)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)