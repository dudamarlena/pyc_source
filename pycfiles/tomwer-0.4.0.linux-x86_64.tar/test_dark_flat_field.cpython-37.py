# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/test/test_dark_flat_field.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 7642 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '09/02/2018'
import logging, os, shutil, tempfile, time, unittest
from glob import glob
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.core import utils
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.settings import mock_lsbram
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test
from silx.gui.utils.testutils import SignalListener
logging.disable(logging.INFO)

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
@unittest.skip('Fail on CI')
class TestConstructionDarkAndFlatField(OrangeWorflowTest):
    __doc__ = '\n    test the workflow composed of the following widgets :\n        - DataWatcherOW\n        - DarkRefsCopy : Make sure the refCopy is correctly make\n    '
    TIMEOUT = 20

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        cls.nodeDataWatcher = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataWatcherOW.DataWatcherOW')
        cls.nodeDarkRefs = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW.DarkRefAndCopyOW')
        cls.darkRefListener = SignalListener()
        cls.datawatcherListener = SignalListener()
        cls.processOrangeEvents(cls)
        cls.link(cls, cls.nodeDataWatcher, 'data', cls.nodeDarkRefs, 'data')
        cls.processOrangeEvents(cls)
        cls.datawatcherWidget = cls.getWidgetForNode(cls, cls.nodeDataWatcher)
        cls.darkRefsWidget = cls.getWidgetForNode(cls, cls.nodeDarkRefs)
        cls.datawatcherWidget.displayAdvancement = False
        cls.darkRefsWidget.setForceSync(True)
        cls.darkRefsWidget.widget.sigScanReady.connect(cls.darkRefListener)
        cls.datawatcherWidget._widget.sigScanReady.connect(cls.datawatcherListener)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeDataWatcher, cls.nodeDarkRefs):
            cls.removeNode(cls, node)

        cls.app.processEvents()
        del cls.datawatcherWidget
        del cls.darkRefsWidget
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)

        def prepareRefFolder():
            datasetID = 'test10'
            self.inputFolder = tempfile.mkdtemp()
            self.scanFolder = os.path.join(self.inputFolder, datasetID)
            self.copytree = shutil.copytree(src=(UtilsTest().getDataset(datasetID)),
              dst=(self.scanFolder))
            [os.remove(f) for f in DarkRefs.getRefHSTFiles((self.scanFolder), prefix='refHST')]
            [os.remove(f) for f in DarkRefs.getDarkHSTFiles((self.scanFolder), prefix='darkHST')]

        prepareRefFolder()

        def prepareScanToProcess():
            self._refParentFolder = tempfile.mkdtemp()
            datasetRef = 'test01'
            self.refFolder = os.path.join(self._refParentFolder, datasetRef)
            shutil.copytree(src=(UtilsTest().getDataset(datasetRef)), dst=(self.refFolder))
            shutil.copyfile(src=(os.path.join(self._refParentFolder, 'test01', 'test01.info')),
              dst=(os.path.join(self.scanFolder, 'test10.info')))
            assert len(glob(os.path.join(self.refFolder, 'refHST*'))) > 0
            dark_HST = os.path.join(self.refFolder, 'darkHST0000.edf')
            if os.path.exists(dark_HST):
                os.rename(dark_HST, os.path.join(self.refFolder, 'dark.edf'))
            assert len(glob(os.path.join(self.refFolder, 'dark.edf'))) == 1

        prepareScanToProcess()
        self.datawatcherWidget.setFolderObserved(self.inputFolder)
        self.darkRefsWidget.recons_params._set_skip_if_exist(True)
        self.darkRefsWidget.setRefsFromScan(self.refFolder)
        self.darkRefsWidget.setModeAuto(False)
        utils.mockLowMemory(False)
        mock_lsbram(True)
        self.darkRefListener.clear()
        self.datawatcherListener.clear()

    def tearDown(self):
        self.datawatcherWidget._widget.stop()
        shutil.rmtree(self._refParentFolder)
        shutil.rmtree(self.inputFolder)
        OrangeWorflowTest.tearDown(self)

    def testWorkflow(self):
        assert not self.datawatcherWidget._widget.isObserving
        self.datawatcherWidget.startObservation()
        timeout = TestConstructionDarkAndFlatField.TIMEOUT
        while self.datawatcherListener.callCount() < 1 and timeout > 0:
            self.app.processEvents()
            timeout -= 0.2
            time.sleep(0.2)

        if timeout < 0:
            raise TimeoutError("data watcher can't find any scan")
        timeout = TestConstructionDarkAndFlatField.TIMEOUT
        while timeout > 0 and self.darkRefListener.callCount() < 1:
            self.app.processEvents()
            timeout -= 0.2
            time.sleep(0.2)

        self.app.processEvents()
        if timeout < 0:
            raise TimeoutError("darkef didn't process")
        self.assertTrue(len(DarkRefs.getDarkHSTFiles((self.scanFolder), prefix='refHST')) > 0)
        self.assertTrue(len(DarkRefs.getRefHSTFiles((self.scanFolder), prefix='dark.edf')) > 0)
        while self.app.hasPendingEvents():
            self.app.processEvents()

        self.assertTrue(self.darkRefListener.callCount() == 1)
        self.assertTrue(self.datawatcherListener.callCount() == 1)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConstructionDarkAndFlatField,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')