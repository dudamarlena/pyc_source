# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/cli/calc.py
# Compiled at: 2017-01-29 09:27:43
# Size of source mod 2**32: 2307 bytes
import click, pandas as pd
from .main import cli, mkdate, AliasedGroup
from stock import models, signals

def get(quandl_code, price_type, from_date=None, to_date=None):
    Price = models.Price
    session = models.Session()
    query = session.query(Price).filter_by(quandl_code=quandl_code)
    if from_date:
        query = query.filter(Price.date >= from_date)
    if to_date:
        query = query.filter(Price.date <= to_date)
    df = pd.read_sql(query.statement, query.session.bind, index_col='date')
    series = getattr(df, price_type)
    return series


@cli.group(cls=AliasedGroup)
def calc():
    pass


@calc.command(name='do')
@click.argument('quandl_code', default='NIKKEI/INDEX')
@click.option('-t', '--price-type', default='close')
@click.option('-s', '--start', callback=mkdate)
@click.option('-e', '--end', callback=mkdate)
@click.option('-m', '--method', default='macd')
def do(quandl_code, price_type, start, end, method):
    series = get(quandl_code, price_type)
    series = series.ix[start:end]
    ret = RollingMean(series).simulate()
    print(ret)


def s(quandl_code='NIKKEI/INDEX', price_type='close', way=None, lostcut=3, start=None, end=None, **kw):
    r = 0
    df = None
    lists = [
     MACD(series)] + [RollingMean(series, i) for i in range(1, 10)]
    for l in lists:
        df_result = l.simulate_action()
        if df_result.empty:
            pass
        else:
            accumulation = df_result.ix[(-1)].accumulation
            if r < accumulation:
                r = max(r, accumulation)
                df = l

    return (
     r, df)


@calc.command(name='signal')
@click.argument('quandl_code', default='NIKKEI/INDEX')
@click.option('-t', '--price-type', default='close')
@click.option('-s', '--signal', default='rolling_mean')
def check_signal(quandl_code, price_type, signal):
    series = service.get(quandl_code, price_type)
    method = getattr(signals, signal)
    result = method(series=series)
    if result:
        click.secho(result)
        return result