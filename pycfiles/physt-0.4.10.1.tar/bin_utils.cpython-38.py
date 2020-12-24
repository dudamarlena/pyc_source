# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/honza/code/my/physt/tests/../physt/bin_utils.py
# Compiled at: 2019-10-09 15:30:11
# Size of source mod 2**32: 4469 bytes
"""Methods for investigation and manipulation of bin arrays."""
from typing import Tuple
import numpy as np

def make_bin_array(bins) -> np.ndarray:
    """Turn bin data into array understood by HistogramXX classes.

    Parameters
    ----------
    bins: array_like
        Array of edges or array of edge tuples

    Examples
    --------
    >>> make_bin_array([0, 1, 2])
    array([[0, 1],
           [1, 2]])
    >>> make_bin_array([[0, 1], [2, 3]])
    array([[0, 1],
           [2, 3]])
    """
    bins = np.asarray(bins)
    if bins.ndim == 1:
        return np.hstack((bins[:-1, np.newaxis], bins[1:, np.newaxis]))
    if bins.ndim == 2:
        if bins.shape[1] != 2:
            raise RuntimeError('Binning schema with ndim==2 must have 2 columns')
        return bins
    raise RuntimeError('Binning schema must have ndim==1 or ndim==2')


def to_numpy_bins(bins) -> np.ndarray:
    """Convert physt bin format to numpy edges.

    Parameters
    ----------
    bins: array_like
        1-D (n) or 2-D (n, 2) array of edges

    Returns
    -------
    edges: all edges
    """
    bins = np.asarray(bins)
    if bins.ndim == 1:
        return bins
    if not is_consecutive(bins):
        raise RuntimeError('Cannot create numpy bins from inconsecutive edges')
    return np.concatenate([bins[:1, 0], bins[:, 1]])


def to_numpy_bins_with_mask(bins) -> Tuple[(np.ndarray, np.ndarray)]:
    """Numpy binning edges including gaps.

    Parameters
    ----------
    bins: array_like
        1-D (n) or 2-D (n, 2) array of edges

    Returns
    -------
    edges: np.ndarray
        all edges
    mask: np.ndarray
        List of indices that correspond to bins that have to be included

    Examples
    --------
    >>> to_numpy_bins_with_mask([0, 1, 2])
    (array([0.,   1.,   2.]), array([0, 1]))

    >>> to_numpy_bins_with_mask([[0, 1], [2, 3]])
    (array([0, 1, 2, 3]), array([0, 2])
    """
    bins = np.asarray(bins)
    if bins.ndim == 1:
        edges = bins
        if bins.shape[0] > 1:
            mask = np.arange(bins.shape[0] - 1)
        else:
            mask = []
    else:
        if bins.ndim == 2:
            edges = []
            mask = []
            j = 0
            if bins.shape[0] > 0:
                edges.append(bins[(0, 0)])
                for i in range(bins.shape[0] - 1):
                    mask.append(j)
                    edges.append(bins[(i, 1)])
                    if bins[(i, 1)] != bins[(i + 1, 0)]:
                        edges.append(bins[(i + 1, 0)])
                        j += 1
                    j += 1
                else:
                    mask.append(j)
                    edges.append(bins[(-1, 1)])

            else:
                raise RuntimeError('to_numpy_bins_with_mask: array with dim=1 or 2 expected')
        else:
            assert np.all(np.diff(edges) > 0), 'to_numpy_bins_with_mask: edges array not monotone.'
        return (edges, mask)


def is_rising(bins) -> bool:
    """Check whether the bins are in raising order.

    Does not check if the bins are consecutive.

    Parameters
    ----------
    bins: array_like
    """
    bins = make_bin_array(bins)
    if np.any(bins[:, 0] >= bins[:, 1]):
        return False
    if np.any(bins[1:, 0] < bins[:-1, 1]):
        return False
    return True


def is_consecutive(bins, rtol: float=1e-05, atol: float=1e-08) -> bool:
    """Check whether the bins are consecutive (edges match).

    Does not check if the bins are in rising order.
    """
    bins = np.asarray(bins)
    if bins.ndim == 1:
        return True
    bins = make_bin_array(bins)
    return np.allclose(bins[1:, 0], bins[:-1, 1], rtol, atol)


def is_bin_subset(sub, sup) -> bool:
    """Check whether all bins in one binning are present also in another:

    Parameters
    ----------
    sub: array_like
        Candidate for the bin subset
    sup: array_like
        Candidate for the bin superset
    """
    sub = make_bin_array(sub)
    sup = make_bin_array(sup)
    for row in sub:
        if not (row == sup).all(axis=1).any():
            return False
        return True


def is_bin_superset(sup, sub) -> bool:
    """Inverse of is_bin_subset"""
    return is_bin_subset(sub=sub, sup=sup)