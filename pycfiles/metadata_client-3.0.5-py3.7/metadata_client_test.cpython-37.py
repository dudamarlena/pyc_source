# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/metadata_client_test.py
# Compiled at: 2019-11-13 06:16:26
# Size of source mod 2**32: 52274 bytes
"""MetadataClientTest class"""
import logging, unittest
from metadata_client.metadata_client import MetadataClient
from .common.config_test import *
from .common.secrets import *
from modules.module_base import ModuleBase

class MetadataClientTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.mdc_client = MetadataClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
          base_api_url=BASE_API_URL)

    def test_get_data_group_types(self):
        resp = MetadataClient.get_all_data_group_types(self.mdc_client)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got data_group_type successfully')
        first_dgt = resp['data'][0]
        self.assert_eq_val(first_dgt['id'], 1)
        self.assert_eq_val(first_dgt['name'], 'Raw')
        self.assert_eq_val(first_dgt['identifier'], 'RAW')
        self.assert_eq_val(first_dgt['flg_available'], True)
        self.assert_eq_val(first_dgt['description'], '')

    def test_get_proposal_experiments(self):
        proposal_number = 0
        resp = MetadataClient.get_proposal_experiments(self.mdc_client, proposal_number)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got experiment successfully')
        first_exp = resp['data'][0]
        self.assert_eq_val(first_exp['id'], -1)
        self.assert_eq_val(first_exp['name'], 'TestExperiment DO NOT DELETE!')
        self.assert_eq_val(first_exp['doi'], 'xfel.mdc.exp.-1')
        self.assert_eq_val(first_exp['experiment_number'], 1)
        self.assert_eq_val(first_exp['flg_available'], True)
        self.assert_eq_val(first_exp['proposal_id'], -1)
        self.assert_eq_val(first_exp['experiment_type_id'], 1)
        self.assert_eq_val(first_exp['experiment_folder'], 'e0001')
        self.assert_eq_val(first_exp['publisher'], 'XFEL')
        self.assert_eq_val(first_exp['contributor'], 'XFEL')
        self.assert_eq_val(first_exp['description'], '')

    def test_get_active_proposal_by_instrument(self):
        instrument_id = -2
        resp = MetadataClient.get_active_proposal_by_instrument(self.mdc_client, instrument_id)
        self.assert_eq_val(resp['app_info'], 'Resource not found!')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['info'], 'proposal not found!')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_experiments_with_errors(self):
        proposal_number = -99
        resp = MetadataClient.get_proposal_experiments(self.mdc_client, proposal_number)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], 'proposal not found!')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], 'Proposal number -99 not found')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_runs(self):
        proposal_number = 0
        resp = MetadataClient.get_proposal_runs(self.mdc_client, proposal_number)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got proposal successfully')
        first_run = resp['data']['runs'][0]
        self.assert_eq_val(first_run['id'], -1)
        self.assert_eq_val(first_run['run_number'], 0)
        self.assert_eq_val(first_run['flg_status'], 1)
        self.assert_eq_val(first_run['flg_run_quality'], -1)
        self.assert_eq_val(first_run['num_files'], 0)
        first_repo = first_run['repositories']['XFEL_TESTS_REPO']
        self.assert_eq_val(first_repo['name'], 'XFEL Tests Repository')
        self.assert_eq_val(first_repo['mount_point'], '/webstorage/XFEL')
        self.assert_eq_val(first_repo['data_groups'], 1)

    def test_get_proposal_runs_with_errors(self):
        proposal_number = -99
        resp = MetadataClient.get_proposal_runs(self.mdc_client, proposal_number)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], 'proposal not found!')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], 'Proposal number -99 not found')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_samples(self):
        proposal_number = 0
        resp = MetadataClient.get_proposal_samples(self.mdc_client, proposal_number)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got sample successfully')
        first_exp = resp['data'][0]
        self.assert_eq_val(first_exp['id'], -1)
        self.assert_eq_val(first_exp['name'], 'TestSample DO NOT DELETE!')
        self.assert_eq_val(first_exp['proposal_id'], -1)
        self.assert_eq_val(first_exp['sample_type_id'], 1)
        self.assert_eq_val(first_exp['flg_available'], True)
        self.assert_eq_val(first_exp['url'], 'https://www.google.com')
        self.assert_eq_val(first_exp['description'], '')

    def test_get_proposal_samples_with_errors(self):
        proposal_number = -99
        resp = MetadataClient.get_proposal_samples(self.mdc_client, proposal_number)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], 'proposal not found!')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], 'Proposal number -99 not found')
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_invalid_keys(self):
        experiment_id = None
        sample_id = None
        run_dict = {}
        data_grp_dict = {}
        resp = MetadataClient.register_run(self.mdc_client, experiment_id, sample_id, run_dict, data_grp_dict)
        logging.error('resp: {0}'.format(resp))
        exp_info = "The following fields are mandatory: ['experiment_id', 'run.run_number', 'run.begin_at', 'run.first_train', 'data_group.data_group_type_id', 'data_group.creator_id', 'data_group.prefix_path']"
        self.assert_eq_val(resp['info'], exp_info)
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_app_error_in_run(self):
        experiment_id = -1
        sample_id = -1
        run_dict = {'run_number':125, 
         'begin_at':'2014-06-25T08:30:00.000+02:00', 
         'first_train':None}
        _MetadataClientTest__prefix_path = '/webstorage/XFEL/raw/SPB/2016_01/p0008/e0001/'
        data_grp_dict = {'data_group_type_id':'1',  'creator_id':'-1', 
         'prefix_path':_MetadataClientTest__prefix_path}
        resp = MetadataClient.register_run(self.mdc_client, experiment_id, sample_id, run_dict, data_grp_dict)
        logging.error('resp: {0}'.format(resp))
        app_info = {'first_train': ["can't be blank", 'is not a number']}
        self.assert_eq_val(resp['info'], 'Error creating run')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_app_error_in_data_group(self):
        experiment_id = -1
        sample_id = -1
        run_number_val = 126
        run_dict = {'run_number':run_number_val,  'begin_at':'2014-06-25T08:30:00.000+02:00', 
         'first_train':126}
        data_grp_dict = {'data_group_type_id':'1', 
         'creator_id':'-1', 
         'prefix_path':None}
        resp = MetadataClient.register_run(self.mdc_client, experiment_id, sample_id, run_dict, data_grp_dict)
        logging.error('resp: {0}'.format(resp))
        app_info = {'prefix_path': ["can't be blank",
                         'is too short (minimum is 2 characters)']}
        self.assert_eq_val(resp['info'], 'Error creating data_group')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_success(self):
        run_info = self._MetadataClientTest__test_successful_register_run()
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_register_run_data_with_invalid_keys(self):
        experiment_id = None
        sample_id = None
        run_id = None
        data_group_id = None
        data_group_dict = {}
        data_group_files_ar = []
        resp = MetadataClient.register_run_data(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, data_group_dict, data_group_files_ar)
        logging.error('resp: {0}'.format(resp))
        exp_info = "The following fields are mandatory: ['experiment_id', 'run_id', 'data_group_id', 'data_group_files']"
        self.assert_eq_val(resp['info'], exp_info)
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_invalid_keys_2(self):
        experiment_id = None
        sample_id = None
        run_id = None
        data_group_id = None
        data_group_dict = {'language': 'pt'}
        data_group_files_ar = [{'filename':'s0000.h5',  'sequence':11},
         {'relative_path':'r0001/', 
          'sequence':11},
         {'sequence': 11}]
        resp = MetadataClient.register_run_data(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, data_group_dict, data_group_files_ar)
        logging.error('resp: {0}'.format(resp))
        exp_info = "The following fields are mandatory: ['experiment_id', 'run_id', 'data_group_id', 'data_group.data_group_type_id', 'data_group.creator_id', 'data_group_files[0].relative_path', 'data_group_files[1].filename', 'data_group_files[2].filename', 'data_group_files[2].relative_path']"
        self.assert_eq_val(resp['info'], exp_info)
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_app_error_in_data_group(self):
        run_info = self._MetadataClientTest__test_successful_register_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_group_dict = {'data_group_type_id':2, 
         'creator_id':-999, 
         'name':'just a new name', 
         'prefix_path':'bla_bla'}
        data_group_files_ar = [
         {'filename':'s0000.h5',  'sequence':11, 
          'relative_path':'r0001/'}]
        resp = MetadataClient.register_run_data(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, data_group_dict, data_group_files_ar)
        logging.error('resp: {0}'.format(resp))
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)
        app_info = {'name':[
          'cannot be updated'], 
         'data_group_type_id':[
          'cannot be updated'], 
         'prefix_path':[
          'cannot be updated']}
        self.assert_eq_val(resp['info'], 'Error updating data_group')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_app_error_in_data_group_files(self):
        run_info = self._MetadataClientTest__test_successful_register_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_group_dict = {'data_group_type_id':1, 
         'creator_id':-1}
        data_group_files_ar = [{'filename':'1',  'relative_path':'1'}]
        resp = MetadataClient.register_run_data(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, data_group_dict, data_group_files_ar)
        logging.error('resp: {0}'.format(resp))
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)
        app_info = {'files': ['is too short (minimum is 40 characters)']}
        self.assert_eq_val(resp['info'], 'Error creating data_file')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_success(self):
        run_data_info = self._MetadataClientTest__test_successful_register_data_run()
        data_file_id = run_data_info['data_file_id']
        run_id = run_data_info['run_id']
        run_number = run_data_info['run_number']
        data_group_id = run_data_info['data_group_id']
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_keys_of_wrong_type(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = ''
        dg_parameters_dict = []
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_dict)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], "The following fields are mandatory: ['run must be a hash', 'run.end_at', 'run.last_train', 'parameters must be a Hash']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_invalid_keys(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'first_train': 100}
        dg_parameters_dict = {}
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_dict)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], "The following fields are mandatory: ['run.end_at', 'run.last_train']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_invalid_keys_2(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'first_train': 100}
        dg_parameters_dict = {'parameters': [{}]}
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_dict)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], "The following fields are mandatory: ['run.end_at', 'run.last_train', 'parameters[0].data_source', 'parameters[0].name', 'parameters[0].value', 'parameters[0].minimum', 'parameters[0].maximum', 'parameters[0].mean', 'parameters[0].standard_deviation', 'parameters[0].data_type_id', 'parameters[0].parameter_type_id', 'parameters[0].unit_id']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_invalid_keys_3(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'first_train': 100}
        dg_parameters_dict = {'parameters': ''}
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_dict)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], "The following fields are mandatory: ['run.end_at', 'run.last_train', 'parameters[0].data_source', 'parameters[0].name', 'parameters[0].value', 'parameters[0].minimum', 'parameters[0].maximum', 'parameters[0].mean', 'parameters[0].standard_deviation', 'parameters[0].data_type_id', 'parameters[0].parameter_type_id', 'parameters[0].unit_id']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_app_error_in_run(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'run_number':1234, 
         'end_at':'2015-06-25T08:30:00.000+02:00', 
         'last_train':-1, 
         'flg_available':1, 
         'flg_status':1}
        dg_parameters_ar = {'parameters': [
                        {'data_source':'MID/XTD6/ATT/MOTOR/BLADE_TOP', 
                         'name':'Velocity Right', 
                         'value':15.6, 
                         'minimum':15.6, 
                         'maximum':15.6, 
                         'mean':15.6, 
                         'standard_deviation':15.6, 
                         'data_type_id':2, 
                         'parameter_type_id':3, 
                         'unit_id':1}]}
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_ar)
        logging.error('resp: {0}'.format(resp))
        cannot_update_ar = [
         'cannot be updated']
        must_be_greater_ar = ['must be greater than or equal to 126']
        self.assert_eq_val(resp['info'], 'Error updating run')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['data'], {})
        self.assert_eq_val(resp['app_info']['run_number'], cannot_update_ar)
        self.assert_eq_val(resp['app_info']['run_folder'], cannot_update_ar)
        self.assert_eq_val(resp['app_info']['last_train'], must_be_greater_ar)
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_app_error_in_parameters(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {}
        dg_parameters_ar = {'parameters': [
                        {'data_source':'MID/XTD6/ATT/MOTOR/BLADE_TOP', 
                         'name':'', 
                         'value':15.6, 
                         'minimum':15.6, 
                         'maximum':15.6, 
                         'mean':15.6, 
                         'standard_deviation':15.6, 
                         'data_type_id':2, 
                         'parameter_type_id':3, 
                         'unit_id':1}]}
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_ar)
        logging.error('resp: {0}'.format(resp))
        cannot_be_blank_ar = [
         "can't be blank"]
        self.assert_eq_val(resp['info'], 'Error creating parameter')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['data'], {})
        self.assert_eq_val(resp['app_info'][0]['name'], cannot_be_blank_ar)
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_success(self):
        run_info = self._MetadataClientTest__test_successful_close_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_parameters_by_data_group_id(data_group_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def test_register_run_replica_with_success(self):
        run_info = self._MetadataClientTest__test_successful_close_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        proposal_number = '000000'
        repository_identifier = 'XFEL_GPFS_OFFLINE_RAW_CC'
        repository_id = 11
        resp_reg = MetadataClient.register_run_replica(self.mdc_client, proposal_number, run_number, repository_identifier)
        logging.error('resp: {0}'.format(resp_reg))
        self.assert_eq_val(resp_reg['info'], 'Run replica registered successfully')
        self.assert_eq_val(resp_reg['success'], True)
        self.assert_eq_val(resp_reg['app_info'], {})
        resp_reg_data = resp_reg['data']
        self.assert_eq_val(resp_reg_data[0]['data_group_id'], data_group_id)
        self.assert_eq_val(resp_reg_data[0]['repository_id'], repository_id)
        self.assert_eq_val(resp_reg_data[0]['flg_available'], True)
        self.assert_eq_val(len(resp_reg_data), 1)
        resp_unreg = MetadataClient.unregister_run_replica(self.mdc_client, proposal_number, run_number, repository_identifier)
        logging.error('resp: {0}'.format(resp_unreg))
        self.assert_eq_val(resp_unreg['info'], 'Run replica unregistered successfully')
        self.assert_eq_val(resp_unreg['success'], True)
        self.assert_eq_val(resp_unreg['app_info'], {})
        resp_unreg_data = resp_unreg['data']
        self.assert_eq_val(resp_unreg_data[0]['data_group_id'], data_group_id)
        self.assert_eq_val(resp_unreg_data[0]['repository_id'], repository_id)
        self.assert_eq_val(resp_unreg_data[0]['flg_available'], False)
        self.assert_eq_val(len(resp_unreg_data), 1)
        self._MetadataClientTest__test_delete_data_file_by_id(data_file_id)
        self._MetadataClientTest__test_delete_run_by_id(run_id)
        self._MetadataClientTest__test_delete_parameters_by_data_group_id(data_group_id)
        self._MetadataClientTest__test_delete_data_group_by_id(data_group_id)

    def __test_successful_register_run(self):
        experiment_id = -1
        sample_id = -1
        run_number_val = 126
        run_dict = {'run_number':run_number_val,  'begin_at':'2014-06-25T08:30:00.000+02:00', 
         'first_train':126}
        _MetadataClientTest__prefix_path = '/webstorage/XFEL/raw/SPB/2016_01/p0008/e0001/'
        data_grp_dict = {'data_group_type_id':'1',  'creator_id':'-1', 
         'prefix_path':_MetadataClientTest__prefix_path}
        resp = MetadataClient.register_run(self.mdc_client, experiment_id, sample_id, run_dict, data_grp_dict)
        logging.error('resp: {0}'.format(resp))
        run_id = resp['data']['run_id']
        data_group_id = resp['data']['data_group_id']
        self.assert_eq_val(resp['info'], 'Run registered successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data']['experiment_id'], experiment_id)
        self.assert_eq_val(resp['data']['sample_id'], sample_id)
        self.assert_not_eq_str(run_id, '', 'run_id')
        self.assert_not_eq_str(data_group_id, '', 'data_group_id')
        return {'experiment_id':experiment_id, 
         'sample_id':sample_id, 
         'run_id':run_id, 
         'run_number':run_number_val, 
         'data_group_id':data_group_id}

    def __test_successful_register_data_run(self):
        run_info = self._MetadataClientTest__test_successful_register_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_group_dict = {'data_group_type_id':1, 
         'creator_id':-1}
        data_group_files_ar = [
         {'filename':'s0000.h5',  'sequence':11, 
          'relative_path':'r0001/'}]
        resp = MetadataClient.register_run_data(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, data_group_dict, data_group_files_ar)
        logging.error('resp: {0}'.format(resp))
        data_file_id = resp['data']['data_file_id']
        self.assert_eq_val(resp['info'], 'Run data registered successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data']['experiment_id'], experiment_id)
        self.assert_eq_val(resp['data']['sample_id'], sample_id)
        self.assert_eq_val(resp['data']['run_id'], run_id)
        self.assert_eq_val(resp['data']['data_group_id'], data_group_id)
        self.assert_not_eq_str(data_file_id, '', 'data_file_id')
        return {'experiment_id':experiment_id, 
         'sample_id':sample_id, 
         'run_id':run_id, 
         'run_number':run_number, 
         'data_group_id':data_group_id, 
         'data_file_id':data_file_id}

    def __test_successful_close_run(self):
        run_info = self._MetadataClientTest__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'end_at':'2015-06-25T08:30:00.000+02:00', 
         'last_train':127, 
         'flg_available':1, 
         'flg_status':1}
        dg_parameters_ar = {'parameters': [
                        {'data_source':'MID/XTD6/ATT/MOTOR/BLADE_TOP', 
                         'name':'VelocityLeft', 
                         'value':15.6, 
                         'minimum':15.6, 
                         'maximum':15.6, 
                         'mean':15.6, 
                         'standard_deviation':15.6, 
                         'data_type_id':2, 
                         'parameter_type_id':3, 
                         'unit_id':1}]}
        resp = MetadataClient.close_run(self.mdc_client, experiment_id, sample_id, run_id, data_group_id, run_dict, dg_parameters_ar)
        logging.error('resp: {0}'.format(resp))
        self.assert_eq_val(resp['info'], 'Run closed successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data']['sample_id'], sample_id)
        self.assert_eq_val(resp['data']['run_id'], run_id)
        self.assert_eq_val(resp['data']['experiment_id'], experiment_id)
        return {'experiment_id':experiment_id, 
         'sample_id':sample_id, 
         'run_id':run_id, 
         'run_number':run_number, 
         'data_group_id':data_group_id, 
         'data_file_id':data_file_id}

    def __test_delete_run_by_id(self, run_id):
        resp_api = self.mdc_client.delete_run_api(run_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT, RUN)
        self.assert_eq_val(resp['info'], 'run deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def __test_delete_parameters_by_data_group_id(self, data_group_id):
        resp_api = self.mdc_client.delete_bulk_parameter_api_by_data_group_id(data_group_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT, PARAMETER)
        self.assert_eq_val(resp['info'], 'parameter deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def __test_delete_data_group_by_id(self, data_group_id):
        resp_api = self.mdc_client.delete_data_group_api(data_group_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT, DATA_GROUP)
        self.assert_eq_val(resp['info'], 'data_group deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def __test_delete_data_file_by_id(self, data_file_id):
        resp_api = self.mdc_client.delete_data_file_api(data_file_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT, DATA_FILE)
        self.assert_eq_val(resp['info'], 'data_file deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})


if __name__ == '__main__':
    unittest.main()