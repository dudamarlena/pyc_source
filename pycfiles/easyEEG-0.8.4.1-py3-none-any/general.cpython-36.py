# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Coding\py\IPython Notebooks\experiment\chunking\lazyEEG\algorithms\general.py
# Compiled at: 2017-06-30 14:46:44
# Size of source mod 2**32: 1568 bytes
from ..default import *
from .. import parameter

def point_sample(df, step='1ms'):
    zdf = df['data']
    step = int(step[:-2]) // (1000 / parameter.sr)
    df = df.iloc[:, ::step]
    if type(df.columns) == pd.TimedeltaIndex:
        df.columns = [
         [
          'data'] * len(df.columns), df.columns]
    return df


def window_sample(df, window, sample='mean'):
    if type(df.columns) != pd.TimedeltaIndex:
        df = df['data']
    else:
        last_col_old = df.columns[(-1)]
        df = df.resample(window, axis=1, how=sample)
        df.columns = df.columns + pd.Timedelta(window) / 2
        last_col_new = df.columns[(-1)]
        if last_col_new > last_col_old:
            del df[last_col_new]
        if type(df.columns) == pd.TimedeltaIndex:
            df.columns = [
             [
              'data'] * len(df.columns), df.columns]
    return df


def subtract(data, index):
    part1 = data.xs('+', level=index)
    try:
        part2 = data.xs('-', level=index)
        result = part1.subtract(part2, fill_value=0)
    except:
        result = part1

    return result


def mean_axis(df, axis_to_mean):
    level = list(np.setdiff1d(df.index.names, axis_to_mean))
    return df.mean(level=level)