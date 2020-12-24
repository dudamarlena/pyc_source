# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/apis/device_type_api_test.py
# Compiled at: 2019-08-05 17:28:52
# Size of source mod 2**32: 4993 bytes
__doc__ = 'DeviceTypeApiTest class'
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...calibration_client_api import CalibrationClientApi

class DeviceTypeApiTest(ApiBase, unittest.TestCase):
    cal_client_api = CalibrationClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)

    def test_create_device_type_api(self):
        _DeviceTypeApiTest__unique_name = Generators.generate_unique_name('DeviceTypeApi')
        device_type = {'device_type': {'name':_DeviceTypeApiTest__unique_name, 
                         'flg_available':'true', 
                         'description':'desc 01'}}
        expect = device_type['device_type']
        received = self._DeviceTypeApiTest__create_entry_api(device_type, expect)
        device_type_id = received['id']
        device_type_name = received['name']
        self._DeviceTypeApiTest__create_error_entry_uk_api(device_type)
        self._DeviceTypeApiTest__get_all_entries_by_name_api(device_type_name, expect)
        self._DeviceTypeApiTest__get_entry_by_id_api(device_type_id, expect)
        self._DeviceTypeApiTest__update_entry_api(device_type_id, expect)
        self._DeviceTypeApiTest__delete_entry_by_id_api(device_type_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client_api.create_device_type_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client_api.create_device_type_api(entry_info)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {'info': {'name': ['has already been taken']}}
        self.assertEqual(receive, expect, 'Expected result not received')
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)
        receive_msg = receive['info']['name'][0]
        expect_msg = expect['info']['name'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = Generators.generate_unique_name('DeviceTypeApiUpd')
        device_type_upd = {'device_type': {'name':unique_name_upd, 
                         'flg_available':'false', 
                         'description':'desc 01 updated!!!'}}
        response = self.cal_client_api.update_device_type_api(entry_id, device_type_upd)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect_upd = device_type_upd['device_type']
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)
        field = 'name'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_name_api(self, name, expect):
        response = self.cal_client_api.get_all_device_types_by_name_api(name)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client_api.get_device_type_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.cal_client_api.delete_device_type_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()