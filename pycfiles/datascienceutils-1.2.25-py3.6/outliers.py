# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/outliers.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 2097 bytes
import numpy as np
from sklearn.preprocessing import Imputer

def impute_data(series, **kwargs):
    Imp = Imputer(**kwargs)
    return Imp.fit_transform(series)


def getOutliers(data, m=2.0):
    """
    data -- is a pandas series
    m --- is the number of sigma deviations
    return:
        Simple data points more than given value times the median
    """
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.0
    return data[(s > m)]


def sigmaDeviation(seq, threshold=3, passes=1):
    for i in range(passes):
        std = np.std(seq)
        seq = filter(lambda x: x > threshold * std, seq)

    return seq


def interQuartileRangeDev(seq, threshold=1.5):
    pass


def capPercentile(seq, threshold=5):
    pass


def zScoreSpikes(seq, zthresh=2):
    mean = np.mean(data)
    std = np.std(data)
    o3 = mean + 2 * std
    o4 = mean + -2 * std