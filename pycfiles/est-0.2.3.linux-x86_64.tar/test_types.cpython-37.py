# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/test/test_types.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 5802 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/26/2019'
import numpy, os, unittest, tempfile, h5py
from est.core.types import Spectrum, XASObject
import est.core.utils as spectra_utils
import est.core.io as read_xas
from silx.io.url import DataUrl
import silx.io.utils
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.io.utils.pymca import read_spectrum

class TestSpectrum(unittest.TestCase):
    __doc__ = 'Test the spectrum class'

    @unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
    def test_from_dat(self):
        """check that we can create a Spectrum from a pymca .dat file"""
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        energy, mu = read_spectrum(data_file)
        spectrum = Spectrum(energy=energy, mu=mu)
        self.assertTrue(spectrum.energy is not None)
        self.assertTrue(spectrum.mu is not None)

    def test_from_numpy_array(self):
        """check that we can create a Spectrum from numpy arrays"""
        energy = numpy.arange(10, 20)
        mu = numpy.arange(10)
        spectrum = Spectrum(energy=energy, mu=mu)
        numpy.testing.assert_array_equal(spectrum.energy, energy)
        numpy.testing.assert_array_equal(spectrum.mu, mu)
        mu_2 = numpy.arange(30, 40)
        spectrum['Mu'] = mu_2
        numpy.testing.assert_array_equal(spectrum.mu, mu_2)


class TestXASObject(unittest.TestCase):
    __doc__ = 'test construction of XAS object from a single spectra'

    @unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
    def test_create_from_single_spectrum(self):
        """check that we can create a XASObject from a pymca .dat file"""
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        spectrum = {}
        spectrum['Energy'], spectrum['Mu'] = read_spectrum(data_file)
        self.spectrum = Spectrum(energy=(spectrum['Energy']), mu=(spectrum['Mu']))
        self.configuration = {'FT':{'KWeight': 1}, 
         'EXAFS':{'EXAFSNormalized': numpy.array([1, 2, 3])}}
        obj = XASObject(spectra=(self.spectrum,), energy=(self.spectrum.energy),
          configuration=(self.configuration),
          dim1=1,
          dim2=1)
        self.assertEqual(obj.n_spectrum, 1)
        ddict = obj.to_dict()
        obj2 = XASObject.from_dict(ddict)
        self.assertEqual(obj2, obj)

    def test_create_from_several_spectrums(self):
        """check that we can create a XASObject from numpy arrays"""
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.output_dir = tempfile.mkdtemp()
        spectra_path = '/data/NXdata/data'
        channel_path = '/data/NXdata/Channel'
        filename = os.path.join(self.output_dir, 'myfile.h5')
        with h5py.File(filename, 'w') as (f):
            f[spectra_path] = self.spectra
            f[channel_path] = self.energy
        url_spectra = DataUrl(file_path=filename, data_path=spectra_path,
          scheme='silx')
        self.xas_obj = read_xas(spectra_url=url_spectra, channel_url=DataUrl(file_path=filename, data_path=channel_path,
          scheme='silx'))
        self.assertEqual(self.xas_obj.dim1, 20)
        self.assertEqual(self.xas_obj.dim2, 10)
        self.assertEqual(self.xas_obj.n_spectrum, 200)
        ddict = self.xas_obj.to_dict(with_process_details=False)
        original_spectra = silx.io.utils.get_data(DataUrl(file_path=filename, data_path=spectra_path,
          scheme='silx'))
        numpy.testing.assert_array_equal(original_spectra, ddict['spectra'])
        obj2 = XASObject.from_dict(ddict)
        self.assertEqual(self.xas_obj.n_spectrum, obj2.n_spectrum)
        self.assertEqual(obj2, self.xas_obj)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSpectrum, TestXASObject):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')