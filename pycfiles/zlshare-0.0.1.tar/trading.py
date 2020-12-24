# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Code\Python\db_trans\zlshare\stock\trading.py
# Compiled at: 2019-01-22 02:15:42
"""
交易数据接口
Created on 2019/01/21
@author: luqy
@group : zealink
@contact: luqy@zealink.com
"""
from __future__ import division
from . import vars
import time, datetime, json
from zlshare.utils import netbase
import pandas as pd, logbook
log = logbook.Logger('stock')

def get_hist_data(code=None, start=None, end=None, ktype='D', retry_count=3, pause=0.001):
    u"""
        获取个股历史交易记录
    Parameters
    ------
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
    """
    dtstart = int('19700101') if start is None else int(start.replace('-', ''))
    dtend = int(datetime.datetime.now().strftime('%Y%m%d')) if end is None else int(end.replace('-', ''))
    if ktype in vars.K_LABELS:
        period = vars.K_LABELS[ktype]
        postdata = {'symbol': code, 
           'count': 10000, 
           'period': period}
        for _ in range(retry_count):
            try:
                res = netbase.Client(vars.K_URL, postdata)
                js = json.loads(res.gvalue())
                if js['code'] != 0:
                    raise ('api[{}] error.code={}').format(vars.K_URL, js['code'])
            except Exception as e:
                log.warning(str(e))
                time.sleep(pause)
            else:
                df = pd.DataFrame(data=js['data'], columns=['date', 'preclose', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
                df['price_change'] = df.close - df.preclose
                df['p_change'] = (df.close - df.preclose) * 100.0 / df.preclose
                for ma in [5, 10, 20]:
                    df['ma' + str(ma)] = df['close'].rolling(ma).mean()
                    df['v_ma' + str(ma)] = df['volume'].rolling(ma).mean()

                df = df.drop(columns=['preclose', 'turnover'])
                df = df[((df['date'] >= dtstart) & (df['date'] <= dtend))]
                df.date = df.date.apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
                df = df.set_index('date').sort_index(ascending=False)
                return df

        raise 'net work error'
    elif ktype in vars.K_MIN_LABELS:
        period = vars.K_MIN_LABELS[ktype]
        postdata = {'symbol': code, 
           'count': 10000, 
           'period': period}
        for _ in range(retry_count):
            try:
                res = netbase.Client(vars.K_MIN_URL, postdata)
                js = json.loads(res.gvalue())
                if js['code'] != 0:
                    raise ('api[{}] error.code={}').format(vars.K_URL, js['code'])
            except Exception as e:
                log.warning(str(e))
                time.sleep(pause)
            else:
                df = pd.DataFrame(data=js['data'], columns=[
                 'date', 'preclose', 'open', 'high', 'low', 'close', 'volume', 'turnover', 'time'])
                df['price_change'] = df.close - df.preclose
                df['p_change'] = (df.close - df.preclose) * 100.0 / df.preclose
                for ma in [5, 10, 20]:
                    df['ma' + str(ma)] = df['close'].rolling(ma).mean()
                    df['v_ma' + str(ma)] = df['volume'].rolling(ma).mean()

                df = df[((df['date'] >= dtstart) & (df['date'] <= dtend))]
                df.date = df.apply(lambda row: datetime.datetime.strptime(('{} {}').format(int(row['date']), int(row['time'])), '%Y%m%d %H%M'), axis=1)
                df = df.drop(columns=['preclose', 'turnover', 'time'])
                df = df.set_index('date').sort_index(ascending=False)
                return df

        raise 'net work error'
    else:
        raise ('unknow ktype = {}').format(ktype)
    return