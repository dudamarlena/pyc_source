# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/larch/test/test_xftf.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 5662 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/25/2019'
import os, unittest, tempfile, shutil, urllib.request
from est.core.types import Spectrum, XASObject
try:
    import larch
except ImportError:
    has_larch = False
else:
    has_larch = True
    from est.core.process.larch.xftf import larch_xftf, process_spectr_xftf
    from est.core.process.larch.autobk import process_spectr_autobk
    from est.io.utils.larch import read_ascii

@unittest.skipIf(has_larch is False, 'xraylarch not installed')
class TestLarchSpectrum(unittest.TestCase):
    __doc__ = 'Make sure computation on one spectrum is valid'

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        xmu_url = 'https://raw.githubusercontent.com/xraypy/xraylarch/master/examples/xafs/cu_rt01.xmu'
        self.data_file = os.path.join(self.outputdir, 'cu_rt01.xmu')
        with urllib.request.urlopen(xmu_url) as (response):
            with open(self.data_file, 'wb') as (out_file):
                data = response.read()
                out_file.write(data)
        assert os.path.exists(self.data_file)
        energy, mu = read_ascii(self.data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.configuration = {'window':'hanning',  'kweight':2,  'kmin':3,  'kmax':13, 
         'dk':1}
        process_spectr_autobk((self.spectrum), configuration={}, overwrite=True)
        assert hasattr(self.spectrum, 'k')
        assert hasattr(self.spectrum, 'chi')

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcess(self):
        process_spectr_xftf((self.spectrum), (self.configuration), overwrite=True)
        self.assertTrue(hasattr(self.spectrum, 'chir_re'))
        self.assertTrue(hasattr(self.spectrum, 'chir_im'))
        self.assertTrue(hasattr(self.spectrum, 'chir'))
        self.assertTrue(hasattr(self.spectrum, 'chir_mag'))


@unittest.skipIf(has_larch is False, 'xraylarch not installed')
class TestLarchSpectra(unittest.TestCase):
    __doc__ = 'Make sure computation on spectra is valid (n spectrum)'

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        xmu_url = 'https://raw.githubusercontent.com/xraypy/xraylarch/master/examples/xafs/cu_rt01.xmu'
        self.data_file = os.path.join(self.outputdir, 'cu_rt01.xmu')
        with urllib.request.urlopen(xmu_url) as (response):
            with open(self.data_file, 'wb') as (out_file):
                data = response.read()
                out_file.write(data)
        assert os.path.exists(self.data_file)
        self.configuration = {'z': 29}
        energy, mu = read_ascii(self.data_file)
        spectrum = Spectrum(energy=energy, mu=mu)
        process_spectr_autobk(spectrum, configuration={}, overwrite=True)
        self.xas_object = XASObject(spectra=(spectrum,), energy=energy,
          dim1=1,
          dim2=1,
          configuration=(self.configuration))
        spectrum = self.xas_object.spectra[0]
        assert hasattr(spectrum, 'k')
        assert hasattr(spectrum, 'chi')

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcessXASObject(self):
        res = larch_xftf(self.xas_object)
        assert isinstance(res, XASObject)
        spectrum = res.spectra[0]
        self.assertTrue(hasattr(spectrum, 'chir_re'))
        self.assertTrue(hasattr(spectrum, 'chir_im'))
        self.assertTrue(hasattr(spectrum, 'chir'))
        self.assertTrue(hasattr(spectrum, 'chir_mag'))

    def testProcessAsDict(self):
        res = larch_xftf(self.xas_object.to_dict())
        assert isinstance(res, XASObject)
        spectrum = res.spectra[0]
        self.assertTrue(hasattr(spectrum, 'chir_re'))
        self.assertTrue(hasattr(spectrum, 'chir_im'))
        self.assertTrue(hasattr(spectrum, 'chir'))
        self.assertTrue(hasattr(spectrum, 'chir_mag'))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestLarchSpectrum, TestLarchSpectra):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')