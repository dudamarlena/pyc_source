# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/filter.py
# Compiled at: 2018-05-14 00:27:06
# Size of source mod 2**32: 1768 bytes
"""

function for filtering

"""
import numpy as np

def hamilton_filter(data, h, *args):
    """
    This function applies "Hamilton filter" to the data
    
    http://econweb.ucsd.edu/~jhamilto/hp.pdf
    
    Parameters
    ----------
    data : arrray or dataframe
    h : integer
        Time horizon that we are likely to predict incorrectly.
        Original paper recommends 2 for annual data, 8 for quarterly data,
        24 for monthly data.
    *args : integer
        If supplied, it is p in the paper. Number of lags in regression. 
        Must be greater than h.
        If not supplied, random walk process is assumed.
        
    Note: For seasonal data, it's desirable for p and h to be integer multiples
          of the number of obsevations in a year.
          e.g. For quarterly data, h = 8 and p = 4 are recommended.

    Returns
    -------
    cycle : array of cyclical component
    trend : trend component

    """
    y = np.asarray(data, float)
    T = len(y)
    if len(args) == 1:
        p = args[0]
        X = np.ones((T - p - h + 1, p + 1))
        for j in range(1, p + 1):
            X[:, j] = y[p - j:T - h - j + 1:1]

        b = np.linalg.solve(X.transpose() @ X, X.transpose() @ y[p + h - 1:T])
        trend = np.append(np.zeros(p + h - 1) + np.nan, X @ b)
        cycle = y - trend
    else:
        if len(args) == 0:
            cycle = np.append(np.zeros(h) + np.nan, y[h:T] - y[0:T - h])
            trend = y - cycle
        return (cycle, trend)