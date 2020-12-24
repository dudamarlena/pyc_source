# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\freq_analysis.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 2093 bytes
from numpy import mean, cumsum
from matplotlib.mlab import find
from .peaks import bigPeaks
from .smooth import smooth
from .tools import plotfft

def fundamental_frequency(s, FS):
    """Compute fundamental frequency along the specified axes.

    Parameters
    ----------
    s: ndarray
        input from which fundamental frequency is computed.
    FS: int
        sampling frequency    
    Returns
    -------
    f0: int
       its integer multiple best explain the content of the signal spectrum.
    """
    s = s - mean(s)
    f, fs = plotfft(s, FS, doplot=False)
    fs = fs[1:int(len(fs) / 2)]
    f = f[1:int(len(f) / 2)]
    cond = find(f > 0.5)[0]
    bp = bigPeaks(fs[cond:], 0)
    if bp == []:
        f0 = 0
    else:
        bp = bp + cond
        f0 = f[min(bp)]
    return f0


def max_frequency(sig, FS):
    """Compute max frequency along the specified axes.

    Parameters
    ----------
    sig: ndarray
        input from which max frequency is computed.
    FS: int
        sampling frequency    
    Returns
    -------
    f_max: int
       0.95 of max_frequency using cumsum.
    """
    f, fs = plotfft(sig, FS, doplot=False)
    t = cumsum(fs)
    ind_mag = find(t > t[(-1)] * 0.95)[0]
    f_max = f[ind_mag]
    return f_max


def median_frequency(sig, FS):
    """Compute median frequency along the specified axes.

    Parameters
    ----------
    sig: ndarray
        input from which median frequency is computed.
    FS: int
        sampling frequency    
    Returns
    -------
    f_max: int
       0.50 of max_frequency using cumsum.
    """
    f, fs = plotfft(sig, FS, doplot=False)
    t = cumsum(fs)
    ind_mag = find(t > t[(-1)] * 0.5)[0]
    f_median = f[ind_mag]
    return f_median