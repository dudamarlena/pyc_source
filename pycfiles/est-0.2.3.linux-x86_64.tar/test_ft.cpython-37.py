# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/pymca/test/test_ft.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 3468 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import os, unittest
from est.core.types import XASObject, Spectrum
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.exafs import pymca_exafs
    from est.core.process.pymca.ft import pymca_ft
    from est.core.process.pymca.k_weight import pymca_k_weight
    from est.core.process.pymca.normalization import pymca_normalization
    from est.io.utils.pymca import read_spectrum

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestFTSingleSpectrum(unittest.TestCase):
    __doc__ = 'Make sure the process have valid io'

    def setUp(self):
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        energy, mu = read_spectrum(data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj = XASObject(energy=energy, spectra=(self.spectrum,), dim1=1,
          dim2=1)
        self.xas_obj = pymca_normalization(xas_obj=(self.xas_obj))
        self.xas_obj = pymca_exafs(xas_obj=(self.xas_obj))
        self.xas_obj = pymca_k_weight(xas_obj=(self.xas_obj))

    def testPyMcaXASAsInput(self):
        res = pymca_ft(xas_obj=(self.xas_obj))
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue('FTRadius' in res.spectra[0]['FT'])
        self.assertTrue('FTImaginary' in res.spectra[0]['FT'])
        self.assertTrue('FTIntensity' in res.spectra[0]['FT'])

    def testDictAsInput(self):
        res = pymca_ft(xas_obj=(self.xas_obj.to_dict()))
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue('FTRadius' in res.spectra[0]['FT'])
        self.assertTrue('FTImaginary' in res.spectra[0]['FT'])
        self.assertTrue('FTIntensity' in res.spectra[0]['FT'])


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFTSingleSpectrum,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')