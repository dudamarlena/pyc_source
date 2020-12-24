# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_effective_pitzer.py
# Compiled at: 2020-04-22 00:40:24
# Size of source mod 2**32: 9830 bytes
__doc__ = "\npyEQL test suite for Effective Pitzer Model\n===========================================\n\nThis file contains tests for the Effective Pitzer Model\nimplemented in pyEQL.\n\nThe Effective Pitzer Model is described in Mistry et al.\n(DOI: 10.1016/j.desal.2013.03.015). The paper validates\nthe model by showing the calculated activity coefficients\nfor each component of synthetic seawater (composition\ngiven in Table 2 of the paper). The mock seawater\nhas a mass ratio of NaCl:MgCl2:Na2SO4:CaCl2:KCl\nof 24.53:5.20:4.09:1.16:0.695, and the total\nsalinity is varied.\n\n        MW\t    g/L\t    mol/L\nNaCl\t58.44\t24.53\t0.419746749\nMgCl2\t95.2\t5.2\t    0.054621849\nNa2SO4\t142\t    4.09\t0.028802817\nCaCl2\t110.98\t1.16\t0.010452334\nKCl\t    74.55\t0.0695\t0.00093226\n\nThe total molality is 0.515 mol salts/kg\n\nThis test suite replicates that synthetic seawter and then\nconfirms that pyEQL's output of activity and fugacity\ncoefficients matches that given by the authors.\n\npyEQL probably uses different pitzer parameters than\nthe paper, so perfect accuracy is not expected.\n\n"
import pyEQL, unittest

class Test_effective_pitzer(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_effective_pitzer"""

    def setUp(self):
        self.tol = 0.15

    def mock_seawater(self, multiple):
        """
        Create a solution of mock seawater.
        Multiple is a scale factor by which the base
        composition (regular seawater) is scaled.
        """
        s1 = pyEQL.Solution([
         [
          'Na+', str(multiple * 0.4197 + multiple * 2 * 0.0288) + 'mol/L'],
         [
          'Cl-',
          str(multiple * 0.4197 + multiple * 2 * 0.0546 + multiple * 2 * 0.01045 + multiple * 0.00093) + 'mol/L'],
         [
          'Mg+2', str(multiple * 0.0546) + 'mol/L'],
         [
          'SO4-2', str(multiple * 0.0288) + 'mol/L'],
         [
          'Ca+2', str(multiple * 0.01045) + 'mol/L'],
         [
          'K+', str(multiple * 0.00093) + 'mol/L']])
        return s1

    def test_effective_pitzer_nacl_activity(self):
        multiple = [
         1, 2, 5, 8]
        expected = [0.7, 0.7, 0.8, 1.1]
        from pyEQL import paramsDB as db
        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt('Na+', 'Cl-')
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, 'pitzer_parameters_activity')
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())
            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(s1.get_ionic_strength(), molality, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], Salt.z_cation, Salt.z_anion, Salt.nu_cation, Salt.nu_anion, temperature)
            result = activity_coefficient * (1 + pyEQL.unit('0.018 kg/mol') * s1.get_total_moles_solute() / s1.get_solvent_mass())
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_effective_pitzer_mgcl2_activity(self):
        multiple = [
         1, 2, 5, 8]
        expected = [0.5, 0.5, 0.67, 1.15]
        from pyEQL import paramsDB as db
        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt('Mg+2', 'Cl-')
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, 'pitzer_parameters_activity')
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())
            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(s1.get_ionic_strength(), molality, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], Salt.z_cation, Salt.z_anion, Salt.nu_cation, Salt.nu_anion, temperature)
            result = activity_coefficient * (1 + pyEQL.unit('0.018 kg/mol') * s1.get_total_moles_solute() / s1.get_solvent_mass())
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_effective_pitzer_KCl_activity(self):
        multiple = [
         1, 2, 5, 8]
        expected = [0.65, 0.61, 0.65, 0.7]
        from pyEQL import paramsDB as db
        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt('K+', 'Cl-')
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, 'pitzer_parameters_activity')
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())
            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(s1.get_ionic_strength(), molality, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], Salt.z_cation, Salt.z_anion, Salt.nu_cation, Salt.nu_anion, temperature)
            result = activity_coefficient * (1 + pyEQL.unit('0.018 kg/mol') * s1.get_total_moles_solute() / s1.get_solvent_mass())
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    @unittest.expectedFailure
    def test_effective_pitzer_na2so4_activity(self):
        multiple = [
         1, 2, 5, 8]
        expected = [0.38, 0.3, 0.25, 0.2]
        from pyEQL import paramsDB as db
        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt('Na+', 'SO4-2')
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, 'pitzer_parameters_activity')
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())
            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(s1.get_ionic_strength(), molality, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], Salt.z_cation, Salt.z_anion, Salt.nu_cation, Salt.nu_anion, temperature)
            result = activity_coefficient * (1 + pyEQL.unit('0.018 kg/mol') * s1.get_total_moles_solute() / s1.get_solvent_mass())
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_effective_pitzer_fugacity(self):
        multiple = [
         1, 5, 8, 10]
        expected = [1, 1, 0.95, 0.95]
        from pyEQL import paramsDB as db
        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            result = s1.get_osmotic_coefficient(scale='fugacity')
            self.assertWithinExperimentalError(result, expected[item], self.tol)


if __name__ == '__main__':
    unittest.main()