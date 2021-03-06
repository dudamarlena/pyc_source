# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/qnpct.py
# Compiled at: 2013-10-03 04:23:38
"""
qnpct
-----

This module provides some facilities for Quick prototyping
with NumPy and CTypes

mw@eml.cc 2013

"""
import time
from ctypes import *
from numpy import *

class arrays(object):
    """
    A simple context manager which handles any number of keyword 
    arguments and exposes as attributes ctypes c_voidp's for the
    ctypes.data attribute of the contiguous version of the array.

    >>> bar = rand(100)
    >>> lib = CDLL('./foo.so')
    >>> with arrays(bar=bar) as ar:
            lib.baz(bar, 3, 2.3)
    >>> ar.toc 
    2.2349

    This is for convenience and rapid(er) prototyping & testing
    of C code and numerical arrays.

    """

    def __init__(self, **kwd):
        for k, v in kwd.iteritems():
            setattr(self, k + '_c', ascontiguousarray(v))
            setattr(self, k, c_voidp(getattr(self, k + '_c').ctypes.data))

    def __enter__(self, *args):
        self.tic = time.time()
        return self

    def __exit__(self, *args):
        self.toc = time.time()