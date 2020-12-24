# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/utils/signal.py
# Compiled at: 2019-06-11 08:01:24
# Size of source mod 2**32: 1548 bytes
import numpy as np
from scipy.signal import hilbert, tukey

def fast_hilbert(array):
    n_points = array.shape[0]
    n_fft = next_power2(n_points)
    return hilbert(array, n_fft)[:n_points]


def next_power2(num):
    """Compute the smallest power of 2 >= to num.(float -> int)"""
    return 2 ** int(np.ceil(np.log2(num)))


def split_signal(X, n_splits=1, apply_window=True):
    """Split the signal in n_splits chunks for faster training.

    Parameters
    ----------
    X : ndarray, shape (n_channels, n_times)
        Signal to split. It should be only one signal.
    n_splits : int (default: 1)
        Number of splits
    apply_window : bool (default: True)
        If set to True, a tukey window is applied to each split to
        reduce the border artifacts.

    Return
    ------
    X_split: ndarray, shape (n_splits, n_channels, n_times // n_splits)
        The signal splitted in n_splits.
    """
    if not X.ndim == 2:
        raise AssertionError('This splitting utility is only designed for one multivariate signal (n_channels, n_times). Found X.ndim={}.'.format(X.ndim))
    else:
        n_splits = int(n_splits)
        assert n_splits > 0, 'The number of splits should be large than 0.'
        n_channels, n_times = X.shape
        n_times = n_times // n_splits
        X_split = X[:, :n_splits * n_times]
        X_split = X_split.reshape(n_channels, n_splits, n_times).swapaxes(0, 1)
        if apply_window:
            X_split *= tukey(n_times, alpha=0.1)[None, None, :]
    return X_split