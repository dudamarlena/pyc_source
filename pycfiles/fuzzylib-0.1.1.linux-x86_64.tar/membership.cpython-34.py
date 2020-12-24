# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzylib/membership.py
# Compiled at: 2015-09-29 17:24:14
# Size of source mod 2**32: 398 bytes


def triangular(x, a, b, c):
    if x < a:
        return 0
    else:
        if x < b:
            return (x - a) / (b - a)
        if x < c:
            return (c - x) / (c - b)
        return 0


def trapezoidal(x, a, b, c, d):
    if x < a:
        return 0
    else:
        if x < b:
            return (x - a) / (b - a)
        if x < c:
            return 1
        if x < d:
            return (d - x) / (d - c)
        return 0