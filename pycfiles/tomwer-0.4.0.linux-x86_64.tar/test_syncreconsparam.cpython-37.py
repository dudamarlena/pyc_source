# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_syncreconsparam.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 5335 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/01/2017'
import unittest
from silx.gui import qt
import tomwer.core.process.reconstruction.darkref.params as DkrfMethod
from tomwer.gui.reconstruction.ftserie import FtserieWidget
from tomwer.gui.reconstruction.darkref.darkrefcopywidget import DarkRefAndCopyWidget
from tomwer.synctools.ftseries import QReconsParams
from tomwer.test.utils import skip_gui_test

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestReconsParamFtSerieDarkRef(unittest.TestCase):
    __doc__ = 'Test that the FtSerie and Dark Ref instances are synchronized\n    both with the ReconsParam instance'

    def setUp(self):
        self.recons_params = QReconsParams()
        self._ftserie = FtserieWidget(dir=None, parent=None, recons_params=(self.recons_params))
        self._darkRefCopy = DarkRefAndCopyWidget(parent=None, reconsparams=(self.recons_params))
        self.qapp = qt.QApplication.instance() or qt.QApplication([])

    def tearDown(self):
        self._ftserie.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._darkRefCopy.setAttribute(qt.Qt.WA_DeleteOnClose)

    def testSync(self):
        """Make sure that connection between dkrf and ftserie are made.
        Some individual test (ftserie and ReconsParams) are also existing"""
        self._ftserie.show()
        self._darkRefCopy.show()
        ftserieEditor = self._ftserie.getReconsParamSetEditor()
        ftserieDKRf = ftserieEditor._dkRefWidget
        dkrfSkip = self._darkRefCopy.mainWidget.tabGeneral._skipOptionCB
        skipping = ftserieDKRf._qcbSkipRef.isChecked()
        self.assertTrue(dkrfSkip.isChecked() is skipping)
        self.assertTrue(self._ftserie.recons_params.dkrf['REFSOVE'] is not skipping)
        self.assertTrue(self._ftserie.recons_params.dkrf['DARKOVE'] is not skipping)
        ftserieDKRf._qcbSkipRef.setChecked(not skipping)
        self.qapp.processEvents()
        self.assertTrue(dkrfSkip.isChecked() is not skipping)
        self.assertTrue(self._ftserie.recons_params.dkrf['REFSOVE'] is skipping)
        self.assertTrue(self._ftserie.recons_params.dkrf['DARKOVE'] is skipping)
        ftserieRef = ftserieEditor._dkRefWidget._qleDKPattern
        dkrfRef = self._darkRefCopy.mainWidget.tabExpert._darkLE
        self.assertTrue(dkrfRef.text() == ftserieRef.text())
        self.assertTrue(dkrfRef.text() == self._ftserie.recons_params.dkrf['DKFILE'])
        txt = dkrfRef.text()
        dkrfRef.setText(txt + 'toto')
        dkrfRef.editingFinished.emit()
        self.qapp.processEvents()
        self.assertTrue(self.recons_params.dkrf['DKFILE'] == txt + 'toto')
        self.assertTrue(dkrfRef.text() == ftserieRef.text())
        self.assertTrue(dkrfRef.text() == self._ftserie.recons_params.dkrf['DKFILE'])
        ftserieRef.setText(txt + 'tata')
        ftserieRef.editingFinished.emit()
        self.assertTrue(dkrfRef.text() == ftserieRef.text())
        self.assertTrue(dkrfRef.text() == self._ftserie.recons_params.dkrf['DKFILE'])
        ftserieWhatDark = ftserieEditor._dkRefWidget._qcbDKMode
        dkrfWhatDark = self._darkRefCopy.mainWidget.tabGeneral._darkWCB
        self.assertTrue(ftserieWhatDark.getMode() == dkrfWhatDark.getMode())
        for mode in DkrfMethod:
            ftserieWhatDark.setMode(mode)
            self.assertTrue(dkrfWhatDark.getMode() == mode)
            self.assertTrue(self._ftserie.recons_params.dkrf['DARKCAL'] == mode)

        for mode in DkrfMethod:
            dkrfWhatDark.setMode(mode)
            self.assertTrue(ftserieWhatDark.getMode() == mode)
            self.assertTrue(self._ftserie.recons_params.dkrf['DARKCAL'] == mode)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReconsParamFtSerieDarkRef,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')