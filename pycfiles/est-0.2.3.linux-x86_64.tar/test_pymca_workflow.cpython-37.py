# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/test/test_pymca_workflow.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 5464 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
import logging, os, shutil, tempfile, unittest
from silx.gui import qt
from orangecontrib.est.test.OrangeWorkflowTest import OrangeWorflowTest
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
from est.gui.qtapplicationmanager import QApplicationManager
logging.disable(logging.INFO)
_logger = logging.getLogger(__file__)
app = QApplicationManager()

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestSimplePyMcaWorkflow(OrangeWorflowTest):
    __doc__ = 'Test the following workflow:\n    - XASInputOW\n    - NormalizationOW\n\n    - XASOutputOW\n    '

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        self.xasInputWidget.setFileSelected(data_file)
        self.outputdir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.outputdir, 'output.h5')
        self.xasOutputWidget.setFileSelected(self.output_file)

    def tearDow(self):
        if os.path.isdir(self.outputdir):
            shutil.rmtree(self.outputdir)
        OrangeWorflowTest.tearDown(self)

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        xasInputNode = cls.addWidget(cls, 'orangecontrib.est.widgets.utils.xas_input.XASInputOW')
        xasNormalizationNode = cls.addWidget(cls, 'orangecontrib.est.widgets.pymca.normalization.NormalizationOW')
        xasEXAFSNode = cls.addWidget(cls, 'orangecontrib.est.widgets.pymca.exafs.ExafsOW')
        xasKWeightNode = cls.addWidget(cls, 'orangecontrib.est.widgets.pymca.k_weight.KWeightOW')
        xasFTNode = cls.addWidget(cls, 'orangecontrib.est.widgets.pymca.ft.FTOW')
        xasOutputNode = cls.addWidget(cls, 'orangecontrib.est.widgets.pymca.utils.xas_output.XASOutputOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, xasInputNode, 'xas_obj', xasNormalizationNode, 'xas_obj')
        cls.link(cls, xasNormalizationNode, 'xas_obj', xasEXAFSNode, 'xas_obj')
        cls.link(cls, xasEXAFSNode, 'xas_obj', xasKWeightNode, 'xas_obj')
        cls.link(cls, xasKWeightNode, 'xas_obj', xasFTNode, 'xas_obj')
        cls.link(cls, xasFTNode, 'xas_obj', xasOutputNode, 'xas_obj')
        cls.processOrangeEvents(cls)
        cls.xasInputWidget = cls.getWidgetForNode(cls, xasInputNode)
        cls.xasNormalizationWidget = cls.getWidgetForNode(cls, xasNormalizationNode)
        cls.xasEXAFSWidget = cls.getWidgetForNode(cls, xasEXAFSNode)
        cls.xasKWeightWidget = cls.getWidgetForNode(cls, xasKWeightNode)
        cls.xasFTWidget = cls.getWidgetForNode(cls, xasFTNode)
        cls.xasOutputWidget = cls.getWidgetForNode(cls, xasOutputNode)

    @classmethod
    def tearDownClass(cls):
        cls.xasInputWidget = None
        cls.xasNormalizationWidget = None
        cls.xasEXAFSWidget = None
        cls.xasKWeightWidget = None
        cls.xasFTWidget = None
        cls.xasOutputWidget = None
        OrangeWorflowTest.tearDownClass()

    def test(self):
        """Make sure the workflow is valid and end on the data transfert"""
        self.xasInputWidget.restart()
        app = qt.QApplication.instance()
        while app.hasPendingEvents():
            app.processEvents()
            self.processOrangeEventsStack()

        self.assertEqual(self.xasNormalizationWidget._window.getNCurves(), 4)
        self.assertEqual(self.xasEXAFSWidget._window.getNCurves(), 3)
        self.assertEqual(self.xasKWeightWidget._window.getNCurves(), 2)
        self.assertEqual(self.xasFTWidget._window.getNCurves(), 2)
        self.assertTrue(os.path.exists(self.output_file))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSimplePyMcaWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite