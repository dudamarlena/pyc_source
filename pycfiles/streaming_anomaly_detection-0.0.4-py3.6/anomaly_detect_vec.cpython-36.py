# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/anomaly_detection/anomaly_detect_vec.py
# Compiled at: 2019-01-06 07:57:07
# Size of source mod 2**32: 6990 bytes
import numpy as np, pandas as pd
from anomaly_detection.anomaly_detect_ts import _detect_anoms

def __verbose_if(condition, args, kwargs=None):
    if condition:
        print(args, kwargs)


def anomaly_detect_vec(x, max_anoms=0.1, direction='pos', alpha=0.05, period=None, only_last=False, threshold=None, e_value=False, longterm_period=None, plot=False, y_log=False, xlabel='', ylabel='count', title='', verbose=False):
    if not isinstance(x, pd.Series):
        raise AssertionError('x must be pandas series')
    else:
        if not max_anoms < 0.5:
            raise AssertionError('max_anoms must be < 0.5')
        elif not direction in ('pos', 'neg', 'both'):
            raise AssertionError('direction should be one of "pos", "neg", "both"')
        assert period, 'Period must be set to the number of data points in a single period'
    __verbose_if((alpha < 0.01 or alpha > 0.1) and verbose, 'Warning: alpha is the statistical significance, and is usually between 0.01 and 0.1')
    max_anoms = 1.0 / x.size if max_anoms < 1.0 / x.size else max_anoms
    step = int(np.ceil(x.size / longterm_period)) if longterm_period else x.size
    all_data = [x.iloc[i:i + step] for i in range(0, x.size, step)]
    one_tail = True if direction in ('pos', 'neg') else False
    upper_tail = True if direction in ('pos', 'both') else False
    all_anoms = pd.Series()
    seasonal_plus_trend = pd.Series()
    for ts in all_data:
        tmp = _detect_anoms(ts,
          k=max_anoms, alpha=alpha, num_obs_per_period=period, use_decomp=True, use_esd=False,
          direction=direction,
          verbose=verbose)
        s_h_esd_timestamps = tmp['anoms'].keys()
        data_decomp = tmp['stl']
        anoms = ts.loc[s_h_esd_timestamps]
        if threshold:
            end = longterm_period - 1 if longterm_period else x.size - 1
            periodic_maxs = [ts.iloc[i:i + period].max() for i in range(0, end, period)]
            if threshold == 'med_max':
                thresh = periodic_maxs.median()
            else:
                if threshold == 'p95':
                    thresh = periodic_maxs.quantile(0.95)
                else:
                    if threshold == 'p99':
                        thresh = periodic_maxs.quantile(0.99)
            anoms = anoms[(anoms >= thresh)]
            all_anoms.append(anoms)
            seasonal_plus_trend.append(data_decomp)

    all_anoms.drop_duplicates(inplace=True)
    seasonal_plus_trend.drop_duplicates(inplace=True)
    return anoms