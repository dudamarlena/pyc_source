# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/test/test_scanlist_ftserie.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 12760 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
import copy, logging, os, shutil, tempfile, unittest, time
from silx.gui.utils.testutils import SignalListener
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.core.process.reconstruction.ftseries.params.fastsetupdefineglobals import FastSetupAll
from tomwer.synctools.stacks.reconstruction.ftseries import _ReconsFtSeriesThread
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test
from tomwer.core.utils.scanutils import MockEDF
logging.disable(logging.INFO)

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestScanListFTSerieWorkflow(OrangeWorflowTest):
    __doc__ = 'Make sure the reconstruction of the second scan is executed with the\n    correct reconstruction parameters.\n    Set up is as following :\n        - ScanList contains two datasets. Those scan can contains or not some .h5\n        - FTSerie is activated with or without H5Exploration option\n    '

    def setUp(self):
        super(TestScanListFTSerieWorkflow, self).setUp()
        self.inputDir = tempfile.mkdtemp()
        ft = FastSetupAll()
        self.default = copy.deepcopy(ft.structures)
        assert 'FT' in ft.structures
        assert 'NUM_PART' in ft.structures['FT']
        assert ft.structures['FT']['NUM_PART'] not in (1, 2)
        ft.structures['FT']['NUM_PART'] = 1
        self.st1 = copy.deepcopy(ft.structures)
        ft.structures['FT']['NUM_PART'] = 2
        self.st2 = copy.deepcopy(ft.structures)

    def tearDow(self):
        if os.path.isdir(self.inputDir):
            shutil.rmtree(self.inputDir)
        super(TestScanListFTSerieWorkflow, self).tearDow()

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        cls.nodeScanList = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataListOW.DataListOW')
        cls.nodeFTSerie = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.FtseriesOW.FtseriesOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, cls.nodeScanList, 'data', cls.nodeFTSerie, 'data')
        cls.processOrangeEvents(cls)
        cls.scanListWidget = cls.getWidgetForNode(cls, cls.nodeScanList)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.nodeFTSerie)
        _ReconsFtSeriesThread.setCopyH5FileReconsIntoFolder(True)
        cls.ftserieWidget._ftserie.reconsStack.setMockMode(True)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeScanList, cls.nodeFTSerie):
            cls.removeNode(cls, node)

        del cls.scanListWidget
        del cls.ftserieWidget
        OrangeWorflowTest.tearDownClass()

    def initData(self, data01H5, data10H5):
        """Init the two datasets and set the given .h5 file if any given
        The order of scanning is always : first dataset01, second dataset10

        :param data01H5: the values of the structures to save as a h5 file.
            Apply on the daset01.
            If None given then no H5 file will be saved
        :param data10H5: the values of the structures to save as a h5 file.
            Apply on the daset10.
            If None given then no H5 file will be saved
        """
        dataDir01 = UtilsTest.getDataset('test01')
        dataDir10 = UtilsTest.getDataset('test10')
        self.clearInputFolder()
        self.dest01 = os.path.join(self.inputDir, os.path.basename(dataDir01))
        shutil.copytree(src=dataDir01, dst=(self.dest01))
        for f in os.listdir(dataDir01):
            assert not f.lower().endswith('.h5')

        self.dest10 = os.path.join(self.inputDir, os.path.basename(dataDir10))
        for f in os.listdir(dataDir10):
            assert not f.lower().endswith('.h5')

        shutil.copytree(src=dataDir10, dst=(self.dest10))
        data_and_dir = (
         (
          data01H5, self.dest01), (data10H5, self.dest10))
        for data, dataDir in data_and_dir:
            if data is not None:
                ft = FastSetupAll()
                ft.structures = data
                path = os.path.join(dataDir, 'reconsH5File.h5')
                ft.writeAll(path, 3.8)

        self.scanListWidget.clear()
        self.scanListWidget.add(self.dest01)
        self.scanListWidget.add(self.dest10)

    def clearInputFolder(self):
        for subFolder in os.listdir(self.inputDir):
            folder = os.path.join(self.inputDir, subFolder)
            assert os.path.isdir(folder)
            shutil.rmtree(folder)

    def setH5Exploration(self, b):
        """Activate or not the exploration"""
        self.ftserieWidget.setH5Exploration(b)

    def runAndTestList(self, structures, results, caseMsg):
        """Check that the reconstruction are send in the same order as the list
        is sending them
        """
        self.initData(structures[0], structures[1])
        self.scanListWidget._sendList()
        self.processOrangeEvents()
        output01 = os.path.join(self.dest01, _ReconsFtSeriesThread.copyH5ReconsName)
        self.assertTrue(os.path.isfile(output01))
        ft01 = FastSetupAll()
        ft01.readAll(output01, 3.8)
        with self.subTest(msg=('test reconstruction parameters used - folder1 : ' + caseMsg), value=(int(ft01.structures['FT']['NUM_PART'])),
          expected=(int(results[0]['FT']['NUM_PART']))):
            self.assertEqual(int(ft01.structures['FT']['NUM_PART']), int(results[0]['FT']['NUM_PART']))
        os.remove(output01)
        output10 = os.path.join(self.dest10, _ReconsFtSeriesThread.copyH5ReconsName)
        self.assertTrue(os.path.isfile(output10))
        ft10 = FastSetupAll()
        ft10.readAll(output10, 3.8)
        with self.subTest(msg=('test reconstruction parameters used - folder2 : ' + caseMsg), value=(ft10.structures['FT']['NUM_PART']),
          expected=(results[1]['FT']['NUM_PART'])):
            self.assertTrue(ft10.structures['FT']['NUM_PART'] == results[1]['FT']['NUM_PART'])
        os.remove(output10)

    def getTestMsg(self, ftserieStatus, structures, results):
        """Return the message fitting with the structures we are setting to
        test01 and test10 and to the restul we want"""
        msg = 'FTSerieWidget status : ' + ftserieStatus
        msg += '\nConfiguration of folders : '
        msg += '\n    - Folder 1 contains '
        msg += 'no .h5' if structures[0] is self.default else 'h5 with ' + ('st1' if structures[0] is self.st1 else 'st2') + ' structure'
        msg += '\n    - Folder 2 contains '
        msg += 'no .h5' if structures[1] is self.default else 'h5 with ' + ('st1' if structures[1] is self.st1 else 'st2') + ' structure'
        msg += '\nResults in folder should be :'
        msg += '\n   - for first folder :'
        msg += 'default' if results[0] is self.default else 'st1' if results[0] is self.st1 else 'ft2'
        msg += '\n   - for second folder :'
        msg += 'default' if results[1] is self.default else 'st1' if results[1] is self.st1 else 'ft2'
        return msg


@unittest.skipIf((skip_gui_test()), reason='skip gui test')
@unittest.skip('Fail on CI...')
class TestLocalReconstructions(OrangeWorflowTest):
    __doc__ = 'test with three widgets : ScanList, FTSerieWidget and ImageStackViewerWidget.\n        Make sure that when path with data set:\n            - scanList is sending signals\n            - FTSerieWidget is reconstructing and emitting a signal\n            - viewer is displaying a set of data (receiving the information)\n    '

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self.inputdir = tempfile.mkdtemp()
        MockEDF.fastMockAcquisition(self.inputdir)
        self.ftserieListener = SignalListener()
        self.ftserieWidget.sigScanReady.connect(self.ftserieListener)

    def tearDow(self):
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)
        OrangeWorflowTest.tearDown(self)

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        cls.nodeScanList = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataListOW.DataListOW')
        cls.nodeFTSerie = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW')
        cls.nodeViewer = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.visualization.ImageStackViewerOW.ImageStackViewerOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, cls.nodeScanList, 'data', cls.nodeFTSerie, 'data')
        cls.link(cls, cls.nodeFTSerie, 'data', cls.nodeViewer, 'data')
        cls.processOrangeEvents(cls)
        cls.scanListWidget = cls.getWidgetForNode(cls, cls.nodeScanList)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.nodeFTSerie)
        cls.viewerWidget = cls.getWidgetForNode(cls, cls.nodeViewer)
        cls.ftserieWidget._ftserie.reconsStack.setMockMode(True)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeScanList, cls.nodeFTSerie, cls.nodeViewer):
            cls.removeNode(cls, node)

        OrangeWorflowTest.tearDownClass()

    def test(self):
        """Make sure the workflow is valid and end on the data transfert"""
        self.scanListWidget.add(self.inputdir)
        self.assertTrue(self.ftserieWidget._ftserie._scan is None)
        self.assertTrue(self.viewerWidget.viewer.getCurrentScanFolder() == '')
        self.assertTrue(self.viewerWidget.viewer.ftseriereconstruction is None)
        self.app.processEvents()
        self.scanListWidget.show()
        self.qWaitForWindowExposed(self.scanListWidget)
        self.scanListWidget._sendList()
        timeout = 5
        loop_duration = 0.01
        while self.ftserieListener.callCount() < 1 and timeout > 0:
            self.app.processEvents()
            time.sleep(loop_duration)
            timeout -= loop_duration

        if timeout <= 0:
            raise TimeoutError('viewer is never activated')
        self.app.processEvents()
        self.assertEqual(self.viewerWidget.viewer.getCurrentScanFolder(), self.inputdir)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanListFTSerieWorkflow, TestLocalReconstructions):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite