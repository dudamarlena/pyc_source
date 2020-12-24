# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/robin/code/Py6S/test/test.py
# Compiled at: 2018-08-09 17:17:27
# Size of source mod 2**32: 7650 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from Py6S import *
import numpy as np, os.path
test_dir = os.path.relpath(os.path.dirname(__file__))

class SimpleTests(unittest.TestCase):

    def test_inbuilt_test(self):
        result = SixS.test()
        self.assertEqual(result, 0)


class SixSClassTests(unittest.TestCase):

    def test_custom_path(self):
        from Py6S import sixs
        s = SixS('/home/robintw/Py6S/6S/6SV1.1/sixsV1.1')
        s.run()
        self.assertEqual(s.outputs.version, sixs.SIXSVERSION)
        self.assertAlmostEqual((s.outputs.transmittance_aerosol_scattering.downward), 0.93514, delta=0.002)

    def test_debug_report(self):
        s = SixS()
        s.produce_debug_report()

    def test_writing_input_file(self):
        s = SixS()
        s.write_input_file('test_input_file.txt')
        self.assertEqual(os.path.exists('test_input_file.txt'), True)

    def test_no_sixs_path(self):
        s = SixS()
        s.sixs_path = None
        with self.assertRaises(ExecutionError):
            s.run()


class VisAOTTests(unittest.TestCase):

    def test_vis_aot_normal(self):
        s = SixS()
        s.run()
        self.assertAlmostEqual((s.outputs.visibility), 8.49, delta=0.002)
        self.assertAlmostEqual((s.outputs.aot550), 0.5, delta=0.002)

    def test_vis_aot_small(self):
        s = SixS()
        s.aot550 = 0.001
        s.run()
        self.assertAlmostEqual(s.outputs.visibility, float('Inf'))
        self.assertAlmostEqual((s.outputs.aot550), 0.001, delta=0.002)

    def test_set_vis(self):
        s = SixS()
        s.aot550 = None
        s.visibility = 40
        s.run()
        self.assertAlmostEqual((s.outputs.phase_function_Q.aerosol), (-0.04939), delta=0.002)


class WavelengthTests(unittest.TestCase):

    def test_specific_wavelength(self):
        s = SixS()
        s.wavelength = Wavelength(0.567)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 129.792, delta=0.002)

    def test_wavelength_range(self):
        s = SixS()
        s.wavelength = Wavelength(0.5, 0.7)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 122.166, delta=0.002)

    def test_wavelength_filter(self):
        s = SixS()
        s.wavelength = Wavelength(0.4, 0.41, [0.7, 0.9, 1.0, 0.3, 1.0])
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 109.435, delta=0.002)

    def test_wavelength_predefined(self):
        s = SixS()
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_TM_B1)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 138.126, delta=0.002)
        s.wavelength = Wavelength(PredefinedWavelengths.MODIS_B6)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 17.917, delta=0.002)

    def test_invalid_wavelengths(self):
        with self.assertRaises(ParameterError):
            Wavelength(1000)
        with self.assertRaises(ParameterError):
            Wavelength(0.15)
        with self.assertRaises(ParameterError):
            Wavelength(0.5, 50)


class AtmosCorrTests(unittest.TestCase):

    def test_atmos_corr_radiance(self):
        s = SixS()
        s.atmos_corr = AtmosCorr.AtmosCorrLambertianFromRadiance(130.1)
        s.run()
        self.assertAlmostEqual((s.outputs.atmos_corrected_reflectance_lambertian), 0.29048, delta=0.002)


class UserDefinedSpectraTest(unittest.TestCase):

    def test_aster_spectra(self):
        s = SixS()
        s.ground_reflectance = GroundReflectance.HomogeneousLambertian(Spectra.import_from_aster('http://speclib.jpl.nasa.gov/speclibdata/jhu.becknic.water.ice.none.solid.ice.spectrum.txt'))
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 7.753, delta=0.002)

    def test_aster_spectra_from_file(self):
        s = SixS()
        s.altitudes.set_target_sea_level()
        s.altitudes.set_sensor_satellite_level()
        s.ground_reflectance = GroundReflectance.HomogeneousLambertian(Spectra.import_from_aster(os.path.join(test_dir, 'jhu.becknic.vegetation.trees.conifers.solid.conifer.spectrum.txt')))
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_reflectance), 0.1403693, delta=0.002)

    def test_usgs_spectra(self):
        s = SixS()
        s.ground_reflectance = GroundReflectance.HomogeneousLambertian(Spectra.import_from_usgs('http://speclab.cr.usgs.gov/spectral.lib06/ds231/ASCII/V/cheatgrass_anp92-11a_veg.29744.asc'))
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 29.316, delta=0.002)

    def test_usgs_spectra_from_file(self):
        s = SixS()
        s.ground_reflectance = GroundReflectance.HomogeneousLambertian(Spectra.import_from_usgs(os.path.join(test_dir, 'butlerite_gds25.3947.asc')))
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 180.818, delta=0.002)


class GeometryTest(unittest.TestCase):

    def test_geom_from_time_and_loc(self):
        g = Geometry.User()
        g.from_time_and_location(50, -1, '2014-05-06', 0, 30)
        self.assertEqual(str(g), '0 (User defined)\n113.587146 359.826938 0.000000 30.000000 5 6\n')


class AltitudesTest(unittest.TestCase):

    def test_custom_sensor_altitude(self):
        s = SixS()
        s.altitudes.set_sensor_custom_altitude(3, 0.26)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 147.964, delta=0.002)

    def test_custom_target_altitude(self):
        s = SixS()
        s.altitudes.set_target_custom_altitude(7)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 139.192, delta=0.002)

    def test_custom_altitudes(self):
        s = SixS()
        s.altitudes.set_target_custom_altitude(7)
        s.altitudes.set_sensor_custom_altitude(50, 0.26)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 158.101, delta=0.002)

    def test_satellite_level(self):
        s = SixS()
        s.altitudes.set_sensor_satellite_level()
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 165.188, delta=0.002)

    def test_changing_levels(self):
        s = SixS()
        s.altitudes.set_sensor_custom_altitude(1)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 142.053, delta=0.002)
        s.altitudes.set_sensor_satellite_level()
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 165.188, delta=0.002)

    def test_target_pressure(self):
        s = SixS()
        s.altitudes.set_sensor_satellite_level()
        s.altitudes.set_target_pressure(200)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 165.188, delta=0.002)


class GroundReflectanceTest(unittest.TestCase):

    def test_hetero_ground_reflectance(self):
        s = SixS()
        s.altitudes.set_sensor_satellite_level()
        s.altitudes.set_target_sea_level()
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_ETM_B2)
        wavelengths = np.arange(0.5, 0.6, 0.025)
        ro_target = np.array([wavelengths, [1.0] * 4]).T
        ro_env = np.array([wavelengths, [0.5] * 4]).T
        s.ground_reflectance = GroundReflectance.HeterogeneousLambertian(0.3, ro_target, ro_env)
        s.run()
        self.assertAlmostEqual((s.outputs.apparent_radiance), 343.68, delta=0.002)