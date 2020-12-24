# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_generic.py
# Compiled at: 2018-11-09 10:49:26
# Size of source mod 2**32: 575 bytes
import sys
sys.path.append('/home/adam/data/adam/progs/PolyPy/PolyPy/polypy/')
import Generic as ge, numpy as np
import numpy.testing as npt
from numpy.testing import assert_almost_equal, assert_equal

def test_bin_choose():
    a = ge.bin_choose(4, 2)
    expected = 1
    assert a == expected


def test_pbc():
    a, b = ge.pbc(10, 9, 20)
    c, d = ge.pbc(1, 40, 20)
    expected_a = False
    expected_b = 10
    expected_c = True
    expected_d = 41
    assert a == expected_a
    assert b == expected_b
    assert c == expected_c
    assert d == expected_d