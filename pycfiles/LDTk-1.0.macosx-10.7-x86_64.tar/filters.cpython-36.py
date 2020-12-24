# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hannu/soft/anaconda/envs/p36/lib/python3.6/site-packages/ldtk/filters.py
# Compiled at: 2017-09-18 11:22:47
# Size of source mod 2**32: 3562 bytes
"""
Limb darkening toolkit
Copyright (C) 2015  Hannu Parviainen <hpparvi@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
from numpy import array, argsort, zeros_like, arange, loadtxt, linspace
from scipy.interpolate import interp1d

class Filter(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, wl):
        raise NotImplementedError

    def plot(self, ax=None, wl_min=300, wl_max=1000, wl_res=500):
        from matplotlib.pyplot import subplots, setp
        if ax is None:
            fig, ax = subplots()
        wl = linspace(wl_min, wl_max, wl_res)
        ax.plot(wl, self(wl))
        setp(ax, xlabel='Wavelength [nm]', ylabel='Transmission')
        return ax


class TabulatedFilter(Filter):
    __doc__ = 'Tabulated filter where the transmission is\n       listed as a function of wavelength.\n    '

    def __init__(self, name, wl_or_fname, tm=None, tmf=1.0):
        """
        Parameters

        name        : str           filter name
        wl_or_fname : array or str  a list of wavelength or filename
        tm          : array         a list of transmission values
        tmf         : float         should be set to 1e-2 if the transmission is given in percents
        """
        super(TabulatedFilter, self).__init__(name)
        if isinstance(wl_or_fname, str):
            self.wl, self.tm = loadtxt(wl_or_fname).T
        else:
            self.wl = array(wl_or_fname)
            self.tm = array(tm)
        self.tm *= tmf
        sid = argsort(self.wl)
        self.wl = self.wl[sid]
        self.tm = self.tm[sid]
        self._ip = interp1d((self.wl), (self.tm), kind='cubic', bounds_error=False, fill_value=0.0)

    def __call__(self, wl):
        return self._ip(wl)


class BoxcarFilter(Filter):
    __doc__ = 'Boxcar filter.'

    def __init__(self, name, wl_min, wl_max):
        super(BoxcarFilter, self).__init__(name)
        self.wl_min = wl_min
        self.wl_max = wl_max

    def __call__(self, wl):
        w = zeros_like(wl)
        w[(wl > self.wl_min) & (wl < self.wl_max)] = 1.0
        return w


sdss_g = BoxcarFilter("g'", 400, 550)
sdss_r = BoxcarFilter("r'", 570, 690)
sdss_i = BoxcarFilter("i'", 710, 790)
sdss_z = BoxcarFilter("z'", 810, 900)
kepler = TabulatedFilter('kepler', arange(350, 960, 25), array([0.0, 0.001, 0.0, 0.056, 0.465, 0.536, 0.624, 0.663,
 0.681, 0.715, 0.713, 0.696, 0.67, 0.649, 0.616, 0.574,
 0.541, 0.49, 0.468, 0.4, 0.332, 0.279, 0.02, 0.0,
 0.0]))
__all__ = 'Filter TabulatedFilter BoxcarFilter sdss_g sdss_r sdss_i sdss_z kepler'.split()