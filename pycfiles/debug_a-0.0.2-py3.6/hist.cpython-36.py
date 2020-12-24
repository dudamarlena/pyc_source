# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\collector\hist.py
# Compiled at: 2018-05-12 01:04:31
# Size of source mod 2**32: 378 bytes
"""
历史数据接口
=======================================================================================
"""
import tushare as ts

def hist_market(date):
    """历史行情数据

    :param date: str: 指定日期，如 "2018-03-19"
    :return:
    """
    hm = ts.get_day_all(date)
    hm['date'] = date
    return hm