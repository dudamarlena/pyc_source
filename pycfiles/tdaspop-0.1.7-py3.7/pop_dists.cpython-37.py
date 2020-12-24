# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdaspop/pop_dists.py
# Compiled at: 2019-10-22 14:59:17
# Size of source mod 2**32: 1107 bytes
"""
Distributions often needed for sampling populations 
"""
__all__ = [
 'double_gaussian']
import numpy as np

def double_gaussian(mode, sigmam, sigmap, size=1000, rng=np.random.RandomState(1)):
    """Draw samples from a double gaussian distribution

    Parameters
    ----------
    mode: `np.float`
        mode of the distribution.
    sigmam: `np.float`
        standard deviation of the distribution
    sigmap: `np.float`
        standard deviation of the distribution
    size: int
        number of samples required
    rng: instance `np.random.RandomState`, defaults to state with seed 1.

    Returns
    -------
    samples: `np.ndarray`
    samples from the double gaussian distribution with given parameters.

    Notes
    -----
    This code is essentially the same as code contributed by D. Rubin for SN.
    """
    sigs = np.abs([sigmam, sigmap])
    probs = sigs / sigs.sum()
    sigsamps = rng.choice((-sigs[0], sigs[1]), size=size, replace=True, p=probs)
    samps = np.abs(rng.normal(0.0, 1.0, size=size))
    return samps * sigsamps + mode