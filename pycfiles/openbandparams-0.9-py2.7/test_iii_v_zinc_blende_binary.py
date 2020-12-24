# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/tests/test_iii_v_zinc_blende_binary.py
# Compiled at: 2015-04-09 03:43:25
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import iii_v_zinc_blende_binaries, GaAs, InAs
from openbandparams import *
import unittest

class TestIIIVZincBlendeBinary(unittest.TestCase):

    def test_str(self):
        for binary in iii_v_zinc_blende_binaries:
            self.assertEqual(str(binary), binary.name)

    def test_repr(self):
        for binary in iii_v_zinc_blende_binaries:
            self.assertEqual(eval(repr(binary)), binary)

    def test_eq(self):
        self.assertEqual(GaAs, GaAs)
        self.assertNotEqual(GaAs, InAs)

    def test_a_300K(self):
        self.assertAlmostEqual(GaAs.a_300K(), 5.65325, places=5)

    def test_da_dT(self):
        self.assertAlmostEqual(GaAs.thermal_expansion(), 3.88e-05, places=7)

    def test_a(self):
        self.assertAlmostEqual(GaAs.a(), 5.65325, places=5)
        self.assertAlmostEqual(GaAs.a(T=301), 5.6532887999999994, places=7)

    def test_Eg_Gamma_0(self):
        self.assertAlmostEqual(GaAs.Eg_Gamma_0(), 1.519, places=3)

    def test_alpha_Gamma(self):
        self.assertAlmostEqual(GaAs.alpha_Gamma(), 0.0005405, places=7)

    def test_beta_Gamma(self):
        self.assertAlmostEqual(GaAs.beta_Gamma(), 204, places=0)

    def test_Eg_Gamma(self):
        self.assertAlmostEqual(GaAs.Eg_Gamma(), 1.42248214286, places=11)
        self.assertAlmostEqual(GaAs.Eg_Gamma(T=0), 1.519, places=3)

    def test_Eg_X_0(self):
        self.assertAlmostEqual(GaAs.Eg_X_0(), 1.981, places=3)

    def test_alpha_X(self):
        self.assertAlmostEqual(GaAs.alpha_X(), 0.00046, places=5)

    def test_beta_X(self):
        self.assertAlmostEqual(GaAs.beta_X(), 204, places=0)

    def test_Eg_X(self):
        self.assertAlmostEqual(GaAs.Eg_X(), 1.89885714286, places=11)
        self.assertAlmostEqual(GaAs.Eg_X(T=0), 1.981, places=3)

    def test_Eg_L_0(self):
        self.assertAlmostEqual(GaAs.Eg_L_0(), 1.815, places=3)

    def test_alpha_L(self):
        self.assertAlmostEqual(GaAs.alpha_L(), 0.000605, places=6)

    def test_beta_L(self):
        self.assertAlmostEqual(GaAs.beta_L(), 204, places=0)

    def test_Eg_L(self):
        self.assertAlmostEqual(GaAs.Eg_L(), 1.70696428571, places=11)
        self.assertAlmostEqual(GaAs.Eg_L(T=0), 1.815, places=3)

    def test_element_fraction(self):
        self.assertEqual(GaAs.element_fraction('Ga'), 1.0)
        self.assertEqual(GaAs.element_fraction('As'), 1.0)
        self.assertEqual(GaAs.element_fraction('In'), 0.0)
        self.assertEqual(InAs.element_fraction('Ga'), 0.0)
        self.assertEqual(InAs.element_fraction('As'), 1.0)
        self.assertEqual(InAs.element_fraction('In'), 1.0)

    def test_GaAs_Eg(self):
        self.assertAlmostEqual(GaAs.Eg(), 1.42248214286, places=11)
        self.assertAlmostEqual(GaAs.Eg(T=0), 1.519, places=3)

    def test_compressive_biaxial_strained(self):
        strain = 0.01
        unstrained = GaAs
        strained = GaAs.strained_001(strain)
        self.assert_(strained.strain_out_of_plane() == strain)
        self.assert_(strained.strain_in_plane() < 0)
        self.assert_(unstrained.a_c() < 0)
        self.assert_(unstrained.a_v() < 0)
        self.assert_(unstrained.b() < 0)
        self.assert_(strained.CBO_strain_shift() > 0)
        self.assert_(strained.VBO_hh_strain_shift() > 0)
        self.assert_(strained.VBO_lh_strain_shift() < 0)
        self.assert_(strained.VBO_strain_shift() > 0)
        self.assert_(strained.Eg_strain_shift() > 0)
        self.assert_(strained.Eg() > unstrained.Eg())

    def test_tensile_biaxial_strained(self):
        strain = -0.01
        unstrained = GaAs
        strained = GaAs.strained_001(strain)
        self.assert_(strained.strain_out_of_plane() == strain)
        self.assert_(strained.strain_in_plane() > 0)
        self.assert_(unstrained.a_c() < 0)
        self.assert_(unstrained.a_v() < 0)
        self.assert_(unstrained.b() < 0)
        self.assert_(strained.CBO_strain_shift() < 0)
        self.assert_(strained.VBO_hh_strain_shift() < 0)
        self.assert_(strained.VBO_lh_strain_shift() > 0)
        self.assert_(strained.VBO_strain_shift() > 0)
        self.assert_(strained.Eg_strain_shift() < 0)
        self.assert_(strained.Eg() < unstrained.Eg())


if __name__ == '__main__':
    unittest.main()