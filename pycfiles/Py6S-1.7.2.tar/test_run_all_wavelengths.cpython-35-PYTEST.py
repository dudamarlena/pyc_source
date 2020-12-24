# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/code/Py6S/test/test_run_all_wavelengths.py
# Compiled at: 2015-09-12 04:41:53
# Size of source mod 2**32: 1526 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from Py6S import *
import numpy as np

class RunAllWavelengthsTests(unittest.TestCase):

    def test_run_all_wavelengths(self):
        s = SixS()
        attribs = dir(SixSHelpers.Wavelengths)
        for f in attribs:
            if 'run' in f and f != 'run_wavelengths':
                func = eval('SixSHelpers.Wavelengths.' + f)
                results = func(s, output_name='apparent_radiance')
                results = func(s)

    def test_extract_output(self):
        s = SixS()
        wvs, values = SixSHelpers.Wavelengths.run_landsat_etm(s, output_name='apparent_reflectance')
        wvs, objs = SixSHelpers.Wavelengths.run_landsat_etm(s)
        obj_values = SixSHelpers.Wavelengths.extract_output(objs, 'apparent_reflectance')
        self.assertTrue(np.all(values == obj_values))