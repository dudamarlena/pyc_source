# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/_util.py
# Compiled at: 2014-09-16 14:39:13
import math

def deg2rad(deg):
    return deg * math.pi / 180.0


def rad2deg(rad):
    return rad * 180.0 / math.pi