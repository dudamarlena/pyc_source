# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\utils\stats.py
# Compiled at: 2019-06-05 03:26:22
# Size of source mod 2**32: 956 bytes
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