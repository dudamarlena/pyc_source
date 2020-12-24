# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/stats.py
# Compiled at: 2014-11-14 02:28:16
# Size of source mod 2**32: 502 bytes
from __future__ import division
import math
__all__ = [
 'divide', 'mean', 'sum']

def divide(num, denom):
    if denom != 0:
        return num / denom
    else:
        return 0


def mean(iterable):
    result = 0
    total = 0
    for value in iterable:
        if value is None:
            pass
        else:
            result += value
            total += 1

    return divide(result, total)


def sum(iterable):
    result = 0
    for value in iterable:
        if value is None:
            pass
        else:
            result += value

    return result