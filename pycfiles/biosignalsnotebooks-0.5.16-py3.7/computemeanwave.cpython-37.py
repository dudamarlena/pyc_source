# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\waves\computemeanwave.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 423 bytes
from numpy import *

def computemeanwave(signal, events, fdist, lmin=0, lmax=0):
    if (lmin == 0) & (lmax == 0):
        lmax = mean(diff(events)) / 2
        lmin = -lmax
    w = waves(signal, events, lmin, lmax)
    w_ = meanwave(w)
    d = wavedistance(w_, w, fdist)
    ws = stdwave(w)
    return (
     w_, ws, d)