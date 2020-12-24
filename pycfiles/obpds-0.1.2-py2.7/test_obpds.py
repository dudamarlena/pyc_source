# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/tests/test_obpds.py
# Compiled at: 2015-11-15 13:26:58
if __name__ == '__main__':
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from obpds import *
import unittest

class TestBasics(unittest.TestCase):
    """
    Tests basic functionality
    """

    def _get_pn_diode(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        n = Layer(1 * um, GaAs, -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, n], Fp='left', Fn='right')
        return d

    def test_pn_diode_default(self):
        d = self._get_pn_diode()
        s = d.get_flatband()
        s = d.get_equilibrium()

    def test_pn_diode_boltzmann(self):
        d = self._get_pn_diode()
        s = d.get_flatband()
        s = d.get_equilibrium(approx='boltzmann')

    def test_pn_diode_parabolic(self):
        d = self._get_pn_diode()
        s = d.get_flatband()
        s = d.get_equilibrium(approx='parabolic')

    def test_pn_diode_kane(self):
        d = self._get_pn_diode()
        s = d.get_flatband()
        s = d.get_equilibrium(approx='kane')

    def test_get_cv(self):
        d = self._get_pn_diode()
        s = d.get_cv(-5, 1, N=10)

    def test_pn_hj_diode(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        N = Layer(1 * um, AlGaAs(Al=0.3), -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, N], Fp='left', Fn='right')
        s = d.get_flatband()
        s = d.get_equilibrium()


if __name__ == '__main__':
    unittest.main()