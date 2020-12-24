# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jake/.virtualenvs/python-dmc/lib/python2.7/site-packages/pybloof.py
# Compiled at: 2015-10-23 10:22:23
from __future__ import division
import operator, _pybloof
from math import ceil, log
LongBloomFilter = _pybloof.LongBloomFilter
StringBloomFilter = _pybloof.StringBloomFilter
UIntBloomFilter = _pybloof.UIntBloomFilter

def bloom_calculator(n, p):
    """
    Calculate the optimal bloom filter parameters for a given number of elements in filter (n) and false
    positive probability (p)
    """
    m = int(ceil(n * log(p) / log(1.0 / pow(2.0, log(2.0)))))
    k = int(log(2.0) * m / n)
    return {'size': m, 'hashes': k}