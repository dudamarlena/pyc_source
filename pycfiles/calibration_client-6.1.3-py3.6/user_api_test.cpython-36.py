# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/apis/user_api_test.py
# Compiled at: 2019-08-14 11:41:29
# Size of source mod 2**32: 2137 bytes
"""UserApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from ..common.secrets import *
from ...calibration_client_api import CalibrationClientApi

class UserApiTest(ApiBase, unittest.TestCase):
    cal_client_api = CalibrationClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)
    _UserApiTest__current_user_info_01 = {'email':str(CLIENT_OAUTH2_INFO['EMAIL']), 
     'first_name':str(CLIENT_OAUTH2_INFO['first_name']), 
     'last_name':str(CLIENT_OAUTH2_INFO['last_name']), 
     'name':str(CLIENT_OAUTH2_INFO['name']), 
     'nickname':str(CLIENT_OAUTH2_INFO['nickname']), 
     'provider':str(CLIENT_OAUTH2_INFO['provider']), 
     'uid':str(CLIENT_OAUTH2_INFO['uid'])}

    def test_user_info(self):
        current_user = self._UserApiTest__current_user_info_01
        resp = self.cal_client_api.get_current_user()
        resp_content = self.load_response_content(resp)
        receive = resp_content
        expect = current_user
        self.fields_validation(receive, expect)
        self.assert_eq_status_code(resp.status_code, OK)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'email', STRING)
        self.assert_eq_hfield(receive, expect, 'first_name', STRING)
        self.assert_eq_hfield(receive, expect, 'last_name', STRING)
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'nickname', STRING)
        self.assert_eq_hfield(receive, expect, 'provider', STRING)
        self.assert_eq_hfield(receive, expect, 'uid', STRING)


if __name__ == '__main__':
    unittest.main()