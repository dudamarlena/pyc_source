# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/test/test_converter.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 2849 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/08/2019'
import unittest
from est.core.types import XASObject
from orangecontrib.est.utils import Converter
import est.core.utils as spectra_utils
import numpy

class TestConverter(unittest.TestCase):
    __doc__ = 'Test conversion of xas_object to Orange.data.Table'

    def setUp(self):
        self.energy, self.spectra = spectra_utils.create_dataset((128, 20, 1))
        self.xas_object = XASObject(energy=(self.energy), spectra=(self.spectra), dim1=20,
          dim2=10)

    def test_conversion(self):
        """Make sure the conversion to/from Orange.data.Table is safe for energy
        and beam absorption
        """
        xas_object = self.xas_object.copy(create_h5_file=False)
        data_table = Converter.toDataTable(xas_object=xas_object)
        converted_xas_object = Converter.toXASObject(data_table=data_table)
        numpy.testing.assert_array_almost_equal(xas_object.energy, converted_xas_object.energy)
        numpy.testing.assert_array_almost_equal(xas_object.spectra[0].mu, converted_xas_object.spectra[0].mu)
        numpy.testing.assert_array_almost_equal(xas_object.spectra[5].mu, converted_xas_object.spectra[5].mu)
        numpy.testing.assert_array_almost_equal(xas_object.spectra[18].mu, converted_xas_object.spectra[18].mu)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConverter,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite