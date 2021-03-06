# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/code/Py6S/test/test_profiles.py
# Compiled at: 2019-03-07 14:34:34
# Size of source mod 2**32: 9384 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from Py6S import *
import numpy as np

class AtmosProfileTests(unittest.TestCase):

    def test_atmos_profile(self):
        aps = [
         AtmosProfile.Tropical,
         AtmosProfile.NoGaseousAbsorption,
         AtmosProfile.UserWaterAndOzone(0.9, 3)]
        results = [0.2723143,
         0.2747224,
         0.2476101]
        for i in range(len(aps)):
            s = SixS()
            s.atmos_profile = aps[i]
            s.run()
            self.assertAlmostEqual((s.outputs.apparent_reflectance), (results[i]), msg=('Error in atmos profile with ID %s. Got %f, expected %f.' % (str(aps[i]), s.outputs.apparent_reflectance, results[i])), delta=0.002)

    def test_from_lat_and_date(self):
        ap = AtmosProfile.FromLatitudeAndDate(53, '2015-07-14')
        @py_assert3 = AtmosProfile.PredefinedType
        @py_assert6 = AtmosProfile.SubarcticSummer
        @py_assert8 = @py_assert3(@py_assert6)
        @py_assert1 = ap == @py_assert8
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/robin/code/Py6S/test/test_profiles.py', lineno=42)
        if not @py_assert1:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s.PredefinedType\n}(%(py7)s\n{%(py7)s = %(py5)s.SubarcticSummer\n})\n}', ), (ap, @py_assert8)) % {'py0':@pytest_ar._saferepr(ap) if 'ap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ap) else 'ap',  'py2':@pytest_ar._saferepr(AtmosProfile) if 'AtmosProfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(AtmosProfile) else 'AtmosProfile',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(AtmosProfile) if 'AtmosProfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(AtmosProfile) else 'AtmosProfile',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


class AeroProfileTests(unittest.TestCase):

    def test_aero_profile(self):
        user_ap = AeroProfile.UserProfile(AeroProfile.Maritime)
        user_ap.add_layer(5, 0.34)
        aps = [
         AeroProfile.Continental,
         AeroProfile.NoAerosols,
         AeroProfile.User(dust=0.3, oceanic=0.7),
         user_ap]
        results = [122.854,
         140.289,
         130.866,
         136.649]
        for i in range(len(aps)):
            s = SixS()
            s.aero_profile = aps[i]
            s.run()
            self.assertAlmostEqual((s.outputs.apparent_radiance), (results[i]), ('Error in aerosol profile with ID %s. Got %f, expected %f.' % (str(aps[i]), s.outputs.apparent_radiance, results[i])), delta=0.002)

    def test_aero_profile_errors(self):
        with self.assertRaises(ParameterError):
            ap = AeroProfile.User(dust=0.8, oceanic=0.4)

    def test_sun_photo_dist_errors1(self):
        with self.assertRaises(ParameterError):
            ap = AeroProfile.SunPhotometerDistribution([0.050000001, 0.065604001, 0.086076997,
             0.112939, 0.148184001, 0.194428995, 0.255104989, 0.334715992, 0.439173013, 0.576227009,
             0.756052017, 0.99199599, 1.30157101, 1.707757, 2.24070191, 2.93996596, 3.85745192,
             5.06126022, 6.64074516, 8.71314526], [
             0.001338098, 0.007492487, 0.026454749, 0.058904506, 0.082712278, 0.073251031, 0.040950641,
             0.014576218, 0.003672085, 0.001576356, 0.002422644, 0.004472982, 0.007452302, 0.011037065,
             0.014523974, 0.016981738, 0.017641816, 0.016284294, 0.01335547, 0.009732267, 0.006301342,
             0.003625077], [
             1.47] * 20, [
             0.0093] * 20)

    def test_sun_photo_dist_errors2(self):
        with self.assertRaises(ParameterError):
            ap = AeroProfile.SunPhotometerDistribution([0.050000001, 0.065604001, 0.086076997,
             0.112939, 0.148184001, 0.194428995, 0.255104989, 0.334715992, 0.439173013, 0.576227009,
             0.756052017, 0.99199599, 1.30157101, 1.707757, 2.24070191, 2.93996596, 3.85745192,
             5.06126022, 6.64074516, 8.71314526, 11.4322901, 15], [
             0.001338098, 0.007492487, 0.026454749, 0.058904506, 0.082712278, 0.073251031, 0.040950641,
             0.014576218, 0.003672085, 0.001576356, 0.002422644, 0.004472982, 0.007452302, 0.011037065,
             0.014523974, 0.016981738, 0.017641816, 0.016284294, 0.01335547, 0.009732267, 0.006301342,
             0.003625077], [
             1.47] * 15, [
             0.0093] * 20)

    def test_sun_photo_dist_errors3(self):
        ap1 = AeroProfile.SunPhotometerDistribution([0.050000001, 0.065604001, 0.086076997,
         0.112939, 0.148184001, 0.194428995, 0.255104989, 0.334715992, 0.439173013, 0.576227009,
         0.756052017, 0.99199599, 1.30157101, 1.707757, 2.24070191, 2.93996596, 3.85745192,
         5.06126022, 6.64074516, 8.71314526, 11.4322901, 15], [
         0.001338098, 0.007492487, 0.026454749, 0.058904506, 0.082712278, 0.073251031, 0.040950641,
         0.014576218, 0.003672085, 0.001576356, 0.002422644, 0.004472982, 0.007452302, 0.011037065,
         0.014523974, 0.016981738, 0.017641816, 0.016284294, 0.01335547, 0.009732267, 0.006301342,
         0.003625077], [
         1.47] * 20, [
         2.3] * 20)
        ap2 = AeroProfile.SunPhotometerDistribution([0.050000001, 0.065604001, 0.086076997,
         0.112939, 0.148184001, 0.194428995, 0.255104989, 0.334715992, 0.439173013, 0.576227009,
         0.756052017, 0.99199599, 1.30157101, 1.707757, 2.24070191, 2.93996596, 3.85745192,
         5.06126022, 6.64074516, 8.71314526, 11.4322901, 15], [
         0.001338098, 0.007492487, 0.026454749, 0.058904506, 0.082712278, 0.073251031, 0.040950641,
         0.014576218, 0.003672085, 0.001576356, 0.002422644, 0.004472982, 0.007452302, 0.011037065,
         0.014523974, 0.016981738, 0.017641816, 0.016284294, 0.01335547, 0.009732267, 0.006301342,
         0.003625077], 1.47, 2.3)
        self.assertEqual(ap1, ap2)

    def test_multimodal_dist_errors1(self):
        with self.assertRaises(ParameterError):
            ap = AeroProfile.MultimodalLogNormalDistribution(0.001, 20)
            ap.add_component(0.05, 2.03, 0.538, [1.508, 1.5, 1.5, 1.5, 1.5,
             1.5, 1.5, 1.5, 1.495, 1.49, 1.49, 1.49, 1.486, 1.48, 1.47, 1.46, 1.456,
             1.443, 1.43, 1.47], [3.24e-07, 3e-08, 2.86e-08, 2.51e-08, 2.2e-08, 2e-08,
             1e-08, 1e-08, 1.48e-08, 2e-08, 6.85e-08, 1e-07, 1.25e-06, 3e-06, 0.00035,
             0.0006, 0.000686, 0.0017, 0.004, 0.0014])
            ap.add_component(0.0695, 2.03, 0.457, [1.452, 1.44, 1.438, 1.433,
             1.432, 1.431, 1.431, 1.43, 1.429, 1.429, 1.429, 1.428, 1.427, 1.425, 1.411, 1.401,
             1.395, 1.385, 1.364, 1.396], [1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08,
             1e-08, 1e-08, 1.38e-08, 1.47e-08, 1.68e-08, 1.93e-08, 4.91e-08, 1.75e-07, 9.66e-06,
             0.000194, 0.000384, 0.00112, 0.00251, 0.131])
            ap.add_component(0.4, 2.03, 0.005, [1.508, 1.5, 1.5, 1.5, 1.5,
             1.5, 1.5, 1.5, 1.495, 1.49, 1.49, 1.49, 1.486, 1.48, 1.47, 1.46, 1.456,
             1.443, 1.43, 1.47], [3.24e-07, 3e-08, 2.86e-08, 2.51e-08, 2.2e-08, 2e-08, 1e-08,
             1e-08, 1.48e-08, 2e-08, 6.85e-08, 1e-07, 1.25e-06, 3e-06, 0.00035, 0.0006, 0.000686,
             0.0017, 0.004, 0.0014])
            ap.add_component(0.4, 2.03, 0.005, [1.508, 1.5, 1.5, 1.5, 1.5,
             1.5, 1.5, 1.5, 1.495, 1.49, 1.49, 1.49, 1.486, 1.48, 1.47, 1.46, 1.456,
             1.443, 1.43, 1.47], [3.24e-07, 3e-08, 2.86e-08, 2.51e-08, 2.2e-08, 2e-08, 1e-08,
             1e-08, 1.48e-08, 2e-08, 6.85e-08, 1e-07, 1.25e-06, 3e-06, 0.00035, 0.0006, 0.000686,
             0.0017, 0.004, 0.0014])
            ap.add_component(0.4, 2.03, 0.005, [1.508, 1.5, 1.5, 1.5, 1.5,
             1.5, 1.5, 1.5, 1.495, 1.49, 1.49, 1.49, 1.486, 1.48, 1.47, 1.46, 1.456,
             1.443, 1.43, 1.47], [3.24e-07, 3e-08, 2.86e-08, 2.51e-08, 2.2e-08, 2e-08, 1e-08,
             1e-08, 1.48e-08, 2e-08, 6.85e-08, 1e-07, 1.25e-06, 3e-06, 0.00035, 0.0006, 0.000686,
             0.0017, 0.004, 0.0014])

    def test_multimodal_dist_errors2(self):
        with self.assertRaises(ParameterError):
            ap = AeroProfile.MultimodalLogNormalDistribution(0.001, 20)
            ap.add_component(0.05, 2.03, 0.538, [1.508, 1.5, 1.5, 1.5, 1.5,
             1.5, 1.5, 1.5, 1.495, 1.49, 1.49, 1.49, 1.486, 1.48, 1.47, 1.46, 1.456,
             1.443, 1.43, 1.47], [3.24e-07, 3e-08, 2.86e-08, 2.51e-08, 2.2e-08, 2e-08,
             1e-08, 1e-08, 1.48e-08, 2e-08, 6.85e-08, 1e-07, 1.25e-06, 3e-06, 0.00035,
             0.0006, 0.000686])

    def test_multimodal_dist_errors3(self):
        with self.assertRaises(ParameterError):
            ap = AeroProfile.MultimodalLogNormalDistribution(0.001, 20)
            ap.add_component(0.4, 2.03, 0.005, [1.508, 1.5, 1.5, 1.5, 1.5,
             1.5, 1.5, 1.5, 1.495, 1.49, 1.49, 1.49, 1.486, 1.48, 1.47, 1.46, 1.456,
             1.443, 1.43, 1.47, 1.999, 1.999, 0], [3.24e-07, 3e-08, 2.86e-08, 2.51e-08, 2.2e-08, 2e-08, 1e-08,
             1e-08, 1.48e-08, 2e-08, 6.85e-08, 1e-07, 1.25e-06, 3e-06, 0.00035, 0.0006, 0.000686,
             0.0017, 0.004, 0.0014])

    def test_running_multiple_add_components(self):
        s = SixS()
        real_intp = [0.0] * 20
        imag_intp = [0.0] * 20
        for i in range(4):
            s.aeroprofile = AeroProfile.MultimodalLogNormalDistribution(0.085, 2.9)
            s.aeroprofile.add_component(rmean=2.65, sigma=0.62, percentage_density=0.093, refr_real=real_intp, refr_imag=imag_intp)
            s.aeroprofile.add_component(rmean=0.176, sigma=0.46, percentage_density=0.907, refr_real=real_intp, refr_imag=imag_intp)