# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/query.py
# Compiled at: 2017-02-06 06:54:43
# Size of source mod 2**32: 1678 bytes
import collections, pandas as pd
from stock import models, signals, charts, util

def get(quandl_code, price_type='close', from_date=None, to_date=None, chart_type=None):
    quandl_code = quandl_code.upper().strip()
    if from_date:
        from_date = util.str2date(from_date)
    if to_date:
        to_date = util.str2date(to_date)
    Price = models.Price
    session = models.Session()
    query = session.query(Price).filter_by(quandl_code=quandl_code)
    if from_date:
        query = query.filter(Price.date >= from_date)
    if to_date:
        query = query.filter(Price.date <= to_date)
    df = pd.read_sql(query.statement, query.session.bind, index_col='date')
    if price_type is None:
        return df
    series = getattr(df, price_type)
    if chart_type:
        f = getattr(charts, chart_type)
        series = f(series)
    session.close()
    return series


def quandl_codes():
    session = models.Session()
    codes = [p[0] for p in session.query(models.Price.quandl_code).distinct().all()]
    session.close()
    return codes


def signal(signal=None, *args, **kw):
    if signal is None:
        signal = 'rolling_mean'
    result = collections.defaultdict(list)
    for code in quandl_codes():
        series = get(code, **kw)
        f = getattr(signals, signal)
        buy_or_sell = f(series, *args)
        if buy_or_sell:
            result[buy_or_sell].append(code)

    return result


def predict(quandl_code, *args, **kw):
    df = get(quandl_code, price_type=None, **kw)
    return signals.predict(df)