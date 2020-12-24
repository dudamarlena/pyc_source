# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/gpk_voicing/pseudo_dur.py
# Compiled at: 2009-11-23 13:45:09
"""Duration estimator for speech.

Usage: s_slope [flags]
Flags: -f FFF opens file FFF for reading.
        -c XXX  selects column XXX (either a data name or an integer).
        -o FFF  sets the output file.
        -dt #.##   Sets the interval for calculating the output.

It takes a local spectrum,
bins it onto the Bark scale,
converts to perceptual loudness (via **E).
Then, it computes a measure of how far you can go
from each point before the spectrum changes too much.
"""
import math as M, numpy

def pdur_guts(s, t, dir, Dt, C):
    """t is an integer; an index into the data.
        S is the normalized perceptual spectrum."""
    n = len(s)
    assert s.shape[1] < 200, 'Implausibly long feature vector.  Is s transposed?'
    sumdiff = 0.0
    len_sum = 0.5
    ctr_sum = 0.125 * dir
    i = t + dir
    while i >= 0 and i < n and sumdiff < 8:
        delta_diff = Dt * C * numpy.sum(numpy.absolute(s[i] - s[t]) ** 2)
        if delta_diff <= 0:
            lsd = M.exp(-sumdiff)
            len_sum += lsd
            slopeint = M.exp(-sumdiff) * 0.5
            ctr_sum += (i - t - 0.5 * dir) * lsd + dir * slopeint
            i += dir
        else:
            lsd = M.exp(-sumdiff) * (1.0 - M.exp(-delta_diff)) / delta_diff
            len_sum += lsd
            slopeint = M.exp(-sumdiff) * (1.0 - M.exp(-delta_diff) * (1 + delta_diff)) / delta_diff ** 2
            ctr_sum += (i - t - 0.5 * dir) * lsd + dir * slopeint
            i += dir
            sumdiff += delta_diff

    return (len_sum * Dt, ctr_sum * Dt)