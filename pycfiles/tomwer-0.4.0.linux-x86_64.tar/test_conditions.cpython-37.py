# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/test/test_conditions.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3736 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/07/2018'
import unittest, shutil, tempfile
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.process.conditions.filters import RegularExpressionFilter, FileNameFilter

class TestConditionalFilter(unittest.TestCase):
    __doc__ = '\n    Small unit test for the core.conditions\n    '

    def testPattern1(self):
        filter = RegularExpressionFilter('name10')
        self.assertTrue(filter.isFiltered('toto') is True)
        self.assertTrue(filter.isFiltered('name10') is False)
        self.assertTrue(filter.isFiltered('name100') is False)

    def testInputOutput(self):
        pass


class TestConditionIO(unittest.TestCase):
    __doc__ = 'Test inputs and outputs types of the handler functions'

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()
        self.scan = MockEDF.mockScan(scanID=(self.scan_folder), nRadio=10,
          nRecons=1,
          nPagRecons=4,
          dim=10)
        self.filter_process = FileNameFilter('*')

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        for input_type in (dict, TomoBase):
            for _input in FileNameFilter.inputs:
                for return_dict in (True, False):
                    with self.subTest(handler=(_input.handler), return_dict=return_dict,
                      input_type=input_type):
                        self.filter_process._set_return_dict(return_dict)
                        input_obj = self.scan
                        if input_type is dict:
                            input_obj = self.scan.to_dict()
                        else:
                            out = getattr(self.filter_process, _input.handler)(input_obj)
                            if return_dict:
                                self.assertTrue(isinstance(out, dict))
                            else:
                                self.assertTrue(isinstance(out, TomoBase))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConditionalFilter, TestConditionIO):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')