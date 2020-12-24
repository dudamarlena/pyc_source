# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_recpyhstwidget.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 6249 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/01/2017'
import unittest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomwer.core.process.reconstruction.ftseries.params.fastsetupdefineglobals import FastSetupAll
from tomwer.core.utils.pyhstutils import _findPyHSTVersions, _getPyHSTDir
from tomwer.gui.reconstruction.ftserie import FtserieWidget
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.gui.reconstruction.recpyhstwidget import RecPyHSTWidget
from tomwer.synctools.ftseries import QReconsParams
from tomwer.test.utils import skip_gui_test
pyhstVersion = _findPyHSTVersions(_getPyHSTDir())
_qapp = QApplicationManager()

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestRecPyHSTWidget(TestCaseQt):
    __doc__ = 'Make sure the gui is correctly editing the ReconsParam and the\n    RecPyHST class\n    '

    def setUp(self):
        self._recons_params = QReconsParams()
        self.ftserieWidget = FtserieWidget(dir=None, recons_params=(self._recons_params))
        self.ftserieWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget = RecPyHSTWidget(parent=None, recons_params=(self._recons_params.pyhst))
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        assert id(self.ftserieWidget.recons_params.pyhst) == id(self._recons_params.pyhst)
        assert id(self.widget.recons_params) == id(self._recons_params.pyhst)

    def tearDown(self):
        self.widget.close()
        self.ftserieWidget.close()

    @unittest.skipIf(len(pyhstVersion) is 0, 'PyHST2 missing')
    def testUpdating(self):
        """Check behavior of the gui when editing the self.recons_params
        Make sure also that sync with the ftserie is made
        """
        pyhstWidget = self.ftserieWidget.getReconsParamSetEditor()._PyHSTWidget
        isMakeOAR = self.widget.recons_params['MAKE_OAR_FILE']
        self.assertTrue(self.widget._makeOARFileCB.isChecked() == isMakeOAR)
        self.assertTrue(pyhstWidget._makeOARFileCB.isChecked() == isMakeOAR)
        self.widget.recons_params['MAKE_OAR_FILE'] = not isMakeOAR
        self.assertTrue(self.widget._makeOARFileCB.isChecked() != isMakeOAR)
        self.assertTrue(pyhstWidget._makeOARFileCB.isChecked() != isMakeOAR)
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == FastSetupAll.OFFV)
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == FastSetupAll.OFFV)
        self._recons_params['PYHSTEXE']['EXE'] = 'toto'
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == 'toto')
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == 'toto')

    @unittest.skipIf(len(pyhstVersion) is 0, 'PyHST2 missing')
    def testEdition(self):
        """Check behavior of ReconsParam when editing i through the gui"""
        pyhstWidget = self.ftserieWidget.getReconsParamSetEditor()._PyHSTWidget
        oVal = self.widget._makeOARFileCB.isChecked()
        self.assertTrue(oVal == pyhstWidget._makeOARFileCB.isChecked())
        self.widget._makeOARFileCB.setChecked(not oVal)
        self.qapp.processEvents()
        self.assertTrue(self.widget.recons_params['MAKE_OAR_FILE'] != oVal)
        self.assertFalse(oVal == pyhstWidget._makeOARFileCB.isChecked())
        pyhstWidget._makeOARFileCB.setChecked(oVal)
        self.assertTrue(self.widget._makeOARFileCB.isChecked() == oVal)
        self.assertTrue(self.widget.recons_params['MAKE_OAR_FILE'] == oVal)
        oExe = self.widget.recons_params['EXE'] = 'toto'
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == oExe)
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == oExe)
        self.widget._qcbPyHSTVersion.addItem('toto')
        iToto = self.widget._qcbPyHSTVersion.findText('toto')
        self.assertTrue(iToto > 0)
        self.widget._qcbPyHSTVersion.setCurrentIndex(iToto)
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == 'toto')
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == 'toto')
        self.assertTrue(self.widget.recons_params['EXE'] == 'toto')
        iOExe = self.widget._qcbPyHSTVersion.findText(oExe)
        self.assertTrue(iOExe > 0)
        pyhstWidget._qcbPyHSTVersion.setCurrentIndex(iOExe)
        self.assertTrue(self.widget._qcbPyHSTVersion.currentText() == oExe)
        self.assertTrue(pyhstWidget._qcbPyHSTVersion.currentText() == oExe)
        self.assertTrue(self.widget.recons_params['EXE'] == oExe)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRecPyHSTWidget,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')