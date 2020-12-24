# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_solute_properties.py
# Compiled at: 2020-04-21 21:02:06
# Size of source mod 2**32: 9876 bytes
__doc__ = '\npyEQL solute properties test suite\n============================================\n\nThis file contains tests of the Solution class methods that retrieve or\ncalculate properties of individual solutes. Methods currently included\nin the testing are:\n\n- get_transport_number()\n- get_molar_conductivity()\n- get_mobility()\n\n\n'
import pyEQL, unittest

class Test_transport_number(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_transport_number"""

    def setUp(self):
        self.s1 = pyEQL.Solution([
         [
          'K+', '0.1 mol/L'], ['Cl-', '0.1 mol/L'], ['FeO', '0.2 mol/L']])

    def test_transport_number_1(self):
        actual = self.s1.get_transport_number('K+')
        self.assertTrue(0 <= actual and actual <= 1)

    def test_transport_number_2(self):
        actual = self.s1.get_transport_number('H2O')
        self.assertEqual(actual.magnitude, 0)

    def test_transport_number_3(self):
        actual = self.s1.get_transport_number('FeO')
        self.assertEqual(actual.magnitude, 0)

    def test_transport_number_4(self):
        total_t = 0
        for item in self.s1.components:
            total_t += self.s1.get_transport_number(item)

        self.assertAlmostEqual(total_t.magnitude, 1)


class Test_molar_conductivity(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_molar_conductivity"""

    def setUp(self):
        self.tol = 0.05

    def test_molar_conductivity_potassium(self):
        self.s1 = pyEQL.Solution([
         [
          'K+', '0.001 mol/L'], ['Cl-', '0.001 mol/L']],
          temperature='25 degC')
        result = self.s1.get_molar_conductivity('K+').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('73.48e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_sodium(self):
        self.s1 = pyEQL.Solution([
         [
          'Na+', '0.001 mol/L'], ['Cl-', '0.001 mol/L']],
          temperature='25 degC')
        result = self.s1.get_molar_conductivity('Na+').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('50.08e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_magnesium(self):
        self.s1 = pyEQL.Solution([
         [
          'Mg+2', '0.001 mol/L'], ['Cl-', '0.002 mol/L']],
          temperature='25 degC')
        result = self.s1.get_molar_conductivity('Mg+2').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('106e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_chloride(self):
        self.s1 = pyEQL.Solution([
         [
          'Na+', '0.001 mol/L'], ['Cl-', '0.001 mol/L']],
          temperature='25 degC')
        result = self.s1.get_molar_conductivity('Cl-').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('76.31e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_fluoride(self):
        self.s1 = pyEQL.Solution([
         [
          'Na+', '0.001 mol/L'], ['F-', '0.001 mol/L']],
          temperature='25 degC')
        result = self.s1.get_molar_conductivity('F-').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('55.4e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_sulfate(self):
        self.s1 = pyEQL.Solution([
         [
          'Na+', '0.002 mol/L'], ['SO4-2', '0.001 mol/L']],
          temperature='25 degC')
        result = self.s1.get_molar_conductivity('SO4-2').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('160.0e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_hydroxide(self):
        self.s1 = pyEQL.Solution(temperature='25 degC')
        result = self.s1.get_molar_conductivity('OH-').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('198e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_hydrogen(self):
        self.s1 = pyEQL.Solution(temperature='25 degC')
        result = self.s1.get_molar_conductivity('H+').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('349.65e-4 m**2 * S / mol').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_molar_conductivity_neutral(self):
        self.s1 = pyEQL.Solution([['FeCl3', '0.001 mol/L']], temperature='25 degC')
        result = self.s1.get_molar_conductivity('FeCl3').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('0 m**2 * S / mol').magnitude
        self.assertAlmostEqual(result, expected, 5)

    def test_molar_conductivity_water(self):
        self.s1 = pyEQL.Solution(temperature='25 degC')
        result = self.s1.get_molar_conductivity('H2O').to('m**2*S/mol').magnitude
        expected = pyEQL.unit('0 m**2 * S / mol').magnitude
        self.assertAlmostEqual(result, expected, 5)


class Test_mobility(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_mobility"""

    def setUp(self):
        self.tol = 0.05

    def test_mobility_potassium(self):
        self.s1 = pyEQL.Solution([
         [
          'K+', '0.001 mol/L'], ['Cl-', '0.001 mol/L']],
          temperature='25 degC')
        molar_conductivity = self.s1.get_molar_conductivity('K+').to('m**2*S/mol')
        expected = self.s1.get_mobility('K+').to('m**2/s/V').magnitude
        charge = self.s1.get_solute('K+').get_formal_charge()
        result = (molar_conductivity / (pyEQL.unit.N_A * pyEQL.unit.e * abs(charge))).to('m**2/s/V').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_mobility_chloride(self):
        self.s1 = pyEQL.Solution([
         [
          'K+', '0.001 mol/L'], ['Cl-', '0.001 mol/L']],
          temperature='25 degC')
        molar_conductivity = self.s1.get_molar_conductivity('Cl-').to('m**2*S/mol')
        expected = self.s1.get_mobility('Cl-').to('m**2/s/V').magnitude
        charge = self.s1.get_solute('Cl-').get_formal_charge()
        result = (molar_conductivity / (pyEQL.unit.N_A * pyEQL.unit.e * abs(charge))).to('m**2/s/V').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_mobility_magnesium(self):
        self.s1 = pyEQL.Solution([
         [
          'Mg+2', '0.001 mol/L'], ['Cl-', '0.002 mol/L']],
          temperature='25 degC')
        molar_conductivity = self.s1.get_molar_conductivity('Mg+2').to('m**2*S/mol')
        expected = self.s1.get_mobility('Mg+2').to('m**2/s/V').magnitude
        charge = self.s1.get_solute('Mg+2').get_formal_charge()
        result = (molar_conductivity / (pyEQL.unit.N_A * pyEQL.unit.e * abs(charge))).to('m**2/s/V').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_mobility_sulfate(self):
        self.s1 = pyEQL.Solution([
         [
          'K+', '0.002 mol/L'], ['SO4-2', '0.001 mol/L']],
          temperature='25 degC')
        molar_conductivity = self.s1.get_molar_conductivity('SO4-2').to('m**2*S/mol')
        expected = self.s1.get_mobility('SO4-2').to('m**2/s/V').magnitude
        charge = self.s1.get_solute('SO4-2').get_formal_charge()
        result = (molar_conductivity / (pyEQL.unit.N_A * pyEQL.unit.e * abs(charge))).to('m**2/s/V').magnitude
        self.assertWithinExperimentalError(result, expected, self.tol)


if __name__ == '__main__':
    unittest.main()