# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\waves\plotheatmap.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 540 bytes
from pylab import *
from numpy import *
import novainstrumentation.waves.waves as waves
import novainstrumentation.waves.meanwave as meanwave

def plotheatmap(signal, events, lmin=0, lmax=0, dt=0.01, color='r'):
    w = waves(signal, events, lmin, lmax)
    w_ = meanwave(w)
    t_ = (arange(len(w_)) + lmin) * dt
    for iw in w:
        plot(t_, iw, lw=3, alpha=0.15, color=color)

    plot(t_, w_, lw=2, color='k')