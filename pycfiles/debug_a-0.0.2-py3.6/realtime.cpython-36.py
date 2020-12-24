# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\collector\realtime.py
# Compiled at: 2018-06-02 23:42:01
# Size of source mod 2**32: 3656 bytes
"""
盘中实时数据接口
=======================================================================================
"""
import tushare as ts
from datetime import datetime
from retrying import retry

@retry(stop_max_attempt_number=6)
def ticks(code, source='spider', date=datetime.now().date().__str__()):
    """返回date日期的分笔数据

    :param source:
    :param code: str: 股票代码，如 603655
    :param date: str: 日期，如 2018-03-15
    :return:
    """
    TODAY = datetime.now().date().__str__()

    def _unify_out(ticks, date):
        ticks = ticks[['time', 'price', 'volume', 'type']]
        ticks['datetime'] = ticks['time'].apply(lambda x: datetime.strptime(date + ' ' + x, '%Y-%m-%d %H:%M:%S'))
        ticks['vol'] = ticks['volume']
        type_convert = {'买盘':0, 
         '卖盘':1, 
         '中性盘':2, 
         '0':2}
        ticks['type'] = ticks['type'].apply(lambda x: type_convert[x])
        ticks.drop(['time', 'volume'], axis=1, inplace=True)
        ticks.sort_values('datetime', inplace=True)
        ticks.reset_index(drop=True, inplace=True)
        return ticks[['datetime', 'price', 'vol', 'type']]

    if source == 'spider':
        if date == TODAY:
            ticks = ts.get_today_ticks(code=code)
            ticks = _unify_out(ticks, date=TODAY)
    elif source == 'spider':
        if date != TODAY:
            ticks = ts.get_tick_data(code=code, date=date)
            ticks = _unify_out(ticks, date=date)
    else:
        ticks = ts.tick(code=code, conn=cons, date=date)
    return ticks


def get_price(code):
    """获取一只股票的最新价格"""
    data = ts.get_realtime_quotes(code)
    return float(data.loc[(0, 'price')])


def bars(codes):
    """获取codes的实时quotes"""
    return ts.get_realtime_quotes(codes)


def klines(code, freq='D', start_date=None):
    """获取K线数据

    :param start_date:
    :param code:
    :param freq: 可选值 D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
    :return: pd.DataFrame
    """
    if start_date is None:
        data = ts.get_k_data(code=code, ktype=freq)
    else:
        data = ts.get_k_data(code=code, start=start_date, ktype=freq)
    return data


def filter_tp(tm):
    """停盘股过滤

    :param tm: return of function today_market
    :return:
    """
    tm1 = tm[(tm['volume'] != 0.0)]
    tm1.reset_index(drop=True, inplace=True)
    return tm1


def filter_st(tm):
    """ST股过滤

    :param tm: return of function today_market
    :return:
    """
    fst = tm['name'].apply(lambda x: True if 'ST' not in x else False)
    tm1 = tm[fst]
    tm1.reset_index(drop=True, inplace=True)
    return tm1


@retry(stop_max_attempt_number=6)
def today_market(filters=['tp']):
    """返回最近一个交易日所有股票的交易数据

    :param filters: list:需要应用的过滤规则，可选 "tp"、"st"
    :return:
    """
    tm = ts.get_today_all()
    if filters is None:
        return tm
    else:
        filters = [x.lower() for x in filters]
        if 'tp' in filters:
            tm = filter_tp(tm)
        if 'st' in filters:
            tm = filter_st(tm)
        return tm


@retry(stop_max_attempt_number=6)
def market_basic():
    """返回A股所有股票的基础信息"""
    return ts.get_stock_basics()