# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\common\math.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = 'math functions\n\nCopyright (C) 2011 Dan Meliza <dan // meliza.org>\nCreated 2011-08-10\n'
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