# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/test/test_larch_workflow.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 6222 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/08/2019'
import logging, os, shutil, tempfile, unittest
from silx.gui import qt
import time, h5py
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
class TestSimpleLarchWorkflow(OrangeWorflowTest):
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
        xasPreEdgeNode = cls.addWidget(cls, 'orangecontrib.est.widgets.larch.pre_edge.PreEdgeOW')
        xasAutobkNode = cls.addWidget(cls, 'orangecontrib.est.widgets.larch.autobk.AutobkOW')
        xasXFTFNode = cls.addWidget(cls, 'orangecontrib.est.widgets.larch.xftf.XFTFOW')
        xasMBackNormNode = cls.addWidget(cls, 'orangecontrib.est.widgets.larch.mback_norm.Mback_normOW')
        xasOutputNode = cls.addWidget(cls, 'orangecontrib.est.widgets.utils.xas_output.XASOutputOW')
        cls.processOrangeEvents(cls)
        cls.link(cls, xasInputNode, 'xas_obj', xasPreEdgeNode, 'xas_obj')
        cls.link(cls, xasPreEdgeNode, 'xas_obj', xasAutobkNode, 'xas_obj')
        cls.link(cls, xasAutobkNode, 'xas_obj', xasXFTFNode, 'xas_obj')
        cls.link(cls, xasXFTFNode, 'xas_obj', xasMBackNormNode, 'xas_obj')
        cls.link(cls, xasMBackNormNode, 'xas_obj', xasOutputNode, 'xas_obj')
        cls.processOrangeEvents(cls)
        cls.xasInputWidget = cls.getWidgetForNode(cls, xasInputNode)
        cls.xasPreEdgeWidget = cls.getWidgetForNode(cls, xasPreEdgeNode)
        cls.xasAutobkWidget = cls.getWidgetForNode(cls, xasAutobkNode)
        cls.xasXFTFWidget = cls.getWidgetForNode(cls, xasXFTFNode)
        cls.xasMbackNormWidget = cls.getWidgetForNode(cls, xasMBackNormNode)
        cls.xasOutputWidget = cls.getWidgetForNode(cls, xasOutputNode)

    @classmethod
    def tearDownClass(cls):
        cls.xasInputWidget = None
        cls.xasPreEdgeWidget = None
        cls.xasAutobkWidget = None
        cls.xasXFTFWidget = None
        cls.xasMbackNormWidget = None
        cls.xasOutputWidget = None
        OrangeWorflowTest.tearDownClass()

    def test(self):
        """Make sure the workflow is valid and end on the data transfert"""
        self.xasInputWidget.restart()
        app = qt.QApplication.instance()
        while app.hasPendingEvents():
            app.processEvents()
            time.sleep(0.1)
            self.processOrangeEventsStack()

        self.assertEqual(self.xasPreEdgeWidget._window.getNCurves(), 4)
        self.assertEqual(self.xasAutobkWidget._window.getNCurves(), 3)
        self.assertEqual(self.xasXFTFWidget._window.getNCurves(), 3)
        self.assertEqual(self.xasMbackNormWidget._window.getNCurves(), 2)
        self.assertTrue(os.path.exists(self.output_file))
        with h5py.File(self.output_file, 'r') as (hdf5):
            self.assertTrue('scan1' in hdf5)
            scan_grp = hdf5['scan1']
            self.assertTrue('absorbed_beam' in scan_grp)
            self.assertTrue('xas_process_1' in scan_grp)
            self.assertTrue('xas_process_2' in scan_grp)
            self.assertTrue('xas_process_3' in scan_grp)
            self.assertTrue('xas_process_4' in scan_grp)
            process_1_grp = scan_grp['xas_process_1']
            self.assertTrue(process_1_grp['program'][()] == 'larch_pre_edge')
            process_4_grp = scan_grp['xas_process_4']
            self.assertTrue(process_4_grp['program'][()] == 'larch_mback_norm')


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSimpleLarchWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite