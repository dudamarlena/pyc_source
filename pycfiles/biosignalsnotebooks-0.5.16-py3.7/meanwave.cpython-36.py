# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\waves\meanwave.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 560 bytes
from numpy import mean

def meanwave(signals):
    """ This function computes the meanwave of various signals.
    
    Given a set of signals, with the same number of samples, this function 
    returns an array representative of the meanwave of those signals - which is
    a wave computed with the mean values of each signal's samples. 
    
    Parameters
    ----------
    signals: matrix-like
      the input signals.

    Returns
    -------
    mw: array-like
      the resulted meanwave  
    """
    return mean(signals, 0)