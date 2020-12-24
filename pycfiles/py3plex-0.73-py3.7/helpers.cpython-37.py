# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/helpers.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 588 bytes
"""
Helper functions.

@author: anze.vavpetic@ijs.si
"""
from math import sqrt
from .settings import W3C, HEDWIG

def avg(x):
    n = float(len(x))
    if n:
        return sum(x) / n
    return 0


def std(x):
    n = float(len(x))
    if n:
        return sqrt((sum((i * i for i in x)) - sum(x) ** 2 / n) / n)
    return 0


def user_defined(uri):
    """
    Is this resource user defined?
    """
    return not uri.startswith(W3C) and not uri.startswith(HEDWIG) and not anonymous_uri(uri)


def anonymous_uri(uri):
    return not uri.startswith('http')