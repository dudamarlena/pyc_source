# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.5-intel-2.7/FXrays/test.py
# Compiled at: 2017-01-18 15:05:06
import doctest
from . import _test

def runtests():
    return doctest.testmod(_test)


if __name__ == '__main__':
    runtests()