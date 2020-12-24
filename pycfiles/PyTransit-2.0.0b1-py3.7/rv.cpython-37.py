# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/utils/rv.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 1035 bytes
from __future__ import division
from numpy import pi, sin, sqrt
from scipy.constants import G

def mp_from_kiepms(K, i, e, p, Ms):
    """Calculates the planet's mass from the fitted parameters"""
    return K * (p * 24 * 3600 / (2 * pi * G)) ** 0.3333333333333333 * Ms ** 0.6666666666666666 / sin(i) * sqrt(1 - e ** 2)