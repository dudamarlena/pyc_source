# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/tests/test_iii_v_zinc_blende_ternary.py
# Compiled at: 2015-04-09 03:43:25
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import iii_v_zinc_blende_ternaries, GaAs, AlAs, AlGaAs, GaAsSb, AlPAs, GaInAs
from openbandparams import *
import unittest

class TestIIIVZincBlendeTernary(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(AlGaAs), 'AlGaAs')
        self.assertEqual(str(GaAsSb), 'GaAsSb')

    def test_repr(self):
        for ternary in iii_v_zinc_blende_ternaries:
            self.assertEqual(eval(repr(ternary)), ternary)
            self.assertEqual(eval(repr(ternary(x=0))), ternary(x=0))
            self.assertEqual(eval(repr(ternary(x=1))), ternary(x=1))
            self.assertEqual(eval(repr(ternary(x=0.1))), ternary(x=0.1))

    def test_latex(self):
        self.assertEqual(AlGaAs.latex(), 'Al_{x}Ga_{1-x}As')
        self.assertEqual(AlGaAs(x=0.1).latex(), 'Al_{0.1}Ga_{0.9}As')
        self.assertEqual(AlGaAs(Al=0.1).latex(), 'Al_{0.1}Ga_{0.9}As')
        self.assertEqual(AlGaAs(Ga=0.9).latex(), 'Al_{0.1}Ga_{0.9}As')
        self.assertEqual(AlPAs.latex(), 'AlP_{x}As_{1-x}')
        self.assertEqual(AlPAs(x=0.1).latex(), 'AlP_{0.1}As_{0.9}')
        self.assertEqual(AlPAs(P=0.1).latex(), 'AlP_{0.1}As_{0.9}')
        self.assertEqual(AlPAs(As=0.9).latex(), 'AlP_{0.1}As_{0.9}')

    def test_eq(self):
        self.assertEqual(AlGaAs, AlGaAs)
        self.assertNotEqual(AlGaAs, GaInAs)
        self.assertEqual(AlGaAs(x=0), AlGaAs(Al=0))
        self.assertEqual(AlGaAs(x=0), AlGaAs(Ga=1))
        self.assertEqual(AlGaAs(Al=0), AlGaAs(Ga=1))
        self.assertEqual(AlPAs(x=0), AlPAs(P=0))
        self.assertEqual(AlPAs(x=0), AlPAs(As=1))
        self.assertEqual(AlPAs(P=0), AlPAs(As=1))

    def test_missing_x(self):
        with self.assertRaises(TypeError):
            AlGaAs.Eg()

    def test_Eg(self):
        self.assertEqual(AlGaAs(x=0).Eg(), GaAs.Eg())
        self.assertEqual(AlGaAs(x=1).Eg(), AlAs.Eg())


if __name__ == '__main__':
    unittest.main()