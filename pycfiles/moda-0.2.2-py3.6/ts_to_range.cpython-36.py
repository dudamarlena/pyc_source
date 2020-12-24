# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\moda\dataprep\ts_to_range.py
# Compiled at: 2018-10-31 09:33:17
# Size of source mod 2**32: 1909 bytes
import pandas as pd

def ts_to_range(ts, time_range='1H', pad_with_zeros=True):
    """
    Creates a new data frame with counts per time range
    :param ts: The original time series, with a column named 'date' and possibly an additional 'category' column
    :param time_range: The time range requested
    :param pad_with_zeros: Whether to add a value of 0 for missing dates (see Pandas resample).
    Note that this will split the time series into different categories (if categories exist), and pad each category
    independently. Then all time series will be appended together.
    :return: a pd.DataFrame with a MultiIndex containing a date and category. Contains an additional column with
    counts in the interval
    """
    if not isinstance(ts.index, pd.core.indexes.datetimes.DatetimeIndex):
        print('Wrong index type. Expecting pd.core.indexes.datetimes.DateTimeIndex')
        return
    else:
        if 'category' in ts:
            range_grp = ts.groupby([pd.Grouper(freq=time_range), 'category']).size().to_frame('value')
            range_grp = range_grp.reset_index(level='category')
            if pad_with_zeros:
                categories = range_grp['category'].unique()
                new_range_grp = pd.DataFrame()
                for cat in categories:
                    this_cat = range_grp[(range_grp['category'] == cat)]
                    this_cat = this_cat.resample(time_range, convention='start').asfreq().fillna(0)
                    this_cat['category'] = cat
                    new_range_grp = new_range_grp.append(this_cat, ignore_index=False)

                range_grp = new_range_grp.set_index(['category'], append=True).sort_index(0)
        else:
            range_grp = ts.groupby(pd.Grouper(freq=time_range)).size().to_frame('value')
        if pad_with_zeros:
            range_grp = range_grp.resample(time_range, convention='start').asfreq().fillna(0)
        return range_grp