# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_mixed_electrolyte_activity.py
# Compiled at: 2020-04-22 00:43:16
# Size of source mod 2**32: 6112 bytes
__doc__ = "\npyEQL test suite for mixed electrolyte activity\n===============================================\n\nThis file contains tests for the Effective Pitzer Model\nimplemented in pyEQL.\n\nThis test suite creates several mixed salt solutions and compares\npyEQL's calculations with experimental data for activity coefficients\nand/or osmotic coefficients.\n\nThe Effective Pitzer Model is described in Mistry et al.\nDOI: 10.1016/j.desal.2013.03.015\n\nExperimental data for mixed electrolytes is obtained from Rodil et al.\nDOI: 10.1021/je9004432\n\n"
import pyEQL, unittest

class Test_nano3_kno3_activity(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_nano3_kno3_activity"""

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