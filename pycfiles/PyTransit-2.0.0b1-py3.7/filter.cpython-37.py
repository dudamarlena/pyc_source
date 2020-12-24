# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/contamination/filter.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 3208 bytes
from numpy import array, ones_like, zeros_like, diff, arange
from scipy.interpolate import interp1d

class Filter:

    def __init__(self, name):
        self.name = name

    def __call__(self, wl):
        return NotImplementedError


class ClearFilter(Filter):
    __doc__ = 'Constant unity transmission.\n\n    '

    def __call__(self, wl):
        return ones_like(wl).astype('d')


class BoxcarFilter(Filter):
    __doc__ = 'Filter with a transmission of 1 inside the minimum and maximum wavelengths and 0 outside.\n    '

    def __init__(self, name, wl_min, wl_max):
        super().__init__(name)
        self.wl_min = wl_min
        self.wl_max = wl_max

    def __call__(self, wl):
        w = zeros_like(wl)
        w[(wl > self.wl_min) & (wl < self.wl_max)] = 1.0
        return w


class TabulatedFilter(Filter):
    __doc__ = 'Interpolated tabulated filter.\n    '

    def __init__(self, name, wl, tm):
        super().__init__(name)
        self.wl = array(wl)
        self.tm = array(tm)
        assert self.wl.size == self.tm.size, 'The wavelength and transmission arrays must be of same size'
        assert all(diff(self.wl) > 0.0), 'Wavelength array must be monotonously increasing'
        assert all((self.tm >= 0.0) & (self.tm <= 1.0)), 'Transmission must always be between 0.0 and 1.0'
        self._ip = interp1d((self.wl), (self.tm), kind='cubic')

    def __call__(self, wl):
        return self._ip(wl)


sdss_g = BoxcarFilter("g'", 400, 550)
sdss_r = BoxcarFilter("r'", 570, 690)
sdss_i = BoxcarFilter("i'", 710, 790)
sdss_z = BoxcarFilter("z'", 810, 900)
kepler = TabulatedFilter('kepler', arange(350, 960, 25), array([0.0, 0.001, 0.0, 0.056, 0.465, 0.536, 0.624, 0.663,
 0.681, 0.715, 0.713, 0.696, 0.67, 0.649, 0.616, 0.574,
 0.541, 0.49, 0.468, 0.4, 0.332, 0.279, 0.02, 0.0,
 0.0]))
__all__ = 'Filter TabulatedFilter BoxcarFilter sdss_g sdss_r sdss_i sdss_z kepler'.split()