# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/test/test_viewer.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 5128 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
import logging, shutil, tempfile, unittest
from silx.gui import qt
import orangecontrib.tomwer.widgets.visualization.ImageStackViewerOW as ImageStackViewerOW
from tomwer.core.utils.scanutils import MockEDF
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.core.scan.edfscan import EDFTomoScan
logging.disable(logging.INFO)
_qapp = QApplicationManager()

class TestFilePatterns(unittest.TestCase):
    __doc__ = 'Make sure the viewer recognize each possible file pattern'
    N_ACQUI = 20
    N_RECONS = 4
    N_PAG_RECONS = 2

    @classmethod
    def setUpClass(cls):
        cls.stackViewer = ImageStackViewerOW()
        cls.stackViewer.setAttribute(qt.Qt.WA_DeleteOnClose)

    @classmethod
    def tearDownClass(cls):
        cls.stackViewer.close()
        del cls.stackViewer

    def setUp(self):
        self._folder = tempfile.mkdtemp()
        MockEDF.fastMockAcquisition((self._folder), n_radio=(self.N_ACQUI))

    def tearDown(self):
        shutil.rmtree(self._folder)

    def testAcquisition(self):
        """
        Make sure the viewer is able to found and load the acquisition files
        """
        self.stackViewer.addScan(EDFTomoScan(self._folder))
        radioDict = self.stackViewer.viewer._stackImageViewerRadio.images
        self.assertTrue(radioDict.size() == self.N_ACQUI)

    def testReconsNotPag(self):
        """
        Make sure the viewer is able to found and load the reconstruction files
        """
        MockEDF.mockReconstruction((self._folder), nRecons=(self.N_RECONS))
        self.stackViewer.addScan(EDFTomoScan(self._folder))
        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_RECONS)

    def testReconsPaganin(self):
        """
        Make sure the viewer is able to found and load the paganin recons files
        """
        MockEDF.mockReconstruction((self._folder), nRecons=0,
          nPagRecons=(self.N_PAG_RECONS))
        self.stackViewer.addScan(EDFTomoScan(self._folder))
        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_PAG_RECONS)

    def testAllRecons(self):
        """
        Make sure the viewer is able to found and load the paganin and the
        not paganin reconstruction and display both
        """
        MockEDF.mockReconstruction((self._folder), nRecons=(self.N_RECONS),
          nPagRecons=(self.N_PAG_RECONS))
        self.stackViewer.addScan(EDFTomoScan(self._folder))
        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_RECONS + self.N_PAG_RECONS)

    def testReconsVolFile(self):
        """Make sure the viewer is able to detect .vol file"""
        MockEDF.mockReconstruction((self._folder), nRecons=(self.N_RECONS),
          nPagRecons=0,
          volFile=True)
        self.stackViewer.addScan(EDFTomoScan(self._folder))
        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_RECONS * 2)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFilePatterns,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')