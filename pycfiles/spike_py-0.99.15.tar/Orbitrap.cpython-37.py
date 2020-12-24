# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Orbitrap.py
# Compiled at: 2020-02-19 16:37:47
# Size of source mod 2**32: 7252 bytes
"""
This file implements all the tools for handling Orbitrap data-sets

To use it :

import Orbitrap
d = Orbitrap.OrbiData(...)    # There are several possible initialisation : empty, from file
play with d

d will allows all NPKData methods, plus a few specific ones.

alternatively, use an importer :
from File.(Importer_name) import Import_1D
d = Import_1D("filename)")

Created by Marc-Andre' on 2014-09
Copyright (c) 2014 IGBMC. All rights reserved.
"""
from __future__ import print_function
import math, unittest, numpy as np
import File.HDF5File as HDF5File
from spike import NPKData
from spike import FTMS
from .NPKError import NPKError
FREQ0 = 10000000.0
REF_FREQ = 1887533.975611561
REF_MASS = 715.3122

class OrbiAxis(FTMS.FTMSAxis):
    __doc__ = '\n    hold information for one Orbitrap axis\n    used internally\n    '

    def __init__(self, itype=0, currentunit='points', size=1024, specwidth=1000000.0, offsetfreq=0.0, left_point=0.0, highmass=10000.0, calibA=0.0, calibB=100000000000000.0, calibC=0.0):
        """
        all parameters from Axis, plus
        specwidth   highest frequency,
        offsetfreq      carrier frequency in heterodyn or lowest frequency if acquisition does not contains 0.0,

        calibA, calibB, calibC : calibration constant, allowing 1 2 or 3 parameters calibration.
            set to zero if unused
            correspond to Bruker parameter ML1 ML2 ML3 for FTICR
            correspond to Thermo parameter  'Source Coeff1', 'Source Coeff2', 'Source Coeff3' for Orbitrap
        highmass    highest physical m/z of interest
        left_point  coordinates of first data point; usually 0.0 after Fourier Transform; may be different after extraction        
        currentunit default unit used for display and zoom,
            possible values for unit are "points" "m/z"
        
        conversion methods work on numpy arrays as well
        """
        super(OrbiAxis, self).__init__(itype=itype, currentunit=currentunit, size=size, specwidth=specwidth,
          offsetfreq=offsetfreq,
          left_point=left_point,
          highmass=highmass,
          calibA=calibA,
          calibB=calibB,
          calibC=calibC)
        self.Orbitrap = 'Orbitrap'
        self.kind = 'Orbitrap'
        self.calibA = calibA
        self.calibB = calibB
        self.calibC = calibC
        self.attributes.insert(0, 'Orbitrap')
        self.attributes.insert(0, 'calibA')
        self.attributes.insert(0, 'calibB')
        self.attributes.insert(0, 'calibC')

    def report(self):
        """high level reporting"""
        if self.itype == 0:
            return 'Orbitrap axis at %f kHz,  %d real points,  from mz = %8.3f   to m/z = %8.3f  M/DeltaM (M=400) = %.0f' % (
             self.specwidth / 1000, self.size, self.lowmass, self.highmass, 400.0 / self.deltamz(400.0))
        return 'Orbitrap axis at %f kHz,  %d complex pairs,  from mz = %8.3f   to m/z = %8.3f  M/DeltaM (M=400) = %.0f' % (
         self.specwidth / 1000, self.size / 2, self.lowmass, self.highmass, 400.0 / self.deltamz(400.0))

    def htomz(self, value):
        """
        return m/z (mz) from Hertz value (h)
        """
        v = np.maximum(value, 0.1)
        return self.calibA + self.calibB / v ** 2 + self.calibC / v ** 4

    def mztoh(self, value):
        """
        return Hz value (h) from  m/z (mz) 
        """
        v = np.maximum(value, 0.1)
        Delta = self.calibB ** 2 - 4 * self.calibC * (self.calibA - v)
        f2 = (-self.calibB - np.sqrt(Delta)) / (2 * (self.calibA - v))
        return np.sqrt(f2)


class OrbiData(FTMS.FTMSData):
    __doc__ = '\n    subclass of FTMS.FTMSData, meant for handling Orbitrap data\n    doc to be written ...\n    '

    def __init__(self, dim=1, shape=None, mode='memory', buffer=None, name=None, debug=0):
        self.axis1 = OrbiAxis()
        if dim == 2:
            raise Exception('2D Orbitrap is not physcally defined (yet ?)')
        elif name:
            if name.endswith('.msh5'):
                if debug > 0:
                    print('reading msh5')
                H = HDF5File(name, 'r')
                H.load(mode=mode)
                super(OrbiData, self).__init__(buffer=(H.data.buffer), debug=debug)
                NPKData.copyaxes(H.data, self)
                self.name = name
                self.hdf5file = H
            else:
                raise Exception('Filename should have a .msh5 extension')
        else:
            if debug > 0:
                print('calling super')
            super(OrbiData, self).__init__(dim=dim, shape=shape, buffer=buffer, name=name, debug=debug)
            for i in range(self.dim):
                axis = self.axes(i + 1)
                setattr(self, 'axis%d' % (i + 1), OrbiAxis(size=(axis.size), itype=0))

        if debug > 1:
            print(self.report())


class Orbi_Tests(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def test_atob(self):
        """testing unit conversion functions"""
        self.announce()
        Oaxis = OrbiAxis(size=1000, specwidth=1667000, itype=0, currentunit='points', calibB=60588995157584.56, highmass=2000.0)
        self.assertAlmostEqual(Oaxis.itoh(0), 0)
        self.assertAlmostEqual(Oaxis.itoh(Oaxis.size), Oaxis.specwidth)
        self.assertAlmostEqual((Oaxis.itomz(1023) / Oaxis.deltamz(Oaxis.itomz(1023))), 511.5, places=2)
        self.assertAlmostEqual(15129 * Oaxis.itomz(123), 103041 * Oaxis.itomz(321))
        self.assertAlmostEqual(123 * Oaxis.mztoi(123) ** 2, 321 * Oaxis.mztoi(321) ** 2)
        for i in (1, 2):
            print(Oaxis.report())
            print(Oaxis._report())
            for x in (1.0, 301.0, Oaxis.size - 20.0, Oaxis.size - 1.0):
                print('point at index %d is at freq %f, m/z %f' % (x, Oaxis.itoh(x), Oaxis.itomz(x)))
                self.assertAlmostEqual(Oaxis.mztoi(Oaxis.itomz(x)), x)
                self.assertAlmostEqual(Oaxis.itoh(Oaxis.htoi(x)), x)

            Oaxis.extract([300, Oaxis.size - 20])


if __name__ == '__main__':
    unittest.main()