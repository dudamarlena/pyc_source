# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/utils/stats.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import numpy

def mean(values):
    ret = None
    if len(values):
        ret = numpy.array(values).mean()
    return ret


def stddev(values, ddof=1):
    ret = None
    if len(values):
        ret = numpy.array(values).std(ddof=ddof)
    return ret