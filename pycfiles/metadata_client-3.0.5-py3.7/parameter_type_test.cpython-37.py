# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/modules/parameter_type_test.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 5059 bytes
"""ParameterTypeTest class"""
import unittest
from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
from modules.parameter_type import ParameterType
MODULE_NAME = PARAMETER_TYPE

class ParameterTypeTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.mdc_client = MetadataClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
          base_api_url=BASE_API_URL)
        _ParameterTypeTest__unique_name1 = Generators.generate_unique_name('ParameterType01')
        _ParameterTypeTest__unique_identifier1 = Generators.generate_unique_identifier()
        self.exp_typ_01 = {'name':_ParameterTypeTest__unique_name1, 
         'identifier':_ParameterTypeTest__unique_identifier1, 
         'flg_available':'true', 
         'description':'desc 01'}
        _ParameterTypeTest__unique_name_upd = Generators.generate_unique_name('paramTypeUpd1')
        _ParameterTypeTest__unique_identifier_upd = Generators.generate_unique_identifier(1)
        self.exp_typ_01_upd = {'name':_ParameterTypeTest__unique_name_upd, 
         'identifier':_ParameterTypeTest__unique_identifier_upd, 
         'flg_available':'false', 
         'description':'desc 01 Updated!'}

    def test_create_parameter_type(self):
        exp_typ_01 = ParameterType(metadata_client=(self.mdc_client),
          name=(self.exp_typ_01['name']),
          identifier=(self.exp_typ_01['identifier']),
          flg_available=(self.exp_typ_01['flg_available']),
          description=(self.exp_typ_01['description']))
        result1 = exp_typ_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.exp_typ_01)
        parameter_type = result1['data']
        parameter_type_id = result1['data']['id']
        parameter_type_name = result1['data']['name']
        exp_typ_01_dup = exp_typ_01
        result2 = exp_typ_01_dup.create()
        expect_app_info = {'name': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)
        result3 = ParameterType.get_by_name(self.mdc_client, parameter_type_name)
        self.assert_find_success(MODULE_NAME, result3, self.exp_typ_01)
        result4 = ParameterType.get_by_id(self.mdc_client, parameter_type_id)
        self.assert_find_success(MODULE_NAME, result4, self.exp_typ_01)
        result5 = ParameterType.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)
        exp_typ_01.name = self.exp_typ_01_upd['name']
        exp_typ_01.identifier = self.exp_typ_01_upd['identifier']
        exp_typ_01.flg_available = self.exp_typ_01_upd['flg_available']
        exp_typ_01.description = self.exp_typ_01_upd['description']
        result6 = exp_typ_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.exp_typ_01_upd)
        exp_typ_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM__'
        exp_typ_01.flg_available = self.exp_typ_01_upd['flg_available']
        exp_typ_01.description = self.exp_typ_01_upd['description']
        result7 = exp_typ_01.update()
        expect_app_info = {'name': ['is too long (maximum is 60 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)
        result8 = exp_typ_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)
        result9 = exp_typ_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)


if __name__ == '__main__':
    unittest.main()