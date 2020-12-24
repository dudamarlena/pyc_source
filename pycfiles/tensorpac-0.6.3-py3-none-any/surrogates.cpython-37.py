# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/surrogates.py
# Compiled at: 2019-06-19 05:13:56
# Size of source mod 2**32: 6186 bytes
"""Surrogates evaluation."""
import numpy as np
from joblib import Parallel, delayed
from .methods import compute_pac
__all__ = 'compute_surrogates'

def compute_surrogates(pha, amp, surargs, pacargs, nperm, njobs):
    """Compute surrogates using tensors and parallel computing.

    Parameters
    ----------
    pha : array_like
        Array of phases of shapes (npha, ..., npts)
    amp : array_like
        Array of amplitudes of shapes (namp, ..., npts)
    suragrs : tuple
        Tuple containing the arguments to pass to the suro_switch function.
    pacargs : tuple
        Tuple containing the arguments to pass to the compute_pac function.
    nperm : int
        Number of permutations.
    njobs : int
        Number of jos for the parallel computing.

    Returns
    -------
    suro : array_like
        Array of pac surrogates of shape (nperm, npha, namp, ..., npts)
    """
    s = Parallel(n_jobs=njobs, prefer='threads')((delayed(_compute_sur)(pha, amp, surargs, pacargs) for k in range(nperm)))
    return np.array(s)


def _compute_sur(pha, amp, surargs, pacargs):
    """Compute surrogates.

    This is clearly not the optimal implementation. Indeed, for each loop the
    suroSwicth and compute_pac have a several "if" that slow down the
    execution, at least a little bit. And, it's not esthetic but joblib doesn't
    accept to pickle functions.

    Parameters
    ----------
    pha : array_like
        Array of phases of shapes (npha, ..., npts)
    amp : array_like
        Array of amplitudes of shapes (namp, ..., npts)
    suragrs : tuple
        Tuple containing the arguments to pass to the suro_switch function.
    pacargs : tuple
        Tuple containing the arguments to pass to the compute_pac function.
    """
    pha, amp = suro_switch(pha, amp, *surargs)
    return compute_pac(pha, amp, *pacargs)


def suro_switch(pha, amp, idn, axis, traxis):
    """List of methods to compute surrogates.

    The surrogates are used to normalized the cfc value. It help to determine
    if the cfc is reliable or not. Usually, the surrogates used the same cfc
    method on surrogates data.
    Here's the list of methods to compute surrogates:
    - No surrogates
    - Swap phase/amplitude across trials
    - Swap amplitude blocks across time.
    - Shuffle amplitude time-series
    - Time lag
    """
    if idn == 0:
        return
    if idn == 1:
        return swap_pha_amp(pha, amp, traxis)
    if idn == 2:
        return swap_blocks(pha, amp, axis)
    if idn == 3:
        return time_lag(pha, amp, axis)
    raise ValueError(str(idn) + ' is not recognized as a valid surrogates evaluation method.')


def swap_pha_amp(pha, amp, axis):
    """Swap phase / amplitude trials (Tort, 2010).

    Parameters
    ----------
    pha : array_like
        Array of phases of shapes (npha, ..., npts)
    amp : array_like
        Array of amplitudes of shapes (namp, ..., npts)
    axis : int
        Location of the trial axis.

    Returns
    -------
    pha : array_like
        Swapped version of phases of shapes (npha, ..., npts)
    amp : array_like
        Swapped version of amplitudes of shapes (namp, ..., npts)
    """
    return (
     pha, _dimswap(amp, axis))


def swap_blocks(pha, amp, axis):
    """Swap amplitudes time blocks.

    To reproduce (Bahramisharif, 2013), use a number of blocks of 2.

    Parameters
    ----------
    pha : array_like
        Array of phases of shapes (npha, ..., npts)
    amp : array_like
        Array of amplitudes of shapes (namp, ..., npts)
    axis : int
        Location of the time axis.

    Returns
    -------
    pha : array_like
        Original version of phases of shapes (npha, ..., npts)
    amp : array_like
        Swapped version of amplitudes of shapes (namp, ..., npts)
    """
    cut_at = np.random.randint(1, amp.shape[axis], (1, ))
    ampl = np.array_split(amp, cut_at, axis=axis)
    ampl.reverse()
    return (pha, np.concatenate(ampl, axis=axis))


def time_lag(pha, amp, axis):
    """Introduce a time lag on phase series..

    Parameters
    ----------
    pha : array_like
        Array of phases of shapes (npha, ..., npts)
    amp : array_like
        Array of amplitudes of shapes (namp, ..., npts)
    axis : int
        Location of the time axis.

    Returns
    -------
    pha : array_like
        Shiffted version of phases of shapes (npha, ..., npts)
    amp : array_like
        Original version of amplitudes of shapes (namp, ..., npts)
    """
    npts = pha.shape[(-1)]
    return (np.roll(pha, (np.random.randint(npts)), axis=axis), amp)


def _dimswap(x, axis=0):
    """Swap values into an array at a specific axis.

    Parameters
    ----------
    x : array_like
        Array of data to swap
    axis : int | 0
        Axis along which to perform swapping.

    Returns
    -------
    x : array_like
        Swapped version of x.
    """
    dimvec = [
     slice(None)] * x.ndim
    rndvec = np.arange(x.shape[axis])
    np.random.shuffle(rndvec)
    dimvec[axis] = rndvec
    return x[tuple(dimvec)]