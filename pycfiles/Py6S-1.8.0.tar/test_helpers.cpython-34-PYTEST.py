# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/code/Py6S/test/test_helpers.py
# Compiled at: 2015-10-26 15:24:38
# Size of source mod 2**32: 10108 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from Py6S import *
import numpy as np, os.path
test_dir = os.path.relpath(os.path.dirname(__file__))

class AllWavelengthsTests(unittest.TestCase):

    def test_run_for_landsat_etm(self):
        s = SixS()
        results = SixSHelpers.Wavelengths.run_landsat_etm(s, output_name='apparent_radiance')
        a = np.array([138.392, 129.426, 111.635, 75.822, 16.684, 5.532])
        self.assertAlmostEqual(results[0], [0.47750000000000004, 0.56125, 0.65875, 0.8262499999999999, 1.6487500000000002, 2.19625], delta=0.002)
        np.testing.assert_allclose(a, results[1], atol=0.1)


class ParallelEquivalenceTests(unittest.TestCase):

    def test_wavelengths_equiv(self):
        s = SixS()
        s.altitudes.set_sensor_satellite_level()
        s.altitudes.set_target_sea_level()
        serial_res = SixSHelpers.Wavelengths.run_vnir(s, spacing=0.05, output_name='apparent_radiance', n=1)
        for i in range(2, 10, 2):
            parallel_res = SixSHelpers.Wavelengths.run_vnir(s, spacing=0.05, output_name='apparent_radiance', n=i)
            np.testing.assert_allclose(parallel_res, serial_res)

    def test_after_prev_run(self):
        s = SixS()
        s.run()
        try:
            results = SixSHelpers.Wavelengths.run_vnir(s, spacing=0.05, output_name='apparent_radiance', n=1)
        except OutputParsingError:
            self.fail('OutputParsingError raised by run_vnir after previous SixS.run')

    def test_angles_equiv(self):
        s = SixS()
        serial_res = SixSHelpers.Angles.run360(s, 'view', output_name='apparent_radiance', n=1)
        for i in range(2, 10, 2):
            parallel_res = SixSHelpers.Angles.run360(s, 'view', output_name='apparent_radiance', n=i)
            np.testing.assert_allclose(parallel_res[0], serial_res[0])


class AllAnglesTests(unittest.TestCase):

    def test_run360(self):
        s = SixS()
        res0 = np.array([163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685,
         163.599, 160.769, 152.359, 138.612, 119.949, 97.014,
         70.809, 43.092, 17.56, 0.685, 163.599, 160.769,
         152.359, 138.612, 119.949, 97.014, 70.809, 43.092,
         17.56, 0.685, 163.599, 160.769, 152.359, 138.612,
         119.949, 97.014, 70.809, 43.092, 17.56, 0.685])
        results = SixSHelpers.Angles.run360(s, 'solar', output_name='apparent_radiance')
        np.testing.assert_allclose(results[0], res0)


class AERONETImportTest(unittest.TestCase):

    def test_import_aeronet(self):
        s = SixS()
        s = SixSHelpers.Aeronet.import_aeronet_data(s, os.path.join(test_dir, '070101_101231_Marambio.dubovik'), '2008-02-22')
        s.run()
        self.assertAlmostEqual(s.outputs.apparent_radiance, 137.324, delta=0.002)

    def test_import_empty_file(self):
        s = SixS()
        with self.assertRaises(ParameterError):
            SixSHelpers.Aeronet.import_aeronet_data(s, os.path.join(test_dir, 'empty_file'), '2008-02-22')


class RadiosondeImportTest(unittest.TestCase):

    def test_simple_radiosonde_import(self):
        s = SixS()
        s.altitudes.set_sensor_satellite_level()
        s.altitudes.set_target_sea_level()
        s.atmos_profile = SixSHelpers.Radiosonde.import_uow_radiosonde_data('http://weather.uwyo.edu/cgi-bin/sounding?region=europe&TYPE=TEXT%3ALIST&YEAR=2012&MONTH=02&FROM=2712&TO=2712&STNM=03808', AtmosProfile.MidlatitudeWinter)
        s.run()
        self.assertAlmostEqual(s.outputs.apparent_radiance, 164.482, delta=0.02)