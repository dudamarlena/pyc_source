# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/test/test_datatransfert.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 4031 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/04/2019'
import unittest, tempfile, shutil, os
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.process.datatransfert import FolderTransfert

class TestDataTransfertIO(unittest.TestCase):
    __doc__ = 'Test inputs and outputs types of the handler functions'

    def setUp(self):
        self.origin_folder = tempfile.mkdtemp()
        self.scan_folder = os.path.join(self.origin_folder, 'scan_toto')
        os.mkdir(self.scan_folder)
        self.output_folder = tempfile.mkdtemp()
        self.scan = MockEDF.mockScan(scanID=(self.scan_folder), nRadio=10,
          nRecons=1,
          nPagRecons=4,
          dim=10)
        self.transfert_process = FolderTransfert()
        self.transfert_process.setDestDir(self.output_folder)

    def tearDown(self):
        shutil.rmtree(self.origin_folder)
        shutil.rmtree(self.output_folder)

    def testInputOutput(self):
        """Test that io using TomoBase instance work"""
        for input_type in (dict, TomoBase):
            for _input in FolderTransfert.inputs:
                for return_dict in (True, False):
                    if os.path.exists(self.output_folder):
                        shutil.rmtree(self.output_folder)
                        os.mkdir(self.output_folder)
                    self.scan = MockEDF.mockScan(scanID=(self.scan_folder), nRadio=10,
                      nRecons=1,
                      nPagRecons=4,
                      dim=10)
                    with self.subTest(handler=(_input.handler), return_dict=return_dict,
                      input_type=input_type):
                        input_obj = self.scan
                        if input_obj is dict:
                            input_obj = input_obj.to_dict()
                        else:
                            self.transfert_process._set_return_dict(return_dict)
                            out = getattr(self.transfert_process, _input.handler)(input_obj)
                            if return_dict:
                                self.assertTrue(isinstance(out, dict))
                            else:
                                self.assertTrue(isinstance(out, TomoBase))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDataTransfertIO,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite