# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/stats/distribution.py
# Compiled at: 2017-01-18 23:31:27
import numpy as np, scipy.stats
__author__ = 'Roberto Calandra'
__version__ = '0.4'

def mean_var(data):
    mean = np.nanmean(data, axis=0)
    var = np.nanvar(data, axis=0)
    return [mean, var]


def mean_std(data):
    mean = np.nanmean(data, axis=0)
    std = np.nanstd(data, axis=0)
    return [mean, std]


def mean_percentile(data, des_percentiles='68+95+99'):
    """

    :param data:
    :param des_percentiles:
    :return:
    """
    mean, variance = mean_var(data=data)
    out = np.array(map(int, des_percentiles.split('+')))
    for i in range(out.size):
        assert 0 <= out[i] <= 100, 'Percentile must be >0 <100; instead is %f' % out[i]

    percentiles = percentileFromGaussian(mean=mean, variance=variance, percentile=out)
    return [mean, percentiles]


def median_percentile(data, des_percentiles='68+95+99'):
    """

    :param data:
    :param des_percentiles: string with +separated values of the percentiles
    :return:
    """
    median = np.nanmedian(data, axis=0)
    out = np.array(map(int, des_percentiles.split('+')))
    for i in range(out.size):
        assert 0 <= out[i] <= 100, 'Percentile must be >0 <100; instead is %f' % out[i]

    list_percentiles = np.empty((2 * out.size,), dtype=out.dtype)
    list_percentiles[0::2] = out
    list_percentiles[1::2] = 100 - out
    percentiles = np.nanpercentile(data, list_percentiles, axis=0)
    return [median, percentiles]


def percentileFromGaussian(mean, variance, percentile='68+95+99'):
    """

    :param mean:
    :param variance:
    :param percentile:
    :return:
    """
    a = np.array([0.68, 0.95, 0.99])
    std = np.sqrt(variance)
    out = scipy.stats.norm.interval(a, loc=mean, scale=std)
    out = np.ravel(np.column_stack((out[1], out[0])))
    return np.nan_to_num(out)