# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/test/test_lamino.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 8381 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '14/11/2018'
import os, shutil, tempfile, unittest
from silx.gui import qt
from tomwer.core import settings
from tomwer.gui.reconstruction.lamino.tofu import TofuWindow
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestLamino(unittest.TestCase):
    __doc__ = 'Test the TofuWidget'

    def setUp(self):
        super().setUp()
        self._window = TofuWindow(parent=None)
        self._widget = self._window._mainWidget
        self._folder = tempfile.mkdtemp()

    def tearDown(self):
        super().tearDown()
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        shutil.rmtree(self._folder)

    def testSetup(self):
        """Make sure the widget is correctly setting parameters from a scan"""
        dataset = UtilsTest.getDataset('test01')
        self._window.loadFromScan(dataset)
        reconsParams = self._widget.getParameters()
        self.assertTrue(self._widget._tabs._inputWidget.getNumber() == 1)
        self.assertTrue(reconsParams['number'] == 1)
        ffcWidget = self._widget._tabs._inputWidget.widget._ffcWidget
        thFlats = os.path.join(dataset, 'refHST0000.edf')
        print(ffcWidget.getFlats())
        self.assertTrue(ffcWidget.getFlats() == thFlats)
        self.assertTrue(reconsParams['flats'] == thFlats)
        thSecondFlats = os.path.join(dataset, 'refHST0010.edf')
        self.assertTrue(ffcWidget.getSecondFlats() == thSecondFlats)
        self.assertTrue(reconsParams['flats2'] == thSecondFlats)
        thDarks = os.path.join(dataset, 'darkend0000.edf')
        self.assertTrue(ffcWidget.getDarks() == thDarks)
        self.assertTrue(reconsParams['darks'] == thDarks)
        inputWidget = self._widget._tabs._inputWidget.widget
        self.assertTrue(inputWidget.rotationAngle._overallAngle.getAngle() == 180.0)
        self.assertTrue(inputWidget.rotationAngle._axisAngleY.getAngle() == 0.0)
        self.assertTrue(inputWidget.rotationAngle._axisAngleZ.getAngle() == 0.0)

    def testSetupWithLockedParams(self):
        """Make sure lockers are corrcetly taking into account"""
        inputWidget = self._widget._tabs._inputWidget.widget
        inputWidget.rotationAngle._overallAngle.setAngle(12.0)
        inputWidget.rotationAngle._overallAngle.lock()
        inputWidget.rotationAngle._axisAngleY.setAngle(-26.0)
        inputWidget.rotationAngle._axisAngleY.lock()
        inputWidget.rotationAngle._axisAngleZ.setAngle(63.5)
        inputWidget.rotationAngle._axisAngleZ.lock()
        outputWidget = self._widget._tabs._outputWidget
        outputWidget.setOutput('toto')
        outputWidget.lockOutput()
        dataset = UtilsTest.getDataset('test01')
        self._window.loadFromScan(dataset)
        self.assertTrue(inputWidget.rotationAngle._overallAngle.getAngle() == 12.0)
        self.assertTrue(inputWidget.rotationAngle._axisAngleY.getAngle() == -26.0)
        self.assertTrue(inputWidget.rotationAngle._axisAngleZ.getAngle() == 63.5)
        self.assertTrue(outputWidget.getOutput() == 'toto')

    def testEditionDisplay(self):
        """
        Test that edition of parameters by the user are taking into account
        """
        displayWidget = self._widget._tabs._inputWidget.widget.rotationAngle
        displayWidget._laminoAngle.setAngle(12.0)
        self.assertTrue(self._widget.getParameters()['axis-angle-x'] == 12.0)
        displayWidget._axisAngleY.setAngle(10.0)
        self.assertTrue(self._widget.getParameters()['axis-angle-y'] == 10.0)
        regionWidget = self._widget._tabs._outputWidget._region
        regionWidget._xRegion._regionLE.setText('0')
        self.assertTrue(self._widget.getParameters()['x-region'] == (0, -1, 1))
        regionWidget.setYRegion(10, 12, 25)
        self.assertTrue(self._widget.getParameters()['y-region'] == (10, 12, 25))
        savingFile = os.path.join(self._folder, 'savingFile.ini')
        self._widget.saveTo(savingFile)
        self.assertTrue(os.path.exists(savingFile))
        regionWidget.setYRegion(10, 12, 22)
        self.assertTrue(self._widget.getParameters()['y-region'] == (10, 12, 22))
        self._widget.loadFile(savingFile)
        self.assertTrue(self._widget.getParameters()['y-region'] == (10, 12, 25))

    def testOutputWidget(self):
        """ test behavior of the output widget and link with get and set
        parameters"""
        outputWidget = self._widget._tabs._outputWidget
        outputWidget._volumeAngleGrp.setAngles(0, 20, -36.0)
        reconsParams = self._widget.getParameters()
        self.assertTrue(reconsParams['volume-angle-x'] == 0)
        self.assertTrue(reconsParams['volume-angle-y'] == 20.0)
        self.assertTrue(reconsParams['volume-angle-z'] == -36.0)

    def testCenteringWidget(self):
        """ test behavior of the centering widget and link with get and set
        parameters"""
        centeringWidget = self._widget._tabs._inputWidget.widget.centeringWidget
        centeringWidget._xCenterLE.setText('12')
        centeringWidget._yCenterLE.setText('2')
        self.assertTrue(self._widget.getParameters()['center-position-x'] == 12.0)
        self.assertTrue(self._widget.getParameters()['center-position-z'] == 2.0)

    def testForceLbsRam(self):
        """Test the behavior of the forcelbsram option"""
        scan1 = tempfile.mkdtemp(suffix='1')
        self._window.loadFromScan(scan1)
        _end = os.path.join('1', 'xySlice')
        self.assertTrue(self._window.getParameters()['output'].endswith(_end))
        self._window._mainWidget._tabs._outputWidget.lockOutput()
        scan2 = tempfile.mkdtemp(suffix='2')
        self._window.loadFromScan(scan2)
        _end = os.path.join('1', 'xySlice')
        self.assertTrue(self._window.getParameters()['output'].endswith(_end))
        self._window._mainWidget._tabs._outputWidget.lockOutput(False)
        self._window.loadFromScan(scan2)
        _end = os.path.join('2', 'xySlice')
        self.assertTrue(self._window.getParameters()['output'].endswith(_end))
        self._window._mainWidget._tabs._outputWidget.setForceLbsram(True)
        self.assertTrue(self._window.getParameters()['output'].startswith(settings.get_lbsram_path()))
        self._window.loadFromScan(scan1)
        self.assertTrue(self._window.getParameters()['output'].startswith(settings.get_lbsram_path()))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestLamino,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')