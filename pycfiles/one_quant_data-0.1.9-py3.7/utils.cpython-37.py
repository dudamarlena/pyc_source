# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/one_quant_data/utils.py
# Compiled at: 2019-10-11 23:46:09
# Size of source mod 2**32: 1943 bytes
import datetime, sys, pandas as pd
from multiprocessing import Process
import psutil, gc, os

def show_sys_mem(info):
    gc.collect()
    rss = psutil.Process(os.getpid()).memory_info().rss
    data = psutil.virtual_memory()
    total = data.total
    free = data.available
    print('|{}| mem usage:{}G({}%)'.format(info, int(rss / 1024 / 1024 / 1024), rss / total * 100))


def get_func_name():
    try:
        raise Exception
    except:
        exc_info = sys.exc_info()
        traceObj = exc_info[2]
        frameObj = traceObj.tb_frame
        Upframe = frameObj.f_back
        return '{}'.format(Upframe.f_code.co_name)


def change(x, y):
    return round(float((y - x) / x * 100), 2)


def format_price(df, price=0, suffix=''):
    if price == 0:
        price = float(df.tail(1)[('close' + suffix)])
    for col in ('open', 'close', 'high', 'low'):
        df[col + suffix] = df[(col + suffix)] / price

    return (
     df, price)


def format_volume(df, volume=0, suffix=''):
    if volume == 0:
        volume = float(df.tail(1)[('volume' + suffix)])
    for col in ('volume', ):
        df[col + suffix] = df[(col + suffix)] / volume

    return (
     df, volume)


def format_date_ts_pro(date):
    if isinstance(date, str):
        return date.replace('-', '')
    return date


def date_delta(date, delta):
    if date.find('-') == -1:
        date_format = '%Y%m%d'
    else:
        date_format = '%Y-%m-%d'
    t = datetime.datetime.strptime(date, date_format)
    if delta > 0:
        t = t + datetime.timedelta(delta)
    else:
        t = t - datetime.timedelta(-delta)
    return t.strftime(date_format)