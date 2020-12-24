# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/EPD64.framework/Versions/7.0/lib/python2.7/site-packages/pyspec/undulator.py
# Compiled at: 2011-06-03 10:37:00
import numpy as np
_C = 299792458.0
_EMASS = 511003.414

def calcB0(B_Rem, lambda_0, gap):
    """Calculate B0 for an undulator of wavelength lambda at gap gap"""
    return B_rem / np.sinh(np.pi * gap / lambda_0)


def calcK(lambda_0, B):
    """Calculate K for an undulator"""
    return _C * lambda_0 * B / (_EMASS * 2.0 * np.pi)