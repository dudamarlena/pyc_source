# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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