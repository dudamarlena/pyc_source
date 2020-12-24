# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/fitting/funcs.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 1095 bytes
from __future__ import absolute_import, division, print_function
import six, numpy as np

def fit_quad_to_peak(x, y):
    """
    Fits a quadratic to the data points handed in
    to the from y = b[0](x-b[1])**2 + b[2] and R2
    (measure of goodness of fit)

    Parameters
    ----------
    x : ndarray
        locations
    y : ndarray
        values

    Returns
    -------
    b : tuple
       coefficients of form y = b[0](x-b[1])**2 + b[2]

    R2 : float
      R2 value

    """
    lenx = len(x)
    if lenx < 3:
        raise Exception('insufficient points handed in ')
    X = np.vstack((x ** 2, x, np.ones(lenx))).T
    beta, _, _, _ = np.linalg.lstsq(X, y)
    SSerr = np.sum((np.polyval(beta, x) - y) ** 2)
    SStot = np.sum((y - np.mean(y)) ** 2)
    ret_beta = (
     beta[0],
     -beta[1] / (2 * beta[0]),
     beta[2] - beta[0] * (beta[1] / (2 * beta[0])) ** 2)
    return (
     ret_beta, 1 - SSerr / SStot)