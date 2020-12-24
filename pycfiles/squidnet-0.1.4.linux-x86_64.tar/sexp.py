# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/squidnet/sexp.py
# Compiled at: 2010-04-07 16:51:20
try:
    from scexp import *
    SEXP_VERSION = 'C Module'
except ImportError:
    try:
        from csexp import *
        SEXP_VERSION = 'Cython Module'
    except ImportError:
        from pysexp import *
        SEXP_VERSION = 'Pure Python'