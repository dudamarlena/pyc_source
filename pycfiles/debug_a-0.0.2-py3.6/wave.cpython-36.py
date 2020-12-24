# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\selector\wave.py
# Compiled at: 2018-05-12 01:04:32
# Size of source mod 2**32: 652 bytes
"""
根据波动大小选股
=============================================
"""
from datetime import datetime
from debug_a.collector.realtime import klines
code = '603655'
code = '600122'

def wave(code):
    data = klines(code)
    data = data.iloc[0:5]
    data['wave_rate'] = (data['high'] - data['low']) / data['open']
    avg_wr = sum(data['wave_rate']) / len(data)
    avg_tor = sum(data['tor']) / len(data)
    return {'code':code, 
     '5日平均波动':avg_wr, 
     '5日平均换手':avg_tor / 100}