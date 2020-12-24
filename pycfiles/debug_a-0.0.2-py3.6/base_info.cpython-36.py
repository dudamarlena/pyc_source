# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\collector\base_info.py
# Compiled at: 2018-05-12 01:04:31
# Size of source mod 2**32: 183 bytes
"""
基础数据接口
===================================
"""
import tushare as ts

def market_basic():
    return ts.get_stock_basics()