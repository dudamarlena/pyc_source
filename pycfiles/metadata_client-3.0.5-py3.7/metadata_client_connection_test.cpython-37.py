# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/metadata_client_connection_test.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 1556 bytes
"""MetadataClientConnectionTest class"""
import logging, unittest
from metadata_client.metadata_client import MetadataClient
from .common.secrets import *
from modules.module_base import ModuleBase

class MetadataClientConnectionTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.wrong_mdc_client = MetadataClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email='xxxxxxxxxxxxxx',
          base_api_url=BASE_API_URL)

    def test_get_data_group_types_with_errors(self):
        resp = MetadataClient.get_all_data_group_types(self.wrong_mdc_client)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['app_info'], "Incorrect request header: 'X-User-Email'!")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['info'], 'data_group_type not found!')
        self.assert_eq_val(resp['data'], {})


if __name__ == '__main__':
    unittest.main()