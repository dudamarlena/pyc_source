# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_graphics.py
# Compiled at: 2019-11-29 15:47:37
# Size of source mod 2**32: 562 bytes
import xarray as xr
from pivpy import io, pivpy, graphics
import numpy as np, os
f1 = 'Run000001.T000.D000.P000.H001.L.vec'
path = os.path.join(os.path.dirname(__file__), '../pivpy/data')
_d = io.load_vec(os.path.join(path, f1))

def test_showscal():
    graphics.showscal(_d, property='ke')


def test_quiver():
    graphics.quiver(_d)


def test_xarray_plot():
    _d.piv.vec2scal(property='curl')
    _d['w'].isel(t=0).plot.pcolormesh()


def test_histogram():
    graphics.histogram(_d)