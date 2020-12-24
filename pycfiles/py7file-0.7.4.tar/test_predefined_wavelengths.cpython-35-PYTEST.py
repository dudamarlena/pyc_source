# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/robin/code/Py6S/test/test_predefined_wavelengths.py
# Compiled at: 2017-01-24 03:29:47
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