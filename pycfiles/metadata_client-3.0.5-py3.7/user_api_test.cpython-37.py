# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/user_api_test.py
# Compiled at: 2019-03-11 08:28:16
# Size of source mod 2**32: 2015 bytes
"""UserApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from ..common.secrets import *
from ...metadata_client_api import MetadataClientApi

class UserApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)
    _UserApiTest__current_user_info_01 = {'email':USER_INFO['EMAIL'], 
     'first_name':USER_INFO['FIRST_NAME'], 
     'last_name':USER_INFO['LAST_NAME'], 
     'name':USER_INFO['NAME'], 
     'nickname':USER_INFO['NICKNAME'], 
     'provider':USER_INFO['PROVIDER'], 
     'uid':USER_INFO['UID']}

    def test_user_info(self):
        current_user = self._UserApiTest__current_user_info_01
        resp = self.client_api.get_current_user()
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