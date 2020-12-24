# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/pymca/test/test_k_weight.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 3024 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import os, unittest
from est.core.types import Spectrum, XASObject
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.k_weight import pymca_k_weight
    from est.core.process.pymca.normalization import pymca_normalization
    from est.io.utils.pymca import read_spectrum

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestKWeightSingleSpectrum(unittest.TestCase):
    __doc__ = 'Make sure the process have valid io'

    def setUp(self):
        self.config = {'SET_KWEIGHT':2.0, 
         'EXAFS':{'Knots': {'Values':(1, 2, 5),  'Number':3,  'Orders':[
                     3, 3, 3]}}}
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        energy, mu = read_spectrum(data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj = XASObject(energy=energy, spectra=(self.spectrum,), configuration=(self.config),
          dim1=1,
          dim2=1)

    def testWithXASObjAsInput(self):
        self.xas_obj = pymca_normalization(self.xas_obj)
        pymca_k_weight(xas_obj=(self.xas_obj))

    def testWithDictAsInput(self):
        self.xas_obj = pymca_normalization(self.xas_obj)
        pymca_k_weight(xas_obj=(self.xas_obj.to_dict()))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestKWeightSingleSpectrum,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')