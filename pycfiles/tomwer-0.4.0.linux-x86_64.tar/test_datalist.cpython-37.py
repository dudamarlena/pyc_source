# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_datalist.py
# Compiled at: 2020-01-08 09:31:39
# Size of source mod 2**32: 3200 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/11/2018'
from tomwer.gui.datalist import DataListDialog
from tomwer.test.utils import skip_gui_test
from silx.gui.utils.testutils import TestCaseQt
from tomwer.core.utils.scanutils import MockEDF
from silx.gui import qt
import unittest, tempfile

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class DataListTest(TestCaseQt):
    __doc__ = 'Test that the datalist widget work correctly'

    def setUp(self):
        super().setUp()
        self.widget = DataListDialog(parent=None)
        self.widget._callbackRemoveAllFolders()
        self.widget.clear()
        assert self.widget.length() is 0
        self._folders = []
        for iFolder in range(5):
            self._folders.append(tempfile.mkdtemp())
            MockEDF.mockScan(scanID=(self._folders[(-1)]), nRadio=5, nRecons=5, nPagRecons=0,
              dim=10)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        self._folders = None
        super().tearDown()

    def test(self):
        """simple test adding and removing folders"""
        for _folder in self._folders:
            self.widget.add(_folder)

        self.assertEqual(self.widget.length(), len(self._folders))
        self.widget.remove(self._folders[0])
        self.assertEqual(self.widget.length(), len(self._folders) - 1)
        self.assertTrue(self._folders[0] not in self.widget.datalist._scanIDs)
        self.widget.selectAll()
        self.widget._callbackRemoveFolder()
        self.assertEqual(self.widget.length(), 0)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (DataListTest,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')