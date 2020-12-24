# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/pymca/test/test_io.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 4228 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import shutil, tempfile, h5py, numpy, os, unittest
from est.core.io import XASWriter
import est.core.io as read_xas
import est.core.utils as spectra_utils
from est.core.types import XASObject
from silx.io.url import DataUrl
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR

class TestReadWrite(unittest.TestCase):
    __doc__ = 'Test read function for spectra and configuration'

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        self.outputfile = os.path.join(self.outputdir, 'output_file.h5')

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    @unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
    def testReadSpectrum(self):
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        res = read_xas(spectra_url=DataUrl(file_path=data_file, scheme='PyMca'),
          channel_url=DataUrl(file_path=data_file, scheme='PyMca'))
        self.assertTrue(isinstance(res, XASObject))
        self.assertEqual(res.n_spectrum, 1)
        self.assertTrue('Mu' in res.spectra[0])
        self.assertTrue('Energy' in res.spectra[0])


class TestNxWriting(unittest.TestCase):
    __doc__ = 'Test that the nx process is correctly store ad the output data'

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        energy, spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.xas_obj = XASObject(spectra=spectra, energy=energy, dim1=20, dim2=10)
        self.h5_file = os.path.join(self.output_dir, 'output_file.h5')

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def testWriteRead(self):
        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(self.xas_obj)
        with h5py.File(self.h5_file, 'r') as (hdf):
            self.assertTrue('scan1' in hdf.keys())
            self.assertTrue('data' in hdf['scan1'].keys())
            self.assertTrue('absorbed_beam' in hdf['scan1'].keys())
            self.assertTrue('monochromator' in hdf['scan1'].keys())
        loaded_xas_obj = XASObject.from_file((self.h5_file), configuration_path=None)
        numpy.testing.assert_allclose(loaded_xas_obj.energy, self.xas_obj.energy)
        numpy.testing.assert_allclose(loaded_xas_obj.absorbed_beam(), self.xas_obj.absorbed_beam())


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReadWrite, TestNxWriting):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')