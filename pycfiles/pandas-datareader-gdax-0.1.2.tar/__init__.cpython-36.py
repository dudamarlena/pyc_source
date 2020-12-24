# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/pandas-datareader-gdax/src/pandas_datareader_gdax/__init__.py
# Compiled at: 2017-11-20 23:26:54
# Size of source mod 2**32: 1613 bytes
import pandas as pd, numpy as np, gdax
from datetime import datetime, timedelta
from time import sleep

def get_data_gdax(product, granularity=1800, start=datetime.now() - timedelta(days=1), end=datetime.now(), delay=1):
    public_client = gdax.PublicClient()
    data_frames = []
    step = timedelta(seconds=(granularity * 200))
    periods = (end - start).total_seconds() / granularity
    period_start = start
    if granularity * 200 > (end - start).total_seconds():
        period_end = end
    else:
        period_end = start + step
    while period_end <= end:
        records = public_client.get_product_historic_rates(product, granularity=granularity, start=(period_start.isoformat()), end=(period_end.isoformat()))
        if not isinstance(records, list):
            raise TypeError('Instance is not a list: %s' % records)
        sleep(delay)
        period_start += step
        period_end += step
        if period_end > end:
            if period_start < end:
                period_end = end
        if not records:
            pass
        else:
            records = np.array(records)
            df = pd.DataFrame((records[:, 1:]), index=(records[:, 0]), columns=['Low', 'High', 'Open', 'Close', 'Volume'])
            df.index = pd.to_datetime((pd.to_numeric(df.index)), utc=True, unit='s')
            df = df.sort_index(ascending=True)
            data_frames.append(df)

    return pd.concat(data_frames)