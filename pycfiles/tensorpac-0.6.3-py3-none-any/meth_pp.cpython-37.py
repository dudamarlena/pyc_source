# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/methods/meth_pp.py
# Compiled at: 2019-07-09 02:37:45
# Size of source mod 2**32: 1460 bytes
"""Individual methods for assessing Preferred Phase."""
import numpy as np
from .meth_pac import _kl_hr

def preferred_phase(pha, amp, n_bins=18):
    """Compute the preferred phase.

    Parameters
    ----------
    pha, amp : array_like
        Respectively the phase of slower oscillations of shape
        (n_pha, n_epochs, n_times) and the amplitude of faster
        oscillations of shape (n_pha, n_epochs, n_times).
    n_bins : int | 72
        Number of bins for bining the amplitude according to phase
        slices.

    Returns
    -------
    binned_amp : array_like
        The binned amplitude according to the phase of shape
        (n_bins, n_amp, n_pha, n_epochs).
    pp : array_like
        The prefered phase where the amplitude is maximum of shape
        (namp, npha, n_epochs).
    polarvec : array_like
        The phase vector for the polar plot of shape (n_bins,)
    """
    binned_amp = _kl_hr(pha, amp, n_bins)
    binned_amp /= binned_amp.sum(axis=0, keepdims=True)
    idxmax = binned_amp.argmax(axis=0)
    binsize = 2 * np.pi / float(n_bins)
    vecbin = np.arange(-np.pi, np.pi, binsize) + binsize / 2
    pp = vecbin[idxmax]
    polarvec = np.linspace(-np.pi, np.pi, binned_amp.shape[0])
    return (binned_amp, pp, polarvec)