# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/test/test_scanlist_samplemoved.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3629 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/03/2018'
import logging, unittest
from tomwer.gui.qtapplicationmanager import QApplicationManager
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test
app = QApplicationManager()
logging.disable(logging.INFO)

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
@unittest.skip('Fail on CI...')
class TestScanListSampleMovedWorkflow(OrangeWorflowTest):
    __doc__ = 'Make sure the sample moved is correctly connecting to the orange-canvas\n    and that it will display requested scans\n    '

    def setUp(self):
        super(TestScanListSampleMovedWorkflow, self).setUp()
        dataset = 'D2_H2_T2_h_'
        self.dataTestDir = UtilsTest.getDataset(dataset)

    def tearDow(self):
        super(TestScanListSampleMovedWorkflow, self).tearDow()

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        cls.nodeScanList = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.control.DataListOW.DataListOW')
        cls.nodeSampleMoved = cls.addWidget(cls, 'orangecontrib.tomwer.widgets.visualization.SampleMovedOW.SampleMovedOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, cls.nodeScanList, 'data', cls.nodeSampleMoved, 'data')
        cls.processOrangeEvents(cls)
        cls.scanListWidget = cls.getWidgetForNode(cls, cls.nodeScanList)
        cls.sampleMovedWidget = cls.getWidgetForNode(cls, cls.nodeSampleMoved)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeScanList, cls.nodeSampleMoved):
            cls.removeNode(cls, node)

        OrangeWorflowTest.tearDownClass()

    def test(self):
        self.assertTrue(len(self.sampleMovedWidget._mainWidget._images) is 0)
        self.scanListWidget.add(self.dataTestDir)
        self.scanListWidget._sendList()
        app.processEvents()


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanListSampleMovedWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')