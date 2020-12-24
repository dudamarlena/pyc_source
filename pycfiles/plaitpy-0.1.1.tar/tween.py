# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okay/tonka/src/plait.py/src/tween.py
# Compiled at: 2018-01-04 14:34:08
import math

def linear(t):
    if t > 0.5:
        return (1 - t) * 2
    else:
        return t * 2


def sin(t):
    return abs(math.sin(t * math.pi))