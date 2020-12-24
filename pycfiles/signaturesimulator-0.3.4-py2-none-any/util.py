# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: signaturesimulator/sense/util.py
# Compiled at: 2018-02-20 04:22:41
"""
Module for some utilty functions
"""
c0 = 299792458.0

def f2lam(f):
    """
    given the frequency in GHz,
    return the wavelength [m]
    """
    return c0 / (f * 1000000000.0)