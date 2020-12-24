# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\stat_analysis.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 942 bytes
import numpy as np
from scipy.stats import gaussian_kde

def scott_density(signal):
    s_k = np.asarray(signal, np.float)
    bw, widths, gridsize, cut = ('scott', 0.8, 100, 3)
    kde = gaussian_kde(s_k, bw)
    if isinstance(bw, str):
        bw = 'scotts' if bw == 'scott' else bw
        bw = getattr(kde, '%s_factor' % bw)()
    support_min = max(min(s_k) - bw * cut, -np.inf)
    support_max = min(max(s_k) + bw * cut, np.inf)
    y = np.linspace(support_min, support_max, gridsize)
    dens = kde.evaluate(y)
    scl = 1 / (dens.max() / (widths / 2))
    dens *= scl
    return (
     dens, y)


def matrix_recurrence(signal):
    N = len(signal)
    S = np.ones((N, N))
    for j in np.arange(N):
        for i in np.arange(N):
            ij = abs(signal[j] - signal[i])
            if ij <= 0.1 * np.std(signal):
                S[(i, j)] = 0

    return S