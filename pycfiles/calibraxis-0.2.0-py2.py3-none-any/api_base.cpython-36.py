# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/apis/api_base.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 1576 bytes
__doc__ = 'BaseApiTest Class with helper methods common to all modules tests'
import unittest
from ..common.config_test import *
from ..common.util import Util

class ApiBase(Util, unittest.TestCase):

    def get_and_validate_create_entry(self, response):
        self.assert_eq_status_code(response.status_code, CREATED)
        resp_content = self.load_response_content(response)
        return resp_content

    def get_and_validate_all_entries_by_name(self, response):
        self.assert_eq_status_code(response.status_code, OK)
        resp_content = self.load_response_content(response)
        return resp_content[0]

    def get_and_validate_entry_by_id(self, response):
        self.assert_eq_status_code(response.status_code, OK)
        resp_content = self.load_response_content(response)
        return resp_content

    def get_and_validate_delete_entry_by_id(self, response):
        self.assert_eq_status_code(response.status_code, NO_CONTENT)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {}
        self.assert_eq_val(receive, expect)

    def get_and_validate_resource_not_found(self, response):
        resp_content = self.load_response_content(response)
        receive = resp_content
        receive_msg = receive['info']
        expect_msg = RESOURCE_NOT_FOUND
        expect = {'info': expect_msg}
        self.assert_eq_status_code(response.status_code, NOT_FOUND)
        self.assertEqual(receive, expect, 'Data must not be found')
        self.assert_eq_str(receive_msg, expect_msg)