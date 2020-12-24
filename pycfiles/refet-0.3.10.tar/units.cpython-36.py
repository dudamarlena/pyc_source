# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\RefET\refet\units.py
# Compiled at: 2018-08-21 12:59:16
# Size of source mod 2**32: 223 bytes
import math

def _deg2rad(deg):
    return deg * math.pi / 180.0


def _rad2deg(rad):
    return rad * 180.0 / math.pi


def _c2f(c):
    return c * 1.8 + 32


def _f2c(f):
    return (f - 32) * 0.5555555555555556