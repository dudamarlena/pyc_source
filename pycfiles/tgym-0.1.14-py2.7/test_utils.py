# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/test_utils.py
# Compiled at: 2017-06-13 15:07:39
import numpy as np
from tgym.utils import calc_spread

def test_calc_spread():
    spread_coefficients = [
     1, -0.1]
    prices = np.array([1, 2, 10, 20])
    spread_price = (-1, 1)
    assert calc_spread(prices, spread_coefficients) == spread_price