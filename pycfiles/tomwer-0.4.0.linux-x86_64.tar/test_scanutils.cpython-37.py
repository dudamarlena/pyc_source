# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/test/test_scanutils.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 2418 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '30/09/2019'
import unittest, os, tempfile
from tomwer.core.utils.scanutils import MockHDF5
from tomwer.core.scan.hdf5scan import HDF5TomoScan

class TestMockHDF5(unittest.TestCase):
    __doc__ = 'Test the MockHDF5 file'

    def test_creation(self):
        folder = tempfile.mkdtemp()
        mock = MockHDF5(scan_path=folder, n_radio=100, n_ini_radio=20)
        self.assertEqual(mock.scan_master_file, os.path.join(folder, os.path.basename(folder) + '.h5'))
        tomoScan = HDF5TomoScan(mock.scan_path)
        tomoScan.updateDataset()
        self.assertTrue(tomoScan.get_scan_range() == 360)
        self.assertTrue(len(tomoScan.projections) == 20)
        mock.add_radio()
        self.assertTrue(len(tomoScan.projections) == 21)
        self.assertTrue(tomoScan.get_scan_range() == 360)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestMockHDF5,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')