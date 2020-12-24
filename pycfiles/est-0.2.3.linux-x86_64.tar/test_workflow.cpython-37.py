# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/pushworkflowactors/test/test_workflow.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 5996 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/12/2019'
import os, unittest, est.core.process.roi, est.core.io
import est.app.process as exec_workflow
from est.core.types import XASObject
from est.pushworkflow.scheme.link import Link
from est.pushworkflow.scheme.node import Node
from est.pushworkflow.scheme.scheme import Scheme
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    import est.core.process.pymca.exafs, est.core.process.pymca.ft, est.core.process.pymca.k_weight
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    import est.core.process.pymca.normalization

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestWorkflowFunctions(unittest.TestCase):
    __doc__ = 'Test some processing workflow'

    def setUp(self):
        unittest.TestCase.setUp(self)
        read_task = Node(callback=(est.core.io.read_frm_file))
        normalization_task = Node(callback=(est.core.process.pymca.normalization.pymca_normalization))
        exafs_task = Node(callback=(est.core.process.pymca.exafs.pymca_exafs))
        k_weight_task = Node(callback=(est.core.process.pymca.k_weight.pymca_k_weight))
        ft_task = Node(callback=(est.core.process.pymca.ft.pymca_ft))
        nodes = (
         read_task, normalization_task, exafs_task, k_weight_task, ft_task)
        links = [
         Link(source_node=read_task, source_channel='xas_obj', sink_node=normalization_task,
           sink_channel='xas_obj'),
         Link(source_node=normalization_task, source_channel='xas_obj', sink_node=exafs_task,
           sink_channel='xas_obj'),
         Link(source_node=exafs_task, source_channel='xas_obj', sink_node=k_weight_task,
           sink_channel='xas_obj'),
         Link(source_node=k_weight_task, source_channel='xas_obj', sink_node=ft_task,
           sink_channel='xas_obj')]
        self.scheme = Scheme(nodes=nodes, links=links)
        self.data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')

    def testProcess(self):
        out = exec_workflow(scheme=(self.scheme), input_=(self.data_file))
        assert isinstance(out, dict)
        xas_obj_out = XASObject.from_dict(out)
        assert 'FT' in xas_obj_out.spectra[0]
        assert 'FTRadius' in xas_obj_out.spectra[0].ft


@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestWorkflowCallableClasses(unittest.TestCase):
    __doc__ = 'Test some processing workflow'

    def setUp(self):
        unittest.TestCase.setUp(self)
        read_task = Node(callback=(est.core.io.XASReader))
        roi_task = Node(callback=(est.core.process.roi.ROIProcess))
        normalization_task = Node(callback=(est.core.process.pymca.normalization.PyMca_normalization))
        k_weight_task = Node(callback=(est.core.process.pymca.k_weight.PyMca_k_weight))
        exafs_task = Node(callback=(est.core.process.pymca.exafs.PyMca_exafs))
        ft_task = Node(callback=(est.core.process.pymca.ft.PyMca_ft))
        nodes = (
         read_task, roi_task, normalization_task, k_weight_task,
         exafs_task, ft_task)
        links = [
         Link(source_node=read_task, source_channel='spectra', sink_node=roi_task,
           sink_channel='spectra'),
         Link(source_node=roi_task, source_channel='spectra', sink_node=normalization_task,
           sink_channel='spectra'),
         Link(source_node=normalization_task, source_channel='spectra', sink_node=exafs_task,
           sink_channel='spectra'),
         Link(source_node=exafs_task, source_channel='spectra', sink_node=k_weight_task,
           sink_channel='spectra'),
         Link(source_node=k_weight_task, source_channel='spectra', sink_node=ft_task,
           sink_channel='spectra')]
        self.scheme = Scheme(nodes=nodes, links=links)
        self.data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')

    def testProcess(self):
        out = exec_workflow(scheme=(self.scheme), input_=(self.data_file))
        assert isinstance(out, dict)
        xas_obj_out = XASObject.from_dict(out)
        assert 'FT' in xas_obj_out.spectra[0]
        assert 'FTRadius' in xas_obj_out.spectra[0].ft
        assert 'FT' in xas_obj_out.configuration
        assert 'Normalization' in xas_obj_out.configuration


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestWorkflowFunctions, TestWorkflowCallableClasses):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')