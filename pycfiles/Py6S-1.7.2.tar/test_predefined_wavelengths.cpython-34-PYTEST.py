# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/code/Py6S/test/test_predefined_wavelengths.py
# Compiled at: 2015-09-12 04:41:53
# Size of source mod 2**32: 1200 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from Py6S import *
import numpy as np

class PredefinedWavelengthTests(unittest.TestCase):

    def test_all_predefined_wavelengths(self):
        s = SixS()
        attribs = dir(PredefinedWavelengths)
        for wavelength in attribs:
            wv = eval('PredefinedWavelengths.%s' % wavelength)
            if type(wv) is tuple:
                print(wavelength)
                s.wavelength = Wavelength(wv)
                s.run()
                continue