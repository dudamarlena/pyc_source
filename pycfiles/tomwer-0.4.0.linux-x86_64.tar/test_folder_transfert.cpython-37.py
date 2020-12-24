# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/test/test_folder_transfert.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 6876 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/10/2019'
from tomwer.test.utils import skip_gui_test
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from silx.gui.utils.testutils import SignalListener
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.scan.scanfactory import ScanFactory
import unittest, tempfile, shutil, time, os

@unittest.skip('CI fail')
class TestCopyNFolder(OrangeWorflowTest):
    __doc__ = 'test the following workflow and behavior.\n    Workflow is :\n        - DataListOW\n        - FTSerieWidget\n        - DataTransfertOW\n\n    A list of folder into ScanList them go through FTserieWidget and to\n    FolderTransfert. Make sure all the data have been copied\n    '
    TIMEOUT_TEST = 20

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        cls.scanListNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataListOW.DataListOW')
        cls.FTSerieNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW')
        cls.folderTransfertNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataTransfertOW.DataTransfertOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, cls.scanListNode, 'data', cls.FTSerieNode, 'data')
        cls.link(cls, cls.FTSerieNode, 'data', cls.folderTransfertNode, 'data')
        cls.processOrangeEvents(cls)
        cls.scanListWidget = cls.getWidgetForNode(cls, cls.scanListNode)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.FTSerieNode)
        cls.transfertWidget = cls.getWidgetForNode(cls, cls.folderTransfertNode)
        cls.processOrangeEvents(cls)
        cls.ftserieWidget._ftserie.reconsStack.setMockMode(True)
        cls.ftserieWidget._ftserie.setForceSync(True)
        cls.transfertWidget.turn_off_print = True
        cls.transfertWidget.setForceSync(True)
        cls.dataTransfertListener = SignalListener()
        cls.transfertWidget.scanready.connect(cls.dataTransfertListener)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.scanListNode, cls.FTSerieNode, cls.folderTransfertNode):
            cls.removeNode(cls, node)

        cls.scanListWidget = None
        cls.ftserieWidget = None
        cls.transfertWidget = None
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self.dataTransfertListener.clear()
        self.folders = []
        for i in range(1):
            inputFolder = tempfile.mkdtemp()
            self.folders.append(inputFolder)
            MockEDF.fastMockAcquisition(inputFolder)

        self.outputdir = tempfile.mkdtemp()

    def tearDown(self):
        for f in self.folders:
            if os.path.isdir(f):
                shutil.rmtree(f)

        if os.path.isdir(self.outputdir):
            shutil.rmtree(self.outputdir)
        OrangeWorflowTest.tearDown(self)

    def testCopy(self):
        self.assertTrue(os.path.isdir(self.outputdir))
        self.transfertWidget.setDestDir(self.outputdir)
        for f in self.folders:
            assert os.path.isdir(f)
            self.scanListWidget.add(ScanFactory.create_scan_object(scan_path=f))
            self.app.processEvents()
            self.processOrangeEventsStack()

        self.assertTrue(self.outpudirIsEmpty())
        self.scanListWidget.start()
        timeout = self.TIMEOUT_TEST
        while timeout > 0 and self.dataTransfertListener.callCount() == 0:
            timeout = timeout - 0.2
            self.app.processEvents()
            self.processOrangeEventsStack()
            time.sleep(0.2)

        self.assertTrue(self.dataHasBeenCopied())
        signal_manager = self.canvas_window.current_document().scheme().signal_manager
        timeout = self.TIMEOUT_TEST
        while timeout > 0 and self.app.hasPendingEvents():
            timeout = timeout - 0.2
            self.app.processEvents()
            print('blocking_nodes:', signal_manager.pending_nodes())
            time.sleep(0.2)

        if timeout <= 0.0:
            raise TimeoutError('Loop infinitely on some qt event...')

    def outpudirIsEmpty(self):
        return len(os.listdir(self.outputdir)) == 0

    def dataHasBeenCopied(self):
        return len(os.listdir(self.outputdir)) == 1


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestCopyNFolder,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')