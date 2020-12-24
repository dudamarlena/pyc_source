# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/pymca/test/test_exafs.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 3675 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import os, unittest
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.exafs import pymca_exafs
    from est.io.utils.pymca import read_spectrum
    from est.core.process.pymca.normalization import pymca_normalization
from est.core.types import Spectrum, XASObject

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestEXAFSSingleSpectrum(unittest.TestCase):
    __doc__ = 'Make sure the process have valid io'

    def setUp(self):
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        energy, mu = read_spectrum(data_file)
        spectrum = Spectrum(energy=energy, mu=mu)
        exafs_configuration = {'Knots': {'Values':(1, 2, 5),  'Number':3}}
        configuration = {'EXAFS': exafs_configuration}
        self.input_ = XASObject(energy=energy, spectra=(spectrum,), dim1=1, dim2=1,
          configuration=configuration)
        self.preproc_input_ = pymca_normalization(xas_obj=(self.input_))
        assert 'NormalizedBackground' in self.preproc_input_.spectra[0]
        for spectrum in self.preproc_input_.spectra:
            assert 'NormalizedBackground' in spectrum

    def testPyMcaXASAsInput(self):
        res = pymca_exafs(self.preproc_input_)
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue('EXAFSKValues' in res.spectra[0])
        self.assertTrue('EXAFSSignal' in res.spectra[0])
        self.assertTrue('PostEdgeB' in res.spectra[0])

    def testDictAsInput(self):
        """Test succeed if the input is a dict"""
        assert 'NormalizedBackground' in self.preproc_input_.spectra[0]
        res = pymca_exafs(self.preproc_input_)
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue('EXAFSKValues' in res.spectra[0])
        self.assertTrue('EXAFSSignal' in res.spectra[0])
        self.assertTrue('PostEdgeB' in res.spectra[0])


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestEXAFSSingleSpectrum,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')