# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_NASA_coeff.py
# Compiled at: 2017-12-10 23:47:59
# Size of source mod 2**32: 1249 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from kinetics import nasa

class test_NASA_Coeff(unittest.TestCase):

    def test_NASA_coefficients(self):
        coeff = nasa.getNASACoeff('H', 300)
        self.assertEqual(coeff, [2.5, 7.05332819e-13, -1.99591964e-15, 2.30081632e-18, -9.27732332e-22, 25473.6599, -0.446682853])

    def test_NASA_coefficients_2(self):
        coeff = nasa.getNASACoeff('H2O', 1500)
        self.assertEqual(coeff, [3.03399249, 0.00217691804, -1.64072518e-07, -9.7041987e-11, 1.68200992e-14, -30004.2971, 4.9667701])

    def test_NASA_coefficients_LowTemp(self):
        self.assertRaises(Exception, nasa.getNASACoeff, 'H', 199)

    def test_NASA_coefficients_HighTemp(self):
        self.assertRaises(Exception, nasa.getNASACoeff, 'OH', 3501)

    def test_NASA_coefficients_UnknownSpecies(self):
        self.assertRaises(Exception, nasa.getNASACoeff, 'Ag', 1100)