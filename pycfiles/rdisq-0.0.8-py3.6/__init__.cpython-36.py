# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2020-03-07 02:01:38
# Size of source mod 2**32: 1110 bytes
__author__ = 'smackware'
from unittest.case import TestCase
from rdisq.response import RdisqResponse
from rdisq import RESULT_ATTR
from rdisq import PROCESS_TIME_ATTR
from rdisq import EXCEPTION_ATTR

class RdisqTest(TestCase):

    def test__result__process_response(self):
        valid_response = {RESULT_ATTR: 'RETURNED', 
         PROCESS_TIME_ATTR: 2, 
         EXCEPTION_ATTR: None}
        result = RdisqResponse(1, None)
        returned_value = result.process_response_data(valid_response)
        self.assertEqual(result.exception, None)
        self.assertEqual(returned_value, 'RETURNED')

    def test__result__process_response_exception(self):

        class TestException(Exception):
            pass

        valid_response = {RESULT_ATTR: None, 
         PROCESS_TIME_ATTR: 2, 
         EXCEPTION_ATTR: TestException('BLAH')}
        result = RdisqResponse(1, None)
        response = result.process_response_data(valid_response)
        self.assertEqual(response, None)
        self.assertTrue(isinstance(result.exception, TestException))