# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/feature.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 9622 bytes
"""
This module contains code for extracting features from data
"""
from __future__ import absolute_import, division, print_function
import logging
logger = logging.getLogger(__name__)
from six.moves import zip
import numpy as np
from collections import deque
from .fitting import fit_quad_to_peak

class PeakRejection(Exception):
    __doc__ = 'Custom exception class to indicate that the refine function rejected\n    the candidate peak.\n\n    This uses the exception handling framework in a method akin to\n    `StopIteration` to indicate that there will be no return value.\n    '


def peak_refinement(x, y, cands, window, refine_function, refine_args=None):
    """Refine candidate locations

    Parameters
    ----------
    x : array
        The independent variable, does not need to be evenly spaced.

    y : array
        The dependent variable.  Must correspond 1:1 with the values in `x`

    cands : array
        Array of the indices in `x` (and `y`) for the candidate peaks.

    refine_function : function
        A function which takes a section of data with a peak in it and returns
        the location and height of the peak to sub-sample accuracy.  Additional
        parameters can be passed through via the refine_args kwarg.
        The function signature must be::

            center, height = refine_func(x, y, **kwargs)

        This function may raise `PeakRejection` to indicate no suitable
        peak was found

    window : int
        How many samples to extract on either side of the
        candidate locations are passed to the refine function.  The
        window will be truncated near the boundaries.  The length of the
        data passed to the refine function will be (2 * window + 1).

    refine_args : dict, optional
        The passed to the refine_function

    Returns
    -------
    peak_locations : array
        The locations of the peaks

    peak_heights : array
        The heights of the peaks

    Examples
    --------
    >>> x = np.arange(512)
    >>> tt = np.zeros(512)
    >>> tt += np.exp(-((x - 150.55)/10)**2)
    >>> tt += np.exp(-((x - 450.75)/10)**2)
    >>> cands = scipy.signal.argrelmax(tt)[0]

    >>> print(peak_refinement(x, tt, cands, 10, refine_quadratic))
    (array([ 150.62286432,  450.7909412 ]), array([ 0.96435832,  0.96491501]))
    >>> print(peak_refinement(x, tt, cands, 10, refine_log_quadratic))
    (array([ 150.55,  450.75]), array([ 1.,  1.]))
    """
    x = np.asarray(x)
    y = np.asarray(y)
    cands = np.asarray(cands, dtype=int)
    window = int(window)
    if refine_args is None:
        refine_args = dict()
    out_tmp = deque()
    max_ind = len(x)
    for ind in cands:
        slc = slice(np.max([0, ind - window]), np.min([max_ind, ind + window + 1]))
        try:
            ret = refine_function(x[slc], y[slc], **refine_args)
        except PeakRejection:
            continue
        else:
            out_tmp.append(ret)

    return tuple([np.array(_) for _ in zip(*out_tmp)])


def refine_quadratic(x, y, Rval_thresh=None):
    """
    Attempts to refine the peaks by fitting to
    a quadratic function.

    Parameters
    ----------
    x : array
        Independent variable

    y : array
        Dependent variable

    Rval_thresh : float, optional
        Threshold for R^2 value of fit,  If the computed R^2 is worse than
        this threshold PeakRejection will be raised

    Returns
    -------
    center : float
        Refined estimate for center

    height : float
        Refined estimate for height

    Raises
    ------
    PeakRejection
       Raised to indicate that no suitable peak was found in the
       interval

    """
    beta, R2 = fit_quad_to_peak(x, y)
    if Rval_thresh is not None and R2 < Rval_thresh:
        raise PeakRejection()
    return (beta[1], beta[2])


def refine_log_quadratic(x, y, Rval_thresh=None):
    """
    Attempts to refine the peaks by fitting a quadratic to the log of
    the y-data.  This is a linear approximation of fitting a Gaussian.

    Parameters
    ----------
    x : array
        Independent variable

    y : array
        Dependent variable

    Rval_thresh : float, optional
        Threshold for R^2 value of fit,  If the computed R^2 is worse than
        this threshold PeakRejection will be raised

    Returns
    -------
    center : float
        Refined estimate for center

    height : float
        Refined estimate for height

    Raises
    ------
    PeakRejection
       Raised to indicate that no suitable peak was found in the
       interval

    """
    beta, R2 = fit_quad_to_peak(x, np.log(y))
    if Rval_thresh is not None and R2 < Rval_thresh:
        raise PeakRejection()
    return (beta[1], np.exp(beta[2]))


def filter_n_largest(y, cands, N):
    """Filters the N largest candidate peaks

    Return a maximum of N largest candidates.  If N > len(cands) then
    all of the cands will be returned sorted, else the indices
    of the N largest peaks will be returned in descending order.

    Parameters
    ----------
    y : array
        Independent variable

    cands : array
        An array containing the indices of candidate peaks

    N : int
        The maximum number of peaks to return, sorted by size.
        Must be positive

    Returns
    -------
    cands : array
        An array of the indices of up to the N largest candidates
    """
    cands = np.asarray(cands)
    N = int(N)
    if N <= 0:
        raise ValueError('The maximum number of peaks to return must be positive not {}'.format(N))
    sorted_args = np.argsort(y[cands])
    if len(cands) < N:
        return cands[sorted_args][::-1]
    return cands[sorted_args[-N:]][::-1]


def filter_peak_height(y, cands, thresh, window=5):
    """
    Filter to remove candidate that are too small.  This
    is implemented by looking at the relative height (max - min)
    of the peak in a window around the candidate peak.

    Parameters
    ----------
    y : array
        Independent variable

    cands : array
        An array containing the indices of candidate peaks

    thresh : int
        The minimum peak-to-peak size of the candidate peak to be accepted

    window : int, optional
        The size of the window around the peak to consider

    Returns
    -------
    cands : array
        An array of the indices which pass the filter

    """
    y = np.asarray(y)
    out_tmp = deque()
    max_ind = len(y)
    for ind in cands:
        slc = slice(np.max([0, ind - window]), np.min([max_ind, ind + window + 1]))
        pk_hght = np.ptp(y[slc])
        if pk_hght > thresh:
            out_tmp.append(ind)

    return np.array(out_tmp)


peak_refinement.refine_function = [
 refine_log_quadratic, refine_quadratic]