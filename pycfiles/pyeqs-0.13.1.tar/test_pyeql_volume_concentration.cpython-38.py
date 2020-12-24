# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_pyeql_volume_concentration.py
# Compiled at: 2020-04-22 00:43:06
# Size of source mod 2**32: 15304 bytes
__doc__ = "\npyEQL volume and concentration methods test suite\n=================================================\n\nThis file contains tests for the volume and concentration-related methods\nused by pyEQL's Solution class\n"
import pyEQL, unittest

class Test_empty_solution(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_empty_solution"""

    def setUp(self):
        self.s1 = pyEQL.Solution()

    def test_empty_solution_1(self):
        expected = pyEQL.solution.Solution
        self.assertIsInstance(self.s1, expected)

    def test_empty_solution_2(self):
        result = self.s1.get_volume().to('L').magnitude
        expected = 1.0
        self.assertEqual(result, expected)

    def test_empty_solution_3(self):
        result = self.s1.get_solvent().get_name()
        expected = 'H2O'
        self.assertEqual(result, expected)

    def test_empty_solution_4(self):
        result = self.s1.get_solvent_mass().to('kg').magnitude
        expected = 0.9970415
        self.assertAlmostEqual(result, expected)

    def test_empty_solution_5(self):
        result = self.s1.get_temperature().to('degC').magnitude
        expected = 25
        self.assertEqual(result, expected)

    def test_empty_solution_6(self):
        result = self.s1.get_pressure().to('atm').magnitude
        expected = 1
        self.assertEqual(result, expected)

    def test_empty_solution_7(self):
        result = self.s1.get_activity('H+')
        expected = 1e-07
        self.assertAlmostEqual(result, expected, 9)

    def test_empty_solution_8(self):
        result = self.s1.list_solutes()
        expected = ['H2O', 'OH-', 'H+']
        self.assertCountEqual(result, expected)


class Test_solute_addition(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_solute_addition"""

    def setUp(self):
        self.s1 = pyEQL.Solution(volume='2 L')
        self.s2 = pyEQL.Solution([['Na+', '4 mol/L'], ['Cl-', '4 mol/L']], volume='2 L')
        self.s3 = pyEQL.Solution([
         [
          'Na+', '4 mol/kg'], ['Cl-', '4 mol/kg']],
          volume='2 L')
        self.s4 = pyEQL.Solution([['Na+', '8 mol'], ['Cl-', '8 mol']], volume='2 L')

    def test_solute_addition_1(self):
        result = self.s2.get_volume().to('L').magnitude
        expected = 2
        self.assertEqual(result, expected)

    def test_solute_addition_2(self):
        result = self.s2.get_amount('Na+', 'mol/L').magnitude
        expected = 4
        self.assertEqual(result, expected)

    def test_solute_addition_3(self):
        result = self.s3.get_amount('Na+', 'mol/kg').magnitude
        expected = 4
        self.assertEqual(result, expected)

    def test_solute_addition_4(self):
        result_molL = self.s2.get_solvent_mass().to('kg').magnitude
        result_molkg = self.s3.get_solvent_mass().to('kg').magnitude
        self.assertLess(result_molL, result_molkg)

    def test_solute_addition_4a(self):
        result = self.s4.get_amount('Na+', 'mol').magnitude
        expected = 8
        self.assertEqual(result, expected)

    def test_solute_addition_4b(self):
        result_molL = self.s2.get_solvent_mass().to('kg').magnitude
        result_mol = self.s4.get_solvent_mass().to('kg').magnitude
        self.assertLess(result_molL, result_mol)

    def test_solute_addition_5(self):
        self.s2.set_amount('Na+', '5 mol/L')
        self.s2.set_amount('Cl-', '5 mol/L')
        result = self.s2.get_volume().to('L').magnitude
        expected = 2
        self.assertEqual(result, expected)

    def test_solute_addition_6(self):
        original = self.s2.get_solvent_mass().to('kg').magnitude
        self.s2.set_amount('Na+', '5 mol/L')
        self.s2.set_amount('Cl-', '5 mol/L')
        result = self.s2.get_solvent_mass().to('kg').magnitude
        self.assertLess(result, original)

    def test_solute_addition_7(self):
        self.s2.set_amount('Na+', '5 mol/L')
        self.s2.set_amount('Cl-', '5 mol/L')
        result = self.s2.get_amount('Na+', 'mol/L').magnitude
        expected = 5
        self.assertEqual(result, expected)

    def test_solute_addition_8(self):
        original = self.s2.get_volume().to('L').magnitude
        self.s2.set_amount('Na+', '5 mol/kg')
        self.s2.set_amount('Cl-', '5 mol/kg')
        result = self.s2.get_volume().to('L').magnitude
        self.assertGreater(result, original)

    def test_solute_addition_9(self):
        original = self.s2.get_solvent_mass().to('kg').magnitude
        self.s2.set_amount('Na+', '5 mol/kg')
        self.s2.set_amount('Cl-', '5 mol/kg')
        result = self.s2.get_solvent_mass().to('kg').magnitude
        self.assertEqual(result, original)

    def test_solute_addition_10(self):
        self.s2.set_amount('Na+', '5 mol/kg')
        self.s2.set_amount('Cl-', '5 mol/kg')
        result = self.s2.get_amount('Na+', 'mol/kg').magnitude
        expected = 5
        self.assertEqual(result, expected)

    def test_solute_addition_8a(self):
        original = self.s2.get_volume().to('L').magnitude
        self.s2.set_amount('Na+', '10 mol')
        self.s2.set_amount('Cl-', '10 mol')
        result = self.s2.get_volume().to('L').magnitude
        self.assertGreater(result, original)

    def test_solute_addition_9a(self):
        original = self.s2.get_solvent_mass().to('kg').magnitude
        self.s2.set_amount('Na+', '10 mol')
        self.s2.set_amount('Cl-', '10 mol')
        result = self.s2.get_solvent_mass().to('kg').magnitude
        self.assertEqual(result, original)

    def test_solute_addition_10a(self):
        self.s2.set_amount('Na+', '10 mol')
        self.s2.set_amount('Cl-', '10 mol')
        result = self.s2.get_amount('Na+', 'mol').magnitude
        expected = 10
        self.assertEqual(result, expected)

    def test_solute_addition_11(self):
        self.s2.add_amount('Na+', '1 mol/L')
        self.s2.add_amount('Cl-', '1 mol/L')
        result = self.s2.get_volume().to('L').magnitude
        expected = 2
        self.assertEqual(result, expected)

    def test_solute_addition_12(self):
        original = self.s2.get_solvent_mass().to('kg').magnitude
        self.s2.add_amount('Na+', '1 mol/L')
        self.s2.add_amount('Cl-', '1 mol/L')
        result = self.s2.get_solvent_mass().to('kg').magnitude
        self.assertLess(result, original)

    def test_solute_addition_13(self):
        self.s2.add_amount('Na+', '1 mol/L')
        self.s2.add_amount('Cl-', '1 mol/L')
        result = self.s2.get_amount('Na+', 'mol/L').magnitude
        expected = 5
        self.assertEqual(result, expected)

    def test_solute_addition_14(self):
        original = self.s3.get_volume().to('L').magnitude
        self.s3.add_amount('Na+', '1 mol/kg')
        self.s3.add_amount('Cl-', '1 mol/kg')
        result = self.s3.get_volume().to('L').magnitude
        self.assertGreater(result, original)

    def test_solute_addition_15(self):
        original = self.s3.get_solvent_mass().to('kg').magnitude
        self.s3.add_amount('Na+', '1 mol/kg')
        self.s3.add_amount('Cl-', '1 mol/kg')
        result = self.s3.get_solvent_mass().to('kg').magnitude
        self.assertEqual(result, original)

    def test_solute_addition_16(self):
        self.s3.add_amount('Na+', '1 mol/kg')
        self.s3.add_amount('Cl-', '1 mol/kg')
        result = self.s3.get_amount('Na+', 'mol/kg').magnitude
        expected = 5
        self.assertEqual(result, expected)

    def test_solute_addition_14a(self):
        original = self.s2.get_volume().to('L').magnitude
        self.s2.add_amount('Na+', '2 mol')
        self.s2.add_amount('Cl-', '2 mol')
        result = self.s2.get_volume().to('L').magnitude
        self.assertGreater(result, original)

    def test_solute_addition_15a(self):
        original = self.s2.get_solvent_mass().to('kg').magnitude
        self.s2.add_amount('Na+', '2 mol')
        self.s2.add_amount('Cl-', '2 mol')
        result = self.s2.get_solvent_mass().to('kg').magnitude
        self.assertEqual(result, original)

    def test_solute_addition_16a(self):
        self.s2.add_amount('Na+', '2 mol')
        self.s2.add_amount('Cl-', '2 mol')
        result = self.s2.get_amount('Na+', 'mol').magnitude
        expected = 10
        self.assertEqual(result, expected)

    def test_solute_addition_14b(self):
        original = self.s2.get_volume().to('L').magnitude
        self.s2.add_amount('Na+', '-2 mol')
        self.s2.add_amount('Cl-', '-2 mol')
        result = self.s2.get_volume().to('L').magnitude
        self.assertLess(result, original)

    def test_solute_addition_15b(self):
        original = self.s2.get_solvent_mass().to('kg').magnitude
        self.s2.add_amount('Na+', '-2 mol')
        self.s2.add_amount('Cl-', '-2 mol')
        result = self.s2.get_solvent_mass().to('kg').magnitude
        self.assertEqual(result, original)

    def test_solute_addition_16b(self):
        self.s2.add_amount('Na+', '-2 mol')
        self.s2.add_amount('Cl-', '-2 mol')
        result = self.s2.get_amount('Na+', 'mol').magnitude
        expected = 6
        self.assertEqual(result, expected)


class Test_get_amount(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_get_amount"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Na+', '1 mol/L'], ['Cl-', '1 mol/L']])

    def test_get_amount_molL(self):
        result = self.s1.get_amount('Na+', 'mol/L').magnitude
        expected = 1
        self.assertAlmostEqual(result, expected, 9)

    def test_get_amount_molkg(self):
        result = self.s1.get_amount('Na+', 'mol/kg').magnitude
        expected = 1.02181221888
        self.assertAlmostEqual(result, expected, 9)

    def test_get_amount_gL(self):
        result = self.s1.get_amount('Na+', 'g/L').magnitude
        expected = 22.98977
        self.assertAlmostEqual(result, expected, 9)

    def test_get_amount_mg(self):
        result = self.s1.get_amount('Na+', 'mg').magnitude
        expected = 22989.77
        self.assertAlmostEqual(result, expected, 9)

    def test_get_amount_mol(self):
        result = self.s1.get_amount('Na+', 'mol').magnitude
        expected = 1
        self.assertAlmostEqual(result, expected, 9)

    def test_get_amount_fraction(self):
        result = self.s1.get_amount('Na+', 'fraction')
        expected = 0.01775457254
        self.assertAlmostEqual(result, expected, 9)


if __name__ == '__main__':
    unittest.main()