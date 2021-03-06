# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/data_group_api_test.py
# Compiled at: 2020-02-20 08:00:45
# Size of source mod 2**32: 8061 bytes
"""DataGroupApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
from ...metadata_client_api import MetadataClientApi

class DataGroupApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)

    def test_create_data_group_api(self):
        _DataGroupApiTest__unique_name = Generators.generate_unique_name('DataGroupApi')
        data_group = {'data_group': {'name':_DataGroupApiTest__unique_name, 
                        'language':'en', 
                        'data_group_type_id':'1', 
                        'experiment_id':'-1', 
                        'user_id':'-1', 
                        'prefix_path':'/webstorage/original/path/.../', 
                        'flg_available':'true', 
                        'flg_writing':'false', 
                        'flg_public':'false', 
                        'format':'this is a format!', 
                        'data_passport':'this is a data passport!', 
                        'removed_at':'2099-05-25T08:30:00.000+02:00', 
                        'description':'desc 01'}}
        expect = data_group['data_group']
        received = self._DataGroupApiTest__create_entry_api(data_group, expect)
        data_group_id = received['id']
        data_group_name = received['name']
        data_group_type_id = received['data_group_type_id']
        data_group_prefix_path = received['prefix_path']
        expect['doi'] = received['doi']
        received = self._DataGroupApiTest__create_duplicate_api(data_group, expect)
        data_group_dup_id = received['id']
        self._DataGroupApiTest__get_all_entries_by_name_api(data_group_name, expect)
        self._DataGroupApiTest__get_entry_by_id_api(data_group_id, expect)
        self._DataGroupApiTest__update_entry_api(data_group_id, data_group_name, data_group_type_id, data_group_prefix_path, expect)
        self._DataGroupApiTest__delete_entry_by_id_api(data_group_id)
        self._DataGroupApiTest__delete_entry_by_id_api(data_group_dup_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'language', STRING)
        self.assert_eq_hfield(receive, expect, 'data_group_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'experiment_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'user_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'prefix_path', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_writing', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_public', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'format', STRING)
        self.assert_eq_hfield(receive, expect, 'data_passport', STRING)
        self.assert_eq_hfield(receive, expect, 'removed_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        expected_doi = {'doi': 'xfel.mdc.dg.{0}'.format(receive['id'])}
        self.assert_eq_hfield(receive, expected_doi, 'doi', STRING)

    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_data_group_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_duplicate_api(self, entry_info, expect):
        response = self.client_api.create_data_group_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __update_entry_api(self, entry_id, entry_name, entry_data_group_type_id, entry_path, expect):
        data_group_upd = {'data_group': {'name':entry_name, 
                        'language':'pt', 
                        'doi':'It is not possible to updated doi!', 
                        'data_group_type_id':entry_data_group_type_id, 
                        'experiment_id':'-1', 
                        'user_id':'-1', 
                        'prefix_path':entry_path, 
                        'flg_available':'false', 
                        'flg_writing':'true', 
                        'flg_public':'true', 
                        'format':'this is an updated format!', 
                        'data_passport':'this is an updated data passport!', 
                        'removed_at':'2100-05-25T08:30:00.000+02:00', 
                        'description':'desc 01 updated!!!'}}
        response = self.client_api.update_data_group_api(entry_id, data_group_upd)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect_upd = data_group_upd['data_group']
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)
        field = 'name'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'prefix_path'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'language'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'doi'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        self.assert_eq_str(expect[field], receive[field])
        field = 'data_group_type_id'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'experiment_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'user_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_writing'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_public'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'format'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'data_passport'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'removed_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_name_api(self, name, expect):
        response = self.client_api.get_all_data_groups_by_name_api(name)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_data_group_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_data_group_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()