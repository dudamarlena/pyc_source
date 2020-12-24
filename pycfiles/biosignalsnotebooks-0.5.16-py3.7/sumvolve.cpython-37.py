# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\waves\sumvolve.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 243 bytes
from numpy import *

def sumvolve(x, window):
    lw = len(window)
    res = zeros(len(x) - lw, 'd')
    for i in range(len(x) - lw):
        res[i] = sum(abs(x[i:i + lw] - window)) / float(lw)

    return res