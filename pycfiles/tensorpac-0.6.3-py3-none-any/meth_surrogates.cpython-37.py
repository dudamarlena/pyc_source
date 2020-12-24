# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/methods/meth_surrogates.py
# Compiled at: 2019-10-07 10:13:11
# Size of source mod 2**32: 3930 bytes
"""Individual methods for assessing surrogates."""
import numpy as np
from joblib import Parallel, delayed
from tensorpac.config import CONFIG

def compute_surrogates(pha, amp, ids, fcn, n_perm, n_jobs):
    """Compute surrogates using tensors and parallel computing."""
    if ids == 0:
        return
    fcn_p = {1:swap_pha_amp, 
     2:swap_blocks,  3:time_lag}[ids]

    def para_surr():
        return fcn(*fcn_p(pha, amp))

    s = Parallel(n_jobs=n_jobs, **CONFIG['JOBLIB_CFG'])((delayed(para_surr)() for k in range(n_perm)))
    return np.array(s)


def swap_pha_amp(pha, amp):
    """Swap phase / amplitude trials.

    Parameters
    ----------
    pha, amp : array_like
        Respectively the arrays of phases of shape (n_pha, ..., n_times) and
        the array of amplitudes of shape (n_amp, ..., n_times).

    Returns
    -------
    pha, amp : array_like
        The phase and amplitude to use to compute the distribution of
        permutations

    References
    ----------
    Tort ABL, Komorowski R, Eichenbaum H, Kopell N (2010) Measuring
    Phase-Amplitude Coupling Between Neuronal Oscillations of Different
    Frequencies. Journal of Neurophysiology 104:1195–1210.
    """
    tr_ = np.random.permutation(pha.shape[1])
    return (pha[:, tr_, ...], amp)


def swap_blocks(pha, amp):
    """Swap amplitudes time blocks.

    Parameters
    ----------
    pha, amp : array_like
        Respectively the arrays of phases of shape (n_pha, ..., n_times) and
        the array of amplitudes of shape (n_amp, ..., n_times).

    Returns
    -------
    pha, amp : array_like
        The phase and amplitude to use to compute the distribution of
        permutations

    References
    ----------
    Bahramisharif A, van Gerven MAJ, Aarnoutse EJ, Mercier MR, Schwartz TH,
    Foxe JJ, Ramsey NF, Jensen O (2013) Propagating Neocortical Gamma Bursts
    Are Coordinated by Traveling Alpha Waves. Journal of Neuroscience
    33:18849–18854.
    """
    cut_at = np.random.randint(1, amp.shape[(-1)], (1, ))
    ampl = np.array_split(amp, cut_at, axis=(-1))
    ampl.reverse()
    return (pha, np.concatenate(ampl, axis=(-1)))


def time_lag(pha, amp):
    """Introduce a time lag on phase series.

    Parameters
    ----------
    pha, amp : array_like
        Respectively the arrays of phases of shape (n_pha, ..., n_times) and
        the array of amplitudes of shape (n_amp, ..., n_times).

    Returns
    -------
    pha, amp : array_like
        The phase and amplitude to use to compute the distribution of
        permutations

    References
    ----------
    Canolty RT (2006) High Gamma Power Is Phase-Locked to Theta. science
    1128115:313.
    """
    shift = np.random.randint(pha.shape[(-1)])
    return (np.roll(pha, shift, axis=(-1)), amp)


def normalize(idn, pac, surro):
    """Normalize the phase amplitude coupling.

    This function performs inplace normalization (i.e. without copy of array)

    Parameters
    ----------
    idn : int
        Normalization method to use :

            * 1 : substract the mean of surrogates
            * 2 : divide by the mean of surrogates
            * 3 : substract then divide by the mean of surrogates
            * 4 : substract the mean then divide by the deviation of surrogates
    pac : array_like
        Array of phase amplitude coupling of shape (n_amp, n_pha, ...)
    surro : array_like
        Array of surrogates of shape (n_perm, n_amp, n_pha, ...)
    """
    s_mean, s_std = np.mean(surro, axis=0), np.std(surro, axis=0)
    if idn == 1:
        pac -= s_mean
    else:
        if idn == 2:
            pac /= s_mean
        else:
            if idn == 3:
                pac -= s_mean
                pac /= s_mean
            else:
                if idn == 4:
                    pac -= s_mean
                    pac /= s_std