# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/util/distances.py
# Compiled at: 2013-04-02 18:46:29
"""
Created on May 2, 2011

@author: jonathanfriedman

Distance functions between two vectors that are of general utility.
"""
import numpy as np, scipy.cluster.hierarchy as sch
from numpy import array, log, log2, sum, all

def KLsym(x, y):
    if not all((x == 0) == (y == 0)):
        raise ValueError('KL divergence not defined when only one distribution is 0.')
    x[x == 0] = 1
    y[y == 0] = 1
    d = 0.5 * np.sum((x - y) * (log2(x) - log2(y)))
    return d


def JS(x, y):
    import warnings
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    idx = np.where(x == 0)
    x_pos = x.copy()
    x_pos[idx] = 1
    idy = np.where(y == 0)
    y_pos = y.copy()
    y_pos[idy] = 1
    dx = x * log2(2 * x_pos / (x_pos + y))
    dy = y * log2(2 * y_pos / (x + y_pos))
    d = 0.5 * sum(dx + dy)
    return d


def JS_2(x, y, method='CS'):
    """
    Use estimates of the average entropy and entropy of the average to calculate JSD.
    """
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    import rpy2.robjects.numpy2ri
    from R_utilities import entropy
    Hx = entropy(x, method=method)
    Hy = entropy(y, method=method)
    Hxy = entropy(x + y, method=method)
    d = np.log2(np.exp(Hxy - (Hx + Hy) / 2))
    return d


def JSsqrt(x, y):
    d = JS(x, y)
    return d ** 0.5


def Morisita(x, y):
    d = 1 - 2 * sum(x * y) / (sum(x ** 2) + sum(y ** 2))
    return d


def chao_jaccard(x, y):
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    import rpy2.robjects.numpy2ri
    rfos = importr('fossil')
    d = 1 - array(rfos.chao_jaccard(x, y))
    return d[0]


def aitchison(x, y, center='mean'):
    lx = log(x)
    ly = log(y)
    if center is 'mean':
        m = np.mean
    elif center is 'median':
        m = np.median
    clr_x = lx - m(lx)
    clr_y = ly - m(ly)
    d = sum((clr_x - clr_y) ** 2) ** 0.5
    return d


namedMetrics = {'klsym': KLsym, 
   'kl_sym': KLsym, 
   'js': JS, 
   'jsd': JS, 
   'jssqrt': JSsqrt, 
   'js_sqrt': JSsqrt, 
   'morisita': Morisita, 
   'chao_jaccard': chao_jaccard, 
   'jaccard_chao': chao_jaccard, 
   'aitchison': aitchison}

def pdist(x, metric, sqaureform=True, **kwargs):
    metric = metric.strip().lower()
    if metric in namedMetrics:
        f = namedMetrics[metric]
        D = sch.distance.pdist(x, f, **kwargs)
    else:
        D = sch.distance.pdist(x, metric=metric, **kwargs)
    if sqaureform:
        D = sch.distance.squareform(D)
    return D


def cdist(x, y, metric, **kwargs):
    metric = metric.strip().lower()
    if metric in namedMetrics:
        f = namedMetrics[metric]
        D = sch.distance.cdist(x, y, f, **kwargs)
    else:
        D = sch.distance.cdist(x, y, metric=metric, **kwargs)
    return D


if __name__ == '__main__':
    x = array([1.0, 2, 1, 1, 0])
    y = array([1.0, 1, 1, 1, 0])
    print JS_2(x, y)
    print JS(x / sum(x), y / sum(y))