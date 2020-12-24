# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/code/Py6S/test/test_exceptions.py
# Compiled at: 2018-11-07 06:27:41
# Size of source mod 2**32: 1728 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from Py6S import *

class ExceptionTests(unittest.TestCase):

    def test_short_output(self):
        with self.assertRaises(OutputParsingError):
            s = SixS()
            s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeSummer)
            s.aero_profile = AeroProfile.PredefinedType(AeroProfile.Continental)
            s.visibility = 23
            altitudes = Altitudes()
            altitudes.set_sensor_satellite_level()
            altitudes.set_target_custom_altitude(-0.05)
            s.altitudes = altitudes
            s.atmos_corr = AtmosCorr.AtmosCorrLambertianFromReflectance(-0.2)
            s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_TM_B2)
            s.ground_reflectance = GroundReflectance.HomogeneousLambertian(0.3)
            s.geometry = Geometry.Landsat_TM()
            s.geometry.month = 4
            s.geometry.day = 25
            s.geometry.gmt_decimal_hour = 2
            s.geometry.latitude = 39.967
            s.geometry.longtitude = 116.35
            s.run()