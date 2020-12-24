# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/scan/test/test_h5.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 6547 bytes
"""Unit test for the scan defined at the hdf5 format"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '16/09/2019'
import unittest, shutil, os, tempfile
from tomwer.test.utils import UtilsTest
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
import numpy

class HDF5TestBaseClass(unittest.TestCase):
    __doc__ = 'base class for hdf5 unit test'

    def get_dataset(self, hdf5_dataset_name):
        dataset_file = os.path.join(self.test_dir, hdf5_dataset_name)
        o_dataset_file = UtilsTest.getH5Dataset(folderID=hdf5_dataset_name)
        shutil.copy(src=o_dataset_file, dst=dataset_file)
        return dataset_file

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)


class TestHDF5Scan(HDF5TestBaseClass):
    __doc__ = 'Basic test for the hdf5 scan'

    def setUp(self):
        super(TestHDF5Scan, self).setUp()
        self.dataset_file = self.get_dataset('data_test2.h5')
        self.scan = HDF5TomoScan(self.dataset_file)

    def testGeneral(self):
        """some general on the HDF5Scan """
        self.assertEqual(self.scan.master_file, self.dataset_file)
        self.assertEqual(self.scan.path, os.path.dirname(self.dataset_file))
        self.assertEqual(self.scan.type, 'hdf5')
        _dict = self.scan.to_dict()
        scan2 = HDF5TomoScan.from_dict(_dict)
        self.assertEqual(scan2.path, self.scan.path)
        radios_urls = self.scan.getRadioUrls()
        self.assertEqual(len(radios_urls), 100)
        url_1 = radios_urls[0]
        self.assertTrue(url_1.is_valid())
        self.assertFalse(url_1.is_absolute())
        self.assertEquals(url_1.scheme(), 'silx')

    def testFrames(self):
        projections = self.scan.projections
        self.assertEqual(len(projections), 100)

    @unittest.skip('no valid hdf5 acquisition defined yet')
    def testDark(self):
        darks = self.scan.darks
        n_dark = 20
        self.assertEqual(len(darks), n_dark)
        self.assertEqual(self.scan.dark_n, n_dark)

    def testRef(self):
        flats = self.scan.flats
        n_ref = 21
        self.assertEqual(self.scan.get_ref_n(), n_ref)
        self.assertEqual(self.scan.ref_n, n_ref)
        self.assertEqual(self.scan.getFlat(), None)
        data = numpy.arange(4194304)
        data.reshape(2048, 2048)
        self.assertEqual(self.scan.get_ff_interval(), 21)
        with self.assertRaises(NotImplementedError):
            self.scan.flatFieldCorrection(data=data)

    def testReconstruction(self):
        reconstruction = self.scan.reconstructions
        self.assertEqual(len(reconstruction), 0)
        reconsUrls = HDF5TomoScan.getReconstructionsUrls(self.scan)
        self.assertEquals(reconsUrls, [])

    def testAxisUtils(self):
        self.assertEqual(self.scan.scan_range, 360)
        self.assertEqual(self.scan.get_scan_range(), 360)
        self.assertEqual(self.scan.tomo_n, 100)
        self.assertEqual(self.scan.get_tomo_n(), 100)
        proj0_file_path = '../../../../../../users/opid19/W:/clemence/visualtomo/data_test2/tomo0001/tomo_0000.h5'
        radios_urls_evolution = self.scan.getProjectionsUrl()
        self.assertEquals(len(radios_urls_evolution), 100)
        self.assertEquals(radios_urls_evolution[0].file_path(), proj0_file_path)
        self.assertEquals(radios_urls_evolution[0].data_slice(), ('0', ))
        self.assertEquals(radios_urls_evolution[0].data_path(), '/entry_0000/measurement/pcoedge64/data')
        radio_0, radio_180 = self.scan.getRadiosForAxisCalc(CorAngleMode.use_0_180)
        self.assertTrue(radio_0 is not None)
        self.assertTrue(radio_180 is not None)
        self.assertEquals(radio_0.url.data_slice(), ('0', ))
        self.assertEquals(radio_0.url.file_path(), proj0_file_path)
        self.assertEquals(radio_0.url.data_path(), '/entry_0000/measurement/pcoedge64/data')
        proj180_file_path = '../../../../../../users/opid19/W:/clemence/visualtomo/data_test2/tomo0001/tomo_0001.h5'
        self.assertEquals(radio_180.url.data_slice(), ('24', ))
        self.assertEquals(radio_180.url.file_path(), proj180_file_path)
        self.assertEquals(radio_180.url.data_path(), '/entry_0000/measurement/pcoedge64/data')

    def testDarkRefUtils(self):
        self.assertEqual(self.scan.tomo_n, 100)
        self.assertEqual(self.scan.get_pixel_size()[0], 6.5)
        self.assertEqual(self.scan.pixel_size[1], 6.5)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestHDF5Scan,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')