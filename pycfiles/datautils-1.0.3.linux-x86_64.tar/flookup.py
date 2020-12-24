# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/np/flookup.py
# Compiled at: 2013-12-13 14:50:04
"""
Code to lookup useful functions by name
"""
import numpy
from . import convert

def finite(v):
    return numpy.array(v)[numpy.isfinite(v)]


def finitemean(v):
    return numpy.mean(finite(v))


def finitestd(v):
    return numpy.std(finite(v))


def stderr(v):
    return finitestd(v) / numpy.sqrt(len(finite(v)))


fs = {'code': convert.code, 
   'codes': numpy.unique, 
   'finite': finite, 
   'finitemean': finitemean, 
   'finitestd': finitestd, 
   'stderr': stderr, 
   'len': len}

class FunctionLookupError(Exception):
    pass


def lookup(n):
    if n in fs:
        return fs[n]
    if hasattr(numpy, n):
        return getattr(numpy, n)
    raise FunctionLookupError