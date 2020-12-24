# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/np/named.py
# Compiled at: 2013-12-13 14:50:04
import numpy

def add_column(arr, name, col, dtype=None):
    arr = numpy.asarray(arr)
    if dtype is None:
        dtype = col.dtype
    ndtype = numpy.dtype(arr.dtype.descr + [(name, dtype)])
    narr = numpy.empty(arr.shape, dtype=ndtype)
    for f in arr.dtype.fields:
        narr[f] = arr[f]

    narr[name] = col
    return narr