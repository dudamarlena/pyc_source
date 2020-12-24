# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_reconsparamset_editor.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 3340 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '14/11/2018'
import unittest, numpy
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomwer.gui.reconstruction.ftserie.reconsparamseditor import ReconsParamSetEditor
from tomwer.test.utils import skip_gui_test

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestReconsParamSet(TestCaseQt):
    __doc__ = '\n    Test the ReconsParamSetEditor.\n    Make sure we can iterate over the set of ReconsParams\n    '

    def setUp(self):
        super().setUp()
        self.widget = ReconsParamSetEditor(parent=None)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        super().tearDown()

    def testSeveralPaganin(self):
        iMulti = self.widget._PaganinWidget._qcbpaganin.findText('multi')
        assert iMulti >= 0
        self.widget._PaganinWidget._qcbpaganin.setCurrentIndex(iMulti)
        self.widget._PaganinWidget._qleSigmaBeta.setText('1, 2, 3')
        self.widget._PaganinWidget._qleSigmaBeta.editingFinished.emit()
        self.widget._PaganinWidget._qleSigmaBeta2.setText('0:10:2')
        self.widget._PaganinWidget._qleSigmaBeta2.editingFinished.emit()
        qt.qApp.processEvents()
        reconsParamList = self.widget.getReconsParamSet()
        assert len(reconsParamList) is 15
        combinations = []
        for db in (1, 2, 3):
            num = 5
            for db2 in numpy.linspace(0, 10, num=5, endpoint=True):
                combinations.append((db, db2))

        for param in reconsParamList:
            c = (
             param['PAGANIN']['DB'], param['PAGANIN']['DB2'])
            assert c in combinations
            combinations.remove(c)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReconsParamSet,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')