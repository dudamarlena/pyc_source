# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/helpers.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 588 bytes
__doc__ = '\nHelper functions.\n\n@author: anze.vavpetic@ijs.si\n'
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