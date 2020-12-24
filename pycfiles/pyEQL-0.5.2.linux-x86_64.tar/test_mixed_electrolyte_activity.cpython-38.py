# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_mixed_electrolyte_activity.py
# Compiled at: 2020-04-22 00:43:16
# Size of source mod 2**32: 6112 bytes
"""
pyEQL test suite for mixed electrolyte activity
===============================================

This file contains tests for the Effective Pitzer Model
implemented in pyEQL.

This test suite creates several mixed salt solutions and compares
pyEQL's calculations with experimental data for activity coefficients
and/or osmotic coefficients.

The Effective Pitzer Model is described in Mistry et al.
DOI: 10.1016/j.desal.2013.03.015

Experimental data for mixed electrolytes is obtained from Rodil et al.
DOI: 10.1021/je9004432

"""
import pyEQL, unittest

class Test_nano3_kno3_activity(unittest.TestCase, pyEQL.CustomAssertions):
    __doc__ = '\n    test mean activity coefficients in a NaNO3 + KNO3 mixture\n    ---------------------------------------------------------\n    Note that the values given in Table 3 of Rodil et al. are single-ion\n    activity coefficients that must be averaged (geometrically) to obtained\n    the mean values below\n\n    '

    def setUp(self):
        self.tol = 0.25

    def test_activity_Na_XNa_75(self):
        molality = [
         0.3997, 0.992, 1.584, 2.373]
        expected = [0.613, 0.5039, 0.4448, 0.3928]
        for item in range(len(molality)):
            s1 = pyEQL.Solution([
             [
              'Na+', str(0.75 * molality[item]) + 'mol/kg'],
             [
              'K+', str(0.25 * molality[item]) + 'mol/kg'],
             [
              'NO3-', str(molality[item]) + 'mol/kg']])
            result = s1.get_activity_coefficient('Na+').magnitude
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_activity_K_XNa_75(self):
        molality = [
         0.3997, 0.992, 1.584, 2.373]
        expected = [0.582, 0.4523, 0.3827, 0.3138]
        for item in range(len(molality)):
            s1 = pyEQL.Solution([
             [
              'Na+', str(0.75 * molality[item]) + 'mol/kg'],
             [
              'K+', str(0.25 * molality[item]) + 'mol/kg'],
             [
              'NO3-', str(molality[item]) + 'mol/kg']])
            result = s1.get_activity_coefficient('K+').magnitude
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_activity_Na_XNa_50(self):
        molality = [
         0.4005, 0.9926, 1.787, 2.384]
        expected = [0.6211, 0.5181, 0.4481, 0.4132]
        for item in range(len(molality)):
            s1 = pyEQL.Solution([
             [
              'Na+', str(0.5 * molality[item]) + 'mol/kg'],
             [
              'K+', str(0.5 * molality[item]) + 'mol/kg'],
             [
              'NO3-', str(molality[item]) + 'mol/kg']])
            result = s1.get_activity_coefficient('Na+').magnitude
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_activity_K_XNa_50(self):
        molality = [
         0.4005, 0.9926, 1.787, 2.384]
        expected = [0.582, 0.4529, 0.3635, 0.3133]
        for item in range(len(molality)):
            s1 = pyEQL.Solution([
             [
              'Na+', str(0.5 * molality[item]) + 'mol/kg'],
             [
              'K+', str(0.5 * molality[item]) + 'mol/kg'],
             [
              'NO3-', str(molality[item]) + 'mol/kg']])
            result = s1.get_activity_coefficient('K+').magnitude
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_activity_Na_XNa_25(self):
        molality = [
         0.4021, 0.9976, 1.794, 2.393]
        expected = [0.6293, 0.5327, 0.468, 0.4364]
        for item in range(len(molality)):
            s1 = pyEQL.Solution([
             [
              'Na+', str(0.25 * molality[item]) + 'mol/kg'],
             [
              'K+', str(0.75 * molality[item]) + 'mol/kg'],
             [
              'NO3-', str(molality[item]) + 'mol/kg']])
            result = s1.get_activity_coefficient('Na+').magnitude
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_activity_K_XNa_25(self):
        molality = [
         0.4021, 0.9976, 1.794, 2.393]
        expected = [0.5942, 0.4731, 0.3878, 0.337]
        for item in range(len(molality)):
            s1 = pyEQL.Solution([
             [
              'Na+', str(0.25 * molality[item]) + 'mol/kg'],
             [
              'K+', str(0.75 * molality[item]) + 'mol/kg'],
             [
              'NO3-', str(molality[item]) + 'mol/kg']])
            result = s1.get_activity_coefficient('K+').magnitude
            self.assertWithinExperimentalError(result, expected[item], self.tol)


if __name__ == '__main__':
    unittest.main()