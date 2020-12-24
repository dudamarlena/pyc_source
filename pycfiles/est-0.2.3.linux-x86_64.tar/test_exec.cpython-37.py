# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/app/test/test_exec.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 2962 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/26/2019'
import unittest, tempfile, shutil
from est.core.utils import DownloadDataset
from pushworkflow.scheme.parser import scheme_load
from ..process import exec_
import os
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestWorkflowFromOwsFile(unittest.TestCase):
    __doc__ = 'test construction of XAS object'

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        file_ = 'pymca_workflow.ows'
        DownloadDataset(dataset=file_, output_folder=(self.outputdir),
          timeout=10.0)
        self.orange_file = os.path.join(self.outputdir, file_)
        self.input_file1 = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        self.output_file = os.path.join(self.outputdir, 'output.h5')

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testPyMcaWorkflow(self):
        """Test regarding the instantiation of the pymcaXAS"""
        exec_(scheme=(scheme_load(self.orange_file)), input_=(self.input_file1),
          output_=(self.output_file))
        self.assertTrue(os.path.exists(self.output_file))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestWorkflowFromOwsFile,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')