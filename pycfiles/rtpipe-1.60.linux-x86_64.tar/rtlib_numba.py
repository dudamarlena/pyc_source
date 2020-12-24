# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/rtlib_numba.py
# Compiled at: 2017-06-21 14:37:45
import numpy as np
from numba import jit, complex64, float32, int32, boolean
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
try:
    import pyfftw, pyfftw.interfaces.numpy_fft as fft
except ImportError:
    from numpy import fft

@jit
def flag_calcmad(data):
    """ Calculate median absolute deviation of data array """
    absdev = np.abs(data - np.median(data))
    return np.median(absdev)