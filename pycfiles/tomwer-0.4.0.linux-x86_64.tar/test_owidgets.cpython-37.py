# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/test/test_owidgets.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 3405 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
import logging, unittest
from tomwer.gui.qtapplicationmanager import QApplicationManager
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import skip_gui_test
logging.disable(logging.INFO)
app = QApplicationManager()

@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestOrangeWidgetsCreations(OrangeWorflowTest):
    __doc__ = 'Create dummy workflow to make sure orange widget are correctly created\n    '

    def setUp(self):
        OrangeWorflowTest.setUp(self)

    def tearDown(self):
        OrangeWorflowTest.tearDown(self)

    def test(self):
        """Simple creation of the following workflow:
        ScanList -> ScanSelector -> nameFilter -> sampleMoved
                                               -> stackSlice
        """
        dataListNode = self.addWidget('orangecontrib.tomwer.widgets.control.DataListOW.DataListOW')
        dataSelectorNode = self.addWidget('orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW')
        scanFilterNode = self.addWidget('orangecontrib.tomwer.widgets.control.FilterOW.NameFilterOW')
        sampleMovedNode = self.addWidget('orangecontrib.tomwer.widgets.visualization.SampleMovedOW.SampleMovedOW')
        groupSliceNode = self.addWidget('orangecontrib.tomwer.widgets.visualization.SliceStackOW.SlicesStackOW')
        self.processOrangeEvents()
        self.link(dataListNode, 'data', dataSelectorNode, 'data')
        self.link(dataSelectorNode, 'data', scanFilterNode, 'data')
        self.link(scanFilterNode, 'data', sampleMovedNode, 'data')
        self.link(scanFilterNode, 'data', groupSliceNode, 'data')
        self.processOrangeEvents()


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestOrangeWidgetsCreations,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')