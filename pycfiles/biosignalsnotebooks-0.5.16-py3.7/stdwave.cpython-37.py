# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\waves\stdwave.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 771 bytes
from numpy import std

def stdwave(signal):
    """ This function computes the standard deviation error wave of various 
    signals.
    
    Given a set of signals, with the same number of samples, this function 
    returns an array representative of the error wave of those signals - which 
    is a wave computed with the standard deviation error values of each signal's
    samples.

    Parameters
    ----------
    signals: matrix-like
      the input signals.
      the signals should be writen in the form of (NxM) matrix,
        where N is the number of samples and M is the number of channels #changed by David Belo

    Returns
    -------
    stdw: array-like
      the resulting error wave.  
    """
    return std(signal, 0)