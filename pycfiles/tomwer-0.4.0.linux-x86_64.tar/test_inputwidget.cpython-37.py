# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_inputwidget.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 3309 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '16/08/2018'
from tomwer.gui.utils import inputwidget
from tomwer.test.utils import skip_gui_test
from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
import unittest, numpy

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class SelectionLineEditTest(TestCaseQt):
    __doc__ = 'Test the SelectionLineEdit'

    def setUp(self):
        super().setUp()
        self.widget = inputwidget.SelectionLineEdit(parent=None)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        super().tearDown()

    def testListSelection(self):
        self.widget.mode = inputwidget.SelectionLineEdit.LIST_MODE
        self.widget.setText('1.0, 2.0; 6.3')
        self.assertTrue(self.widget.selection == (1.0, 2.0, 6.3))
        self.widget.setText('1.0:3.6:0.2')
        self.assertTrue(self.widget.selection == tuple(numpy.linspace(1.0, 3.6, num=(int(13.0)))))
        self.assertTrue(self.widget.getMode() == inputwidget.SelectionLineEdit.RANGE_MODE)
        self.widget.setText('1.0')
        self.assertTrue(self.widget.selection == 1.0)

    def testRangeSelection(self):
        self.widget.mode = inputwidget.SelectionLineEdit.RANGE_MODE
        self.widget.setText('1.0:3.6:0.2')
        self.assertTrue(self.widget.selection == tuple(numpy.linspace(1.0, 3.6, num=(int(13.0)))))
        self.widget.setText('1.0')
        self.assertTrue(self.widget.selection == 1.0)
        self.widget.setText('1.0, 2.0, 6.3')
        self.assertTrue(self.widget.getMode() == inputwidget.SelectionLineEdit.LIST_MODE)
        self.assertTrue(self.widget.selection == (1.0, 2.0, 6.3))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (SelectionLineEditTest,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')