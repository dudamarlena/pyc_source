# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/tests/test_basic.py
# Compiled at: 2015-09-29 17:11:27
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from obpds import *
from obpds.tests.obpds_test_case import OBPDSTestCase
import unittest

class TestBasic(OBPDSTestCase):
    """
    Tests basic functionality
    """

    def test_pn_diode_default(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        n = Layer(1 * um, GaAs, -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, n])
        s = d.get_flatband()
        s = d.get_equilibrium()

    def test_pn_diode_boltzmann(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        n = Layer(1 * um, GaAs, -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, n])
        s = d.get_flatband()
        s = d.get_equilibrium(approx='boltzmann')

    def test_pn_diode_parabolic(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        n = Layer(1 * um, GaAs, -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, n])
        s = d.get_flatband()
        s = d.get_equilibrium(approx='parabolic')

    def test_pn_diode_kane(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        n = Layer(1 * um, GaAs, -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, n])
        s = d.get_flatband()
        s = d.get_equilibrium(approx='kane')

    def test_pn_hj_diode(self):
        p = Layer(1 * um, GaAs, 1e+17 / cm3)
        N = Layer(1 * um, AlGaAs(Al=0.3), -1e+17 / cm3)
        d = TwoTerminalDevice(layers=[p, N])
        s = d.get_flatband()
        s = d.get_equilibrium()


if __name__ == '__main__':
    unittest.main()