# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pytrack_analysis/preprocessing.py
# Compiled at: 2017-07-25 14:19:40
# Size of source mod 2**32: 740 bytes
from scipy import signal
import numpy as np, pandas as pd, time

def interpolate(_data):
    return _data.interpolate()


def to_mm(_data, px2mm):
    return _data * px2mm


def gaussian_filter(_df, _len=16, _sigma=1.6):
    cols = np.empty((len(_df.index), len(_df.columns)))
    cols.fill(np.nan)
    header = []
    for column in _df:
        header.append(column)
        cols[:, len(header) - 1] = gaussian_filtered((_df[column]), _len=_len, _sigma=_sigma)

    return pd.DataFrame(cols, columns=header)


def gaussian_filtered(_X, _len=16, _sigma=1.6):
    norm = np.sqrt(2 * np.pi) * _sigma
    window = signal.gaussian((_len + 1), std=_sigma) / norm
    return np.convolve(_X, window, 'same')