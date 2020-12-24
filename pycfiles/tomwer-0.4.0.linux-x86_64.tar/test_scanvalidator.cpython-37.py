# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_scanvalidator.py
# Compiled at: 2020-01-10 04:27:31
# Size of source mod 2**32: 3905 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
import logging, os, shutil, tempfile, time, unittest
from tomwer.core import settings
from tomwer.core import utils
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.process.scanvalidator import ScanValidatorP
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.gui.utils.waiterthread import QWaiterThread
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.test.utils import skip_gui_test
logging.disable(logging.INFO)
_qapp = QApplicationManager()

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestScanValidator(unittest.TestCase):
    __doc__ = '\n    Simple test to make sure the timeout of data watcher is working properly\n    '
    LOOP_MEM_RELEASER_DURATION = 0.2
    NB_SCANS = 2

    @classmethod
    def setUpClass(cls):
        settings.mock_lsbram(True)
        cls.scanValidator = ScanValidatorP(memoryReleaser=(QWaiterThread(0.5)))
        cls.scans = []
        for iScan in range(cls.NB_SCANS):
            scanID = tempfile.mkdtemp()
            MockEDF.mockScan(scanID=scanID, nRadio=10,
              nRecons=2,
              nPagRecons=0,
              dim=10)
            cls.scans.append(scanID)

    @classmethod
    def tearDownClass(cls):
        settings.mock_lsbram(False)
        utils.mockLowMemory(False)
        for f in cls.scans:
            if os.path.isdir(f):
                shutil.rmtree(f)

    @unittest.skipIf(settings.isOnLbsram() and utils.isLowOnMemory(settings.get_lbsram_path()), 'Lbsram already overloaded')
    def testMemoryReleaseLoop(self):
        """
        Make sure the internal loop of the scan validator is active if we are
        on lbsram.
        """
        for scan in self.scans:
            self.scanValidator.addScan(EDFTomoScan(scan))

        self.assertTrue(len(self.scanValidator._scansToValidate) is self.NB_SCANS)
        utils.mockLowMemory(True)
        for i in range(3):
            while _qapp.hasPendingEvents():
                _qapp.processEvents()

            time.sleep(self.LOOP_MEM_RELEASER_DURATION * 2)

        self.assertTrue(len(self.scanValidator._scansToValidate) is 0)
        utils.mockLowMemory(False)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanValidator,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')