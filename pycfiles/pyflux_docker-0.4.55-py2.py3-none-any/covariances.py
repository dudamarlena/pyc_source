# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/covariances.py
# Compiled at: 2018-02-01 11:59:15
import numpy as np
from math import sqrt

def cov(x, lag=0):
    if lag >= x.shape[0]:
        raise ValueError('Not enough observations to compute autocovariance')
    else:
        x1 = x[lag:x.shape[0]]
        x2 = x[0:x.shape[0] - lag]
        return np.sum((x1 - np.mean(x)) * (x2 - np.mean(x))) / x1.shape[0]


def acf(x, lag=0):
    x1 = x[lag:x.shape[0]]
    return cov(x, lag=lag) / cov(x, lag=0)


def acf_plot(data, max_lag=10):
    import matplotlib.pyplot as plt, seaborn as sns
    plt.figure(figsize=(15, 5))
    ax = plt.subplot(111)
    plt.bar(range(1, 10), [ acf(data, lag) for lag in range(1, 10) ])
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('ACF Plot')
    plt.axhline(0 + 2 / np.sqrt(len(data)), linestyle='-', color='black')
    plt.axhline(0 - 2 / np.sqrt(len(data)), linestyle='-', color='black')
    plt.show()