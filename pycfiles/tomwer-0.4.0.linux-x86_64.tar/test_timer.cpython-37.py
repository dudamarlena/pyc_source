# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/test/test_timer.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3240 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/04/2019'
import shutil, tempfile, unittest
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.process.timer import Timer
from tomwer.core.scan.scanbase import TomoBase

class TestTimerIO(unittest.TestCase):
    __doc__ = 'Test inputs and outputs types of the handler functions'

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()
        self.scan = MockEDF.mockScan(scanID=(self.scan_folder), nRadio=10,
          nRecons=1,
          nPagRecons=4,
          dim=10)
        self.timer_process = Timer(wait=1)

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        """Test that io using TomoBase instance work"""
        for input_type in (dict, TomoBase):
            for _input in Timer.inputs:
                for return_dict in (True, False):
                    with self.subTest(handler=(_input.handler), return_dict=return_dict,
                      input_type=input_type):
                        input_obj = self.scan
                        if input_obj is dict:
                            input_obj = input_obj.to_dict()
                        else:
                            self.timer_process._set_return_dict(return_dict)
                            out = getattr(self.timer_process, _input.handler)(input_obj)
                            if return_dict:
                                self.assertTrue(isinstance(out, dict))
                            else:
                                self.assertTrue(isinstance(out, TomoBase))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestTimerIO,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite