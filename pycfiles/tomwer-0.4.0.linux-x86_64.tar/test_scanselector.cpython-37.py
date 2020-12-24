# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_scanselector.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 3041 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/01/2017'
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.test.utils import skip_gui_test
from silx.gui.utils.testutils import TestCaseQt
from tomwer.gui.scanselectorwidget import ScanSelectorWidget
from tomwer.core.utils.scanutils import MockEDF
import shutil, tempfile, unittest, logging
_qapp = QApplicationManager()
logging.disable(logging.INFO)

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestScanSelector(TestCaseQt):
    __doc__ = '\n    Simple test for the ScanSelectorOW\n    '

    def setUp(self):
        self._folder1 = tempfile.mkdtemp()
        self._folder2 = tempfile.mkdtemp()
        self._folder3 = tempfile.mkdtemp()
        for _folder in (self._folder1, self._folder2, self._folder3):
            MockEDF.mockScan(scanID=_folder, nRadio=5, nRecons=5, nPagRecons=0, dim=10)

        self.widget = ScanSelectorWidget(parent=None)

    def tearDown(self):
        shutil.rmtree(self._folder1)
        shutil.rmtree(self._folder2)
        shutil.rmtree(self._folder3)

    def test(self):
        self.widget.add(self._folder1)
        self.widget.add(self._folder2)
        self.widget.add(self._folder3)
        self.assertTrue(self.widget.dataList.length() is 3)
        self.widget.remove(self._folder3)
        self.assertTrue(self.widget.dataList.length() is 2)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanSelector,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')