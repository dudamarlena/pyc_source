# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/walshb/camog/build/lib.linux-x86_64-2.7/camog/_csv.py
# Compiled at: 2017-11-15 03:36:24
import multiprocessing
from . import _cfastcsv

def load(filename, sep=',', headers=True, nthreads=None, flags=0):
    if nthreads is None:
        nthreads = multiprocessing.cpu_count()
    elif nthreads <= 0:
        raise ValueError('Invalid nthreads %s' % nthreads)
    return _cfastcsv.parse_file(filename, sep, nthreads, flags, 1 if headers else 0)