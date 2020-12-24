# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_activity.py
# Compiled at: 2020-04-22 01:17:03
# Size of source mod 2**32: 20101 bytes
__doc__ = '\npyEQL activity correction methods test suite\n============================================\n\nThis file contains tests for some of the activity correction methods\nemployed by pyEQL.\n\nNOTE: generally, these tests check the module output against experimental\ndata rather than the theoretical result of the respective functions. In some\ncases, the output is also tested against a well-established model published\nby USGS(PHREEQC)\n'
import pyEQL, unittest

class Test_activity_pitzer_nacl(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_activity_pitzer_nacl"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Na+', '0.1 mol/L'], ['Cl-', '0.1 mol/L']])
        self.tol = 0.05

    def test_activity_pitzer_coeff_units(self):
        result = self.s1.get_activity_coefficient('Na+').dimensionality
        self.assertEqual(result, '')

    def test_activity_pitzer_units(self):
        result = self.s1.get_activity('Na+').dimensionality
        self.assertEqual(result, '')

    def test_activity_pitzer_equality(self):
        a1 = self.s1.get_activity_coefficient('Na+')
        a2 = self.s1.get_activity_coefficient('Cl-')
        self.assertEqual(a1, a2)

    def test_activity_crc_HCl(self):
        """
        calculate the activity coefficient of HCl at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        cation = 'H+'
        nu_cation = 1
        anion = 'Cl-'
        nu_anion = 1
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        pub_activity_coeff = [
         0.965,
         0.952,
         0.929,
         0.905,
         0.876,
         0.832,
         0.797,
         0.768,
         0.759,
         0.811,
         1.009,
         2.38]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i] * nu_cation) + 'mol/kg'
                conc_a = str(conc_list[i] * nu_anion) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute(cation, conc_c)
                sol.add_solute(anion, conc_a)
                act_cat = sol.get_activity_coefficient(cation)
                act_an = sol.get_activity_coefficient(anion)
                result = (act_cat ** nu_cation * act_an ** nu_anion) ** (1 / (nu_cation + nu_anion))
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_CsI(self):
        """
        calculate the activity coefficient of CsI at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        cation = 'Cs+'
        nu_cation = 1
        anion = 'I-'
        nu_anion = 1
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2]
        pub_activity_coeff = [
         0.965,
         0.951,
         0.925,
         0.898,
         0.863,
         0.804,
         0.749,
         0.688,
         0.601,
         0.534,
         0.47]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i] * nu_cation) + 'mol/kg'
                conc_a = str(conc_list[i] * nu_anion) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute(cation, conc_c)
                sol.add_solute(anion, conc_a)
                act_cat = sol.get_activity_coefficient(cation)
                act_an = sol.get_activity_coefficient(anion)
                result = (act_cat ** nu_cation * act_an ** nu_anion) ** (1 / (nu_cation + nu_anion))
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_bacl2(self):
        """
        calculate the activity coefficient of BaCl2 at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
        pub_activity_coeff = [
         0.887,
         0.849,
         0.782,
         0.721,
         0.653,
         0.559,
         0.492,
         0.436,
         0.391,
         0.393]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i]) + 'mol/kg'
                conc_a = str(conc_list[i] * 2) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Ba+2', conc_c)
                sol.add_solute('Cl-', conc_a)
                act_cat = sol.get_activity_coefficient('Ba+2')
                act_an = sol.get_activity_coefficient('Cl-')
                result = (act_cat ** 1 * act_an ** 2) ** 0.3333333333333333
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_licl(self):
        """
        calculate the activity coefficient of LiCl at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        pub_activity_coeff = [
         0.965,
         0.952,
         0.928,
         0.904,
         0.874,
         0.827,
         0.789,
         0.756,
         0.739,
         0.775,
         0.924,
         2.0]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i]) + 'mol/kg'
                conc_a = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Li+', conc_c)
                sol.add_solute('Cl-', conc_a)
                act_cat = sol.get_activity_coefficient('Li+')
                act_an = sol.get_activity_coefficient('Cl-')
                result = (act_cat ** 1 * act_an ** 1) ** 0.5
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_rbcl(self):
        """
        calculate the activity coefficient of RbCl at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        pub_activity_coeff = [
         0.965,
         0.951,
         0.926,
         0.9,
         0.867,
         0.811,
         0.761,
         0.707,
         0.633,
         0.583,
         0.546,
         0.544]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i]) + 'mol/kg'
                conc_a = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Rb+', conc_c)
                sol.add_solute('Cl-', conc_a)
                result = sol.get_activity_coefficient('Rb+')
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_MgCl2(self):
        """
        calculate the activity coefficient of MgCl2 at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        cation = 'Mg+2'
        nu_cation = 1
        anion = 'Cl-'
        nu_anion = 2
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        pub_activity_coeff = [
         0.889,
         0.852,
         0.79,
         0.734,
         0.672,
         0.59,
         0.535,
         0.493,
         0.485,
         0.577,
         1.065,
         14.4]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i] * nu_cation) + 'mol/kg'
                conc_a = str(conc_list[i] * nu_anion) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute(cation, conc_c)
                sol.add_solute(anion, conc_a)
                act_cat = sol.get_activity_coefficient(cation)
                act_an = sol.get_activity_coefficient(anion)
                result = (act_cat ** nu_cation * act_an ** nu_anion) ** (1 / (nu_cation + nu_anion))
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_KBr(self):
        """
        calculate the activity coefficient of KBr at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        cation = 'K+'
        nu_cation = 1
        anion = 'Br-'
        nu_anion = 1
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
        pub_activity_coeff = [
         0.965,
         0.952,
         0.927,
         0.902,
         0.87,
         0.817,
         0.771,
         0.722,
         0.658,
         0.617,
         0.593,
         0.626]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i] * nu_cation) + 'mol/kg'
                conc_a = str(conc_list[i] * nu_anion) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute(cation, conc_c)
                sol.add_solute(anion, conc_a)
                act_cat = sol.get_activity_coefficient(cation)
                act_an = sol.get_activity_coefficient(anion)
                result = (act_cat ** nu_cation * act_an ** nu_anion) ** (1 / (nu_cation + nu_anion))
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_crc_k2so4(self):
        """
        calculate the activity coefficient of K2SO4 at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *CRC Handbook of Chemistry and Physics*, Mean Activity Coefficients of Electrolytes as a Function of
        Concentration, in: W.M. Haynes (Ed.), 92nd ed., 2011.

        """
        conc_list = [
         0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
        pub_activity_coeff = [
         0.885,
         0.844,
         0.772,
         0.704,
         0.625,
         0.511,
         0.424,
         0.343,
         0.251]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc_c = str(conc_list[i] * 2) + 'mol/kg'
                conc_a = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('K+', conc_c)
                sol.add_solute('SO4-2', conc_a)
                act_cat = sol.get_activity_coefficient('K+')
                act_an = sol.get_activity_coefficient('SO4-2')
                result = (act_cat ** 2 * act_an ** 1) ** 0.3333333333333333
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_pitzer_nacl_1(self):
        """
        calculate the activity coefficient at each concentration and compare
        to experimental data

        Experimental activity coefficient values at 25 degC are found in
        *J. Phys. Chem. Reference Data* Vol 13 (1), 1984, p.53.

        """
        conc_list = [
         0.1, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6]
        pub_activity_coeff = [
         0.778,
         0.72,
         0.681,
         0.665,
         0.657,
         0.669,
         0.714,
         0.782,
         0.873,
         0.987]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Na+', conc)
                sol.add_solute('Cl-', conc)
                result = sol.get_activity_coefficient('Na+')
                expected = pub_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    @unittest.expectedFailure
    def test_water_activity_pitzer_nacl_1(self):
        r"""
        calculate the water activity at each concentration and compare
        to experimental data

        Experimental osmotic coefficients for NaCl are found in:
        Pitzer and Pelper, 1984. "Thermodyamic Properties of Aqueous Sodium Chloride Solutions"
        *J. Phys. Chem. Ref. Data* 13(1).

        Osmotic coefficients were converted into water activity according to the equation
        found in
        Blandamer, Mike J., Engberts, Jan B. F. N., Gleeson, Peter T., Reis,
        Joao Carlos R., 2005. "Activity of water in aqueous systems: A frequently
        neglected property." *Chemical Society Review* 34, 440-458.

        .. math:: ln a_w = - \Phi M_w \sum_i m_i

        Where :math:`M_w` is the molar mass of water (0.018015 kg/mol) and :math:`m_i` is the molal concentration
        of each species.

        """
        conc_list = [
         0.1, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6]
        pub_water_activity = [
         0.9964,
         0.991,
         0.9821,
         0.9733,
         0.9646,
         0.9304,
         0.8975,
         0.8657,
         0.8351,
         0.8055]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Na+', conc)
                sol.add_solute('Cl-', conc)
                result = sol.get_water_activity()
                expected = pub_water_activity[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_activity_pitzer_phreeqc_nacl_2(self):
        """
        calculate the activity coefficient at each concentration and compare
        to the output of the PHREEQC model

        PHREEQC version 3.1.4 was used to calculate density, conductivity, water
        activity, and NaCl activity coefficient for NaCl solutions up to 6m.
        The Pitzer model (pitzer.dat) database was used.
        <http://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc/>

        """
        conc_list = [
         0.1, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6]
        phreeqc_pitzer_activity_coeff = [
         0.7771,
         0.7186,
         0.6799,
         0.6629,
         0.6561,
         0.6675,
         0.7128,
         0.7825,
         0.8729,
         0.9874]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Na+', conc)
                sol.add_solute('Cl-', conc)
                result = sol.get_activity_coefficient('Na+')
                expected = phreeqc_pitzer_activity_coeff[i]
                self.assertWithinExperimentalError(result, expected, self.tol)

    def test_water_activity_phreeqc_pitzer_nacl_2(self):
        """
        calculate the water activity at each concentration and compare
        to the output of the PHREEQC model

        PHREEQC version 3.1.4 was used to calculate density, conductivity, water
        activity, and NaCl activity coefficient for NaCl solutions up to 6m.
        The Pitzer model (pitzer.dat) database was used.
        <http://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc/>

        """
        conc_list = [
         0.1, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6]
        phreeqc_pitzer_water_activity = [
         0.997,
         0.992,
         0.984,
         0.975,
         0.967,
         0.932,
         0.893,
         0.851,
         0.807,
         0.759]
        for i in range(len(conc_list)):
            with self.subTest(conc=(conc_list[i])):
                conc = str(conc_list[i]) + 'mol/kg'
                sol = pyEQL.Solution()
                sol.add_solute('Na+', conc)
                sol.add_solute('Cl-', conc)
                result = sol.get_water_activity()
                expected = phreeqc_pitzer_water_activity[i]
                self.assertWithinExperimentalError(result, expected, self.tol)


if __name__ == '__main__':
    unittest.main()