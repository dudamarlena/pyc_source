# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/pymca/test/test_normalization.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 5128 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import os, shutil, tempfile, unittest, h5py, numpy
from silx.io.url import DataUrl
import est.core.io as read_xas
from est.core.types import Spectrum, XASObject
import est.core.utils as spectra_utils
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.normalization import pymca_normalization
    from est.io.utils.pymca import read_spectrum

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestNormalizationSingleSpectrum(unittest.TestCase):
    __doc__ = 'Make sure the process is processing correctly on a spectrum'

    def setUp(self):
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        energy, mu = read_spectrum(data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj = XASObject(spectra=(self.spectrum,), energy=energy, dim1=1,
          dim2=1)

    def testWithXASObjAsInput(self):
        res = pymca_normalization(xas_obj=(self.xas_obj))
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue(isinstance(res.spectra, (tuple, list)))
        res_spectrum = res.spectra[0]
        self.assertTrue(isinstance(res_spectrum, Spectrum))
        self.assertTrue('NormalizedMu' in res_spectrum)
        self.assertTrue('NormalizedEnergy' in res_spectrum)
        self.assertTrue('NormalizedSignal' in res_spectrum)

    def testWithDictAsInput(self):
        res = pymca_normalization(xas_obj=(self.xas_obj.to_dict()))
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue('NormalizedMu' in res.spectra[0])
        self.assertTrue('NormalizedEnergy' in res.spectra[0])
        self.assertTrue('NormalizedSignal' in res.spectra[0])


@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestNormalizationMultipleSpectrum(unittest.TestCase):
    __doc__ = 'Make sure the process is processing correctly on a XASObject spectra'

    def setUp(self):
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.output_dir = tempfile.mkdtemp()
        spectra_path = '/data/NXdata/data'
        channel_path = '/data/NXdata/Channel'
        filename = os.path.join(self.output_dir, 'myfile.h5')
        with h5py.File(filename, 'w') as (f):
            f[spectra_path] = self.spectra
            f[channel_path] = self.energy
        self.xas_obj = read_xas(spectra_url=DataUrl(file_path=filename, data_path=spectra_path,
          scheme='silx'),
          channel_url=DataUrl(file_path=filename, data_path=channel_path,
          scheme='silx'))

    def tearDown(self):
        shutil.rmtree(path=(self.output_dir))

    def testWithXASObjAsInput(self):
        res = pymca_normalization(xas_obj=(self.xas_obj))
        self.assertTrue(isinstance(res, XASObject))
        for spectrum in self.xas_obj.spectra:
            self.assertTrue('NormalizedMu' in spectrum)
            self.assertTrue('NormalizedEnergy' in spectrum)
            self.assertTrue('NormalizedSignal' in spectrum)

    def testWithDictAsInput(self):
        pass


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestNormalizationSingleSpectrum,
     TestNormalizationMultipleSpectrum):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')