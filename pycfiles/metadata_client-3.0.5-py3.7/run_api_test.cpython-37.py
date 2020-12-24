# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/run_api_test.py
# Compiled at: 2020-02-20 06:10:10
# Size of source mod 2**32: 8482 bytes
"""RunApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
from ...metadata_client_api import MetadataClientApi

class RunApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)

    def test_create_run_api(self):
        _RunApiTest__unique_name = Generators.generate_unique_id()
        run = {RUN: {'run_number':_RunApiTest__unique_name, 
               'run_alias':'Run_Alias', 
               'experiment_id':'-1', 
               'sample_id':'-1', 
               'begin_at':'2014-05-25T08:30:00.000+02:00', 
               'end_at':'2015-05-25T08:30:00.000+02:00', 
               'first_train':'1', 
               'last_train':'999', 
               'flg_available':'true', 
               'flg_status':'1', 
               'original_format':'', 
               'system_msg':'', 
               'description':'desc 01'}}
        expect = run[RUN]
        received = self._RunApiTest__create_entry_api(run, expect)
        run_id = received['id']
        run_number = received['run_number']
        experiment_id = received['experiment_id']
        self._RunApiTest__create_error_entry_uk_api(run)
        self._RunApiTest__get_all_entries_by_run_number_api(run_number, expect)
        self._RunApiTest__get_entry_by_id_api(run_id, expect)
        self._RunApiTest__get_entry_by_run_number_and_experiment_id_api(run_number, experiment_id, expect)
        self._RunApiTest__update_entry_api(run_id, run_number, expect)
        self._RunApiTest__delete_entry_by_id_api(run_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'run_number', NUMBER)
        self.assert_eq_hfield(receive, expect, 'experiment_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'sample_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'begin_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'end_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'first_train', NUMBER)
        self.assert_eq_hfield(receive, expect, 'last_train', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_status', NUMBER)
        self.assert_eq_hfield(receive, expect, 'original_format', STRING)
        self.assert_eq_hfield(receive, expect, 'system_msg', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        expect['run_folder'] = 'r{0:04d}'.format(expect['run_number'])
        self.assert_eq_hfield(receive, expect, 'run_folder', STRING)

    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_run_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_run_api(entry_info)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {'info': {'experiment_id':['has already been taken'],  'run_number':[
                   'must be unique per proposal',
                   'has already been taken']}}
        self.assertEqual(receive, expect, 'Expected result not received')
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)
        receive_msg = receive['info']['run_number'][0]
        expect_msg = expect['info']['run_number'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, run_number, expect):
        run_upd = {RUN: {'run_number':run_number, 
               'run_alias':'Run_Alias_Updated...', 
               'experiment_id':'-1', 
               'sample_id':'-1', 
               'begin_at':'2014-06-25T08:30:00.000+02:00', 
               'end_at':'2015-06-25T08:30:00.000+02:00', 
               'first_train':9223372036854775802, 
               'last_train':9223372036854775807, 
               'flg_available':'false', 
               'flg_status':'-1', 
               'original_format':'format updated', 
               'system_msg':'system msg update', 
               'description':'desc 01 updated!!!'}}
        res = self.client_api.update_run_api(entry_id, run_upd)
        resp_content = self.load_response_content(res)
        receive = resp_content
        run_upd[RUN]['unit_id'] = '-1'
        expect_upd = run_upd[RUN]
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(res.status_code, OK)
        field = 'run_number'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'run_alias'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'begin_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'end_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'first_train'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'last_train'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_status'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'original_format'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'system_msg'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_run_number_api(self, run_number, expect):
        response = self.client_api.get_all_runs_by_run_number_api(run_number)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_run_number_and_experiment_id_api(self, run_number, experiment_id, expect):
        response = self.client_api.get_run_by_run_number_and_experiment_id_api(run_number, experiment_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_run_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_run_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()