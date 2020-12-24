# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/test/test_reconstruction.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 9531 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '25/03/2019'
import os, shutil, tempfile, unittest
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.core.utils.scanutils import MockEDF
from tomwer.synctools.ftseries import _QDKRFRP, _QAxisRP, QReconsParams
from tomwer.core.scan.scanbase import TomoBase
import tomwer.core.process.reconstruction.darkref.params as DkrfMethod
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.test.utils import skip_gui_test
import time
from tomwer.core.log import TomwerLogger
import logging
logging.disable(logging.INFO)
_logger = TomwerLogger(__name__)

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
@unittest.skip('Fail on CI...')
class TestReconstructionWidgets(OrangeWorflowTest):
    __doc__ = 'Test behavior for several scans with the following scheme\n    \n        * DataSelector\n        * DarkRefs orange widget (reconstruct both dark and flat)\n        * Ftaxis orange widget\n        * Ftseries orange widget\n    \n    Then process the workflow and check if the different values of ReconsParams\n    are valid. And that in all case, pass all processes\n    '

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        cls.dataSelectorNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW')
        cls.darkRefNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW.DarkRefAndCopyOW')
        cls.ftAxisNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.reconstruction.AxisOW.AxisOW')
        cls.ftSeriesNode = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, cls.dataSelectorNode, 'data', cls.darkRefNode, 'data')
        cls.link(cls, cls.darkRefNode, 'data', cls.ftAxisNode, 'data')
        cls.link(cls, cls.ftAxisNode, 'data', cls.ftSeriesNode, 'data')
        cls.processOrangeEvents(cls)
        cls.dataSelectorWidget = cls.getWidgetForNode(cls, cls.dataSelectorNode)
        cls.darkRefWidget = cls.getWidgetForNode(cls, cls.darkRefNode)
        cls.axisWidget = cls.getWidgetForNode(cls, cls.ftAxisNode)
        cls.ftSeriesWidget = cls.getWidgetForNode(cls, cls.ftSeriesNode)
        cls.ftSeriesWidget._ftserie.reconsStack.setMockMode(True)
        cls.ftSeriesWidget._ftserie.setForceSync(True)
        cls.darkRefWidget.setForceSync(True)
        cls.axisWidget.setLocked(True)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.dataSelectorNode, cls.darkRefNode, cls.ftAxisNode,
         cls.ftSeriesNode):
            cls.removeNode(cls, node)

        _logger.info('all nodes removed')
        cls.dataSelectorWidget = None
        cls.darkRefWidget = None
        cls.axisWidget = None
        cls.ftSeriesWidget = None
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self._source_dir = tempfile.mkdtemp()

        def create_scan(folder_name):
            _dir = os.path.join(self._source_dir, folder_name)
            MockEDF.mockScan(scanID=_dir, nRadio=10, scan_range=180, n_extra_radio=2)
            return ScanFactory.create_scan_object(_dir)

        self.scan_1 = create_scan('scan_1')
        self.scan_2 = create_scan('scan_2')
        self.scan_2.ftseries_recons_params = QReconsParams(empty=True)
        self.scan_2.ftseries_recons_params.dkrf = _QDKRFRP()
        self.scan_2.ftseries_recons_params.dkrf.ref_calc_method = 'None'
        self.scan_3 = create_scan('scan_3')
        self.scan_3.ftseries_recons_params = QReconsParams(empty=False)
        self.scan_3.ftseries_recons_params.copy(self.scan_2.ftseries_recons_params.dkrf)
        self.scan_4 = create_scan('scan_4')
        self.scan_4.ftseries_recons_params = QReconsParams()
        self.scan_4.ftseries_recons_params.axis = _QAxisRP()
        self.scan_4.ftseries_recons_params.axis.to_the_center = False
        self.darkRefWidget.recons_params.ref_calc_method = 'Median'
        self.darkRefWidget.recons_params._set_skip_if_exist(False)
        self.axisWidget.recons_params.to_the_center = False
        self.axisWidget.recons_params.plot_figure = False
        self.darkRefWidget.widget._refCopyWidget.setChecked(False)
        self.ftSeriesWidget.recons_params.ref_calc_method = 'Average'
        self.ftSeriesWidget.recons_params.dkrf._set_skip_if_exist(True)
        self.ftSeriesWidget.recons_params.plot_figure = True
        self.ftSeriesWidget.recons_params.to_the_center = True
        self._scans = (
         self.scan_1, self.scan_2, self.scan_3, self.scan_4)
        for _scan in self._scans:
            self.dataSelectorWidget.addScan(_scan)

        self.app.processEvents()
        self.axisWidget._skip_exec(True)

    def tearDown(self):
        shutil.rmtree(self._source_dir)
        OrangeWorflowTest.tearDown(self)

    def testProcessing(self):
        """Test the different values of reconstruction parameters during the
        workflow execution"""
        for _scan in self._scans:
            self.app.processEvents()
            assert isinstance(_scan, TomoBase)
            self.dataSelectorWidget.setActiveScan(_scan)
            self.dataSelectorWidget.widget._selectActiveScan()
            self.processOrangeEventsStack()
            self.assertTrue(self.darkRefWidget.recons_params.ref_calc_method is DkrfMethod.median)
            self.assertTrue(_scan.ftseries_recons_params.dkrf.ref_calc_method is DkrfMethod.median)
            self.assertTrue(self.darkRefWidget.recons_params.overwrite_ref is True)
            self.assertTrue(_scan.ftseries_recons_params.dkrf.overwrite_ref is True)
            self.assertTrue(isinstance(_scan.ftseries_recons_params, QReconsParams))
            self.assertTrue(isinstance(_scan.ftseries_recons_params.dkrf, _QDKRFRP))
            for t in range(0, 5):
                time.sleep(0.1)
                self.processOrangeEventsStack()
                self.app.processEvents()

            self.assertTrue(isinstance(_scan.ftseries_recons_params, QReconsParams))
            self.assertTrue(self.axisWidget.recons_params.plot_figure is False)
            self.assertTrue(isinstance(_scan.ftseries_recons_params, QReconsParams))
            self.processOrangeEventsStack()
            self.assertTrue(self.ftSeriesWidget.recons_params.dkrf.ref_calc_method is DkrfMethod.median)
            self.assertTrue(_scan.ftseries_recons_params.dkrf.ref_calc_method is DkrfMethod.median)
            self.assertTrue(self.ftSeriesWidget.recons_params.dkrf.overwrite_ref is True)
            self.assertTrue(_scan.ftseries_recons_params.dkrf.overwrite_ref is True)
            self.app.processEvents()

        while self.app.hasPendingEvents():
            self.app.processEvents()


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReconstructionWidgets,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')