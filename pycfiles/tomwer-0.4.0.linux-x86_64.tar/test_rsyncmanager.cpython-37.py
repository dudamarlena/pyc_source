# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/test/test_rsyncmanager.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3974 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '17/01/2018'
import filecmp, logging, os, shutil, tempfile, unittest
from tomwer.synctools.rsyncmanager import RSyncManager
from tomwer.test.utils import UtilsTest
logging.disable(logging.INFO)

@unittest.skipIf(RSyncManager().canUseRSync() is False, 'Rsync is missing')
class TestRSyncManager(unittest.TestCase):
    __doc__ = 'Check that the RSyncManager is correctly synchronizing folders.\n    '

    def setUp(self):
        self.topSrcFolder = tempfile.mkdtemp()
        self.topTargetFolder = tempfile.mkdtemp()
        self.dataSetID = 'test01'
        self.dataDir = UtilsTest.getDataset(self.dataSetID)
        self.sourceFolder = os.path.join(self.topSrcFolder, self.dataSetID)
        shutil.copytree(src=(os.path.join(self.dataDir)), dst=(self.sourceFolder))

    def tearDown(self):
        shutil.rmtree(self.topSrcFolder)
        shutil.rmtree(self.topTargetFolder)

    def testSyncFolder(self):
        """Test that a simple sync between two folders are valid"""
        self.assertTrue(len(os.listdir(self.topTargetFolder)) is 0)
        manager = RSyncManager()
        manager.syncFolder(source=(self.sourceFolder), target=(self.topTargetFolder),
          block=True,
          delete=False)
        targetFolder = os.path.join(self.topTargetFolder, self.dataSetID)
        self.assertTrue(len(os.listdir(targetFolder)) == len(os.listdir(self.sourceFolder)))
        self.assertTrue(filecmp.dircmp(targetFolder, self.sourceFolder))
        self.assertTrue(os.path.isdir(self.sourceFolder))

    def testSyncFolderDelete(self):
        """Test that a simple sync between two folders are valid ans source
        folder is correctly deleted"""
        self.assertTrue(len(os.listdir(self.topTargetFolder)) is 0)
        manager = RSyncManager()
        manager.syncFolder(source=(self.sourceFolder), target=(self.topTargetFolder),
          block=True,
          delete=True)
        targetFolder = os.path.join(self.topTargetFolder, self.dataSetID)
        self.assertTrue(len(os.listdir(targetFolder)) == len(os.listdir(self.dataDir)))
        self.assertTrue(filecmp.dircmp(targetFolder, self.sourceFolder))
        self.assertFalse(os.path.isdir(self.sourceFolder))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRSyncManager,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')