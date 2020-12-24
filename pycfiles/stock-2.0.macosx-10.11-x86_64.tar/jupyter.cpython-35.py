# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/jupyter.py
# Compiled at: 2017-01-29 05:04:09
# Size of source mod 2**32: 223 bytes
import matplotlib.pyplot as plt
from stock import query

def get(**kw):
    return query.get(**kw)


def show(**kw):
    series = get(**kw)
    plt.plot(series.index, series)


def drow():
    plt.figure(figsize=(15, 15))