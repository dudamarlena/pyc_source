# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/other/kmc2/custom_distances.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 3778 bytes
import numpy as np
from numpy.fft import rfft, irfft
from scipy.fftpack import next_fast_len
from sklearn.metrics.pairwise import check_pairwise_arrays

def roll_invariant_euclidean_distances(X, Y=None, squared=False):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.
    The distance is the minimum of the euclidean distance over all rolls:

        dist(x, y) = min_       au(||x(t) - y(t -       au)||^2)

    Parameters
    ----------
    X : array, shape (n_samples_1, n_features)

    Y : array, shape (n_samples_2, n_features)

    squared : boolean
        Not used. Only for API compatibility.

    Returns
    -------
    distances : array, shape (n_samples_1, n_samples_2)

    """
    X = np.atleast_2d(X)
    if Y is not None:
        Y = np.atleast_2d(Y)
    X, Y = check_pairwise_arrays(X, Y)
    n_samples_1, n_features = X.shape
    n_samples_2, n_features = Y.shape
    X_norm = np.power(np.linalg.norm(X, axis=1), 2)
    Y_norm = np.power(np.linalg.norm(Y, axis=1), 2)
    n_fft = n_features
    X_hat = rfft(X, n_fft, axis=1)
    Y_hat = rfft(Y, n_fft, axis=1).conj()
    distances = np.zeros((n_samples_1, n_samples_2))
    if n_samples_2 > 1:
        print('RIED on %s samples, this might be slow' % (distances.shape,))
    for ii in range(n_samples_1):
        for jj in range(n_samples_2):
            XY = irfft(X_hat[ii] * Y_hat[jj], n_fft).max()
            distances[(ii, jj)] = X_norm[ii] + Y_norm[jj] - 2 * XY

    distances += 1e-12
    return distances


def translation_invariant_euclidean_distances(X, Y=None, squared=False, symmetric=False):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.
    The distance is the minimum of the euclidean distance over a set of
    translations:

        dist(x, y) = min_{i, j}(||x(i:i+T) - y(j:j+T)||^2)

    where T = n_features / 2, and 1 <= i, j <= n_features / 2

    Parameters
    ----------
    X : array, shape (n_samples_1, n_features)

    Y : array, shape (n_samples_2, n_features)

    squared : boolean
        Not used. Only for API compatibility.

    symmetric : boolean
        If False, the distance is not symmetric anymore, since we keep indice
        j fixed at `n_features / 4`.

    Returns
    -------
    distances : array, shape (n_samples_1, n_samples_2)

    """
    X = np.atleast_2d(X)
    if Y is not None:
        Y = np.atleast_2d(Y)
    X, Y = check_pairwise_arrays(X, Y)
    n_samples_1, n_features = X.shape
    n_samples_2, n_features = Y.shape
    distances = np.zeros((n_samples_1, n_samples_2))
    for nn in range(n_samples_1):
        for mm in range(n_samples_2):
            XY = (X[nn, :, None] - Y[mm, None, :]) ** 2
            if symmetric:
                jj_range = np.arange(n_features // 2)
            else:
                jj_range = [
                 n_features // 4]
            dist = np.zeros((n_features // 2, len(jj_range)))
            for ii in range(n_features // 2):
                for jj, kk in enumerate(jj_range):
                    xy = XY[ii:ii + n_features // 2, kk:kk + n_features // 2]
                    dist[(ii, jj)] = xy.trace(axis1=0, axis2=1)

            distances[(nn, mm)] = dist.min()

    return distances