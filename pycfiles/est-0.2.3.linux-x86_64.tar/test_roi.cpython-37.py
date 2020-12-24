# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/process/test/test_roi.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 3963 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import os, shutil, tempfile, unittest, h5py, numpy
from silx.io.url import DataUrl
import est.core.io as read_xas
from est.core.process.roi import xas_roi
import est.core.utils as spectra_utils

class TestRoi(unittest.TestCase):

    def setUp(self):
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(16, 100, 30))
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

    def testApplyRoi(self):
        """Test output of the roi process"""
        original_spectra = self.xas_obj._spectra_volume(spectra=(self.xas_obj.spectra), key='mu',
          dim_1=(self.xas_obj.dim1),
          dim_2=(self.xas_obj.dim2)).copy()
        assert original_spectra.shape == (16, 100, 30)
        roi_dict = {'origin':(20, 50),  'size':(10, 20)}
        self.xas_obj.configuration = {'roi': roi_dict}
        res_xas_obj = xas_roi(self.xas_obj)
        self.assertEqual(res_xas_obj.n_spectrum, 200)
        reduces_spectra = res_xas_obj._spectra_volume(spectra=(res_xas_obj.spectra), key='mu',
          dim_1=(res_xas_obj.dim1),
          dim_2=(res_xas_obj.dim2)).copy()
        assert reduces_spectra.shape == (16, 20, 10)
        numpy.testing.assert_array_equal(original_spectra[:, 50:70, 20:30], reduces_spectra)

    def testWorkflowWithRoi(self):
        """"""
        pass


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRoi,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')