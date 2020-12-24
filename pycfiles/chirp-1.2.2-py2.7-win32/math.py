# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\common\math.py
# Compiled at: 2013-12-11 23:17:46
"""math functions

Copyright (C) 2011 Dan Meliza <dan // meliza.org>
Created 2011-08-10
"""
from numpy import frompyfunc

def _decibels(x, mindB=0.0):
    """ Convert from linear scale to decibels safely """
    from numpy import log10, power
    thresh = power(10.0, 0.1 * mindB)
    if x > thresh:
        return log10(x) * 10.0
    return mindB


decibels = frompyfunc(_decibels, 1, 1)

def nandecibels(x):
    """ Converts linear scale to decibels, without raising errors """
    from numpy import where, log10, nan
    return where(x > 0, log10(x) * 10, nan)