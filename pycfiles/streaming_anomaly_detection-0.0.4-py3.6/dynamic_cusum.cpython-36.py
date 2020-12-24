# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/anomaly_detection/dynamic_cusum.py
# Compiled at: 2019-02-19 10:52:03
# Size of source mod 2**32: 927 bytes
"""
This algorithm focus on detect anomaly based on CUSUM chart.
"""
import pandas as pd

def detect_via_high_sum(ts, istart=5, threshold_times=5):
    """
    detect a time series using high sum algorithm
    :param ts: the time series to be detected
    :param istart: the data from index 0 to index istart will be used as cold startup data to train
    :param threshold_times: the times for setting threshold
    :return: a generator, and each element will be a tuple, the tuple is an anomaly point, the tuple's format: (anomaly_point_index, anomaly_point_value)
    """
    assert isinstance(ts, pd.Series), 'given ts must be pd.Series'
    S_h = 0
    for i, v in ts.iteritems():
        if i < istart:
            pass
        else:
            mean, std = ts[:i].mean(), ts[:i].std()
            S_h_ = max(0, S_h + v - mean - std)
            if S_h_ > threshold_times * std:
                yield (
                 i, v)
            else:
                S_h = S_h_