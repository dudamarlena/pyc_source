# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/utils/mathutils.py
# Compiled at: 2017-11-15 03:51:36
# Size of source mod 2**32: 1942 bytes
"""Math function which can be useful on the full project
"""
import numpy

def naive_rad2deg(x):
    """
    Naive implementation of radiuan to degree.

    Useful for very old numpy (v1.0.1 on MacOSX from Risoe)
    """
    return 180.0 * x / numpy.pi


def naive_deg2rad(x):
    """
    Naive implementation of degree to radiuan.

    Useful for very old numpy (v1.0.1 on MacOSX from Risoe)
    """
    return x * numpy.pi / 180.0


try:
    from numpy import rad2deg, deg2rad
except ImportError:
    rad2deg = naive_deg2rad
    deg2rad = naive_deg2rad