# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/modules/condition_test.py
# Compiled at: 2019-08-05 13:13:33
# Size of source mod 2**32: 10889 bytes
"""ConditionTest class"""
import unittest
from calibration_client.calibration_client import CalibrationClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.condition import Condition
MODULE_NAME = CONDITION

class ConditionTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.cal_client = CalibrationClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
          base_api_url=BASE_API_URL)
        _ConditionTest__parameters_conditions_attr_01 = [
         {'parameter_id':'-1', 
          'value':'2.5', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'},
         {'parameter_id':'-2', 
          'value':'1.5', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'}]
        _ConditionTest__parameters_conditions_attr_02 = [
         {'parameter_id':'-1', 
          'value':'2.4', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'},
         {'parameter_id':'-2', 
          'value':'1.3', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'}]
        _ConditionTest__parameters_conditions_attr_03 = [
         {'parameter_id':'-1', 
          'value':'2.7', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'},
         {'parameter_id':'-2', 
          'value':'1.8', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'}]
        _ConditionTest__parameters_conditions_attr_02 = [
         {'parameter_id':'-1', 
          'value':'2.4', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:see_tests'},
         {'parameter_id':'-2', 
          'value':'1.3', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:see_tests'}]
        _ConditionTest__parameters_conditions_attr_03 = [
         {'parameter_id':'-1', 
          'value':'2.7', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:see_tests'},
         {'parameter_id':'-2', 
          'value':'1.8', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:see_tests'}]
        _ConditionTest__unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'
        self.cond_01 = {'name':_ConditionTest__unique_name, 
         'flg_available':'true', 
         'event_at':'2019-07-20 09:14:52', 
         'description':'Created automatically via seed:seed_tests', 
         'parameters_conditions_attributes':_ConditionTest__parameters_conditions_attr_01}
        self.cond_02 = {'name':'CONDITION_TEST-2_DO_NOT_DELETE', 
         'flg_available':'true', 
         'event_at':'2019-07-20 09:14:52', 
         'description':'Created automatically via seed:seed_tests', 
         'parameters_conditions_attributes':_ConditionTest__parameters_conditions_attr_02}
        self.cond_03 = {'name':'CONDITION_TEST-3_DO_NOT_DELETE', 
         'flg_available':'true', 
         'event_at':'2019-07-20 09:14:52', 
         'description':'Created automatically via seed:seed_tests', 
         'parameters_conditions_attributes':_ConditionTest__parameters_conditions_attr_03}
        _ConditionTest__unique_name_upd = Generators.generate_unique_name('ConditionUpd01')
        self.cond_01_upd = {'name':_ConditionTest__unique_name, 
         'flg_available':'true', 
         'event_at':'2019-07-20 09:14:52', 
         'description':'Created automatically via seed:seed_tests', 
         'parameters_conditions_attributes':_ConditionTest__parameters_conditions_attr_01}

    def test_create_condition(self):
        cond_01 = Condition(calibration_client=(self.cal_client),
          name=(self.cond_01['name']),
          flg_available=(self.cond_01['flg_available']),
          event_at=None,
          parameters_conditions_attributes=(self.cond_01['parameters_conditions_attributes']),
          description=(self.cond_01['description']))
        result1 = cond_01.set_expected()
        self.assert_find_success(MODULE_NAME, result1, self.cond_01)
        condition = result1['data']
        condition_id = result1['data']['id']
        condition_name = result1['data']['name']
        cond_01_dup = cond_01
        result2 = cond_01_dup.set_expected()
        self.assert_find_success(MODULE_NAME, result2, self.cond_01)
        result3 = cond_01.get_expected()
        self.assert_find_success(MODULE_NAME, result3, self.cond_01)
        res4 = cond_01.get_possible()
        possible_conditions_list = [self.cond_03, self.cond_02, self.cond_01]
        self.assert_find_success(MODULE_NAME, res4, possible_conditions_list)
        cond_01.parameters_conditions_attributes[0]['value'] = '200'
        result5 = cond_01.get_expected()
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

    def test_create_condition_from_dict_success(self):
        _ConditionTest__parameters_01 = [
         {'parameter_id':'-1', 
          'value':'2.5', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'},
         {'parameter_id':'-2', 
          'value':'1.5', 
          'lower_deviation_value':'0.5', 
          'upper_deviation_value':'0.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'}]
        _ConditionTest__unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'
        cond_dict = {'name':_ConditionTest__unique_name, 
         'flg_available':'true', 
         'description':'Created automatically via seed:seed_tests', 
         'parameters_conditions_attributes':_ConditionTest__parameters_01}
        resp = Condition.set_condition_from_dict(self.cal_client, cond_dict)
        expect = {'id':-1, 
         'flg_available':True, 
         'name':'CONDITION_TEST-1_DO_NOT_DELETE', 
         'description':'Created automatically via seed:seed_tests', 
         'num_parameters':2}
        msg = 'Got {0} successfully'.format(MODULE_NAME)
        expect = {'success':True,  'info':msg,  'app_info':{},  'data':expect}
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['info'], expect['info'])
        self.assert_eq_val(resp['success'], expect['success'])
        expect_data = expect['data']
        if type(expect_data) is dict:
            if len(expect_data) > 0:
                for key, val in expect_data.items():
                    self.assert_eq_val(resp['data'][key], expect_data[key])

        else:
            self.assert_eq_val(resp['data'], expect_data)

    def test_create_condition_from_dict_error(self):
        _ConditionTest__parameters_01 = [
         {'parameter_id':'-1', 
          'value':'100.5', 
          'lower_deviation_value':'10.5', 
          'upper_deviation_value':'10.5', 
          'flg_available':'true', 
          'description':'Created automatically via seed:seed_tests'}]
        _ConditionTest__unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'
        expect = {'name':_ConditionTest__unique_name, 
         'flg_available':'true', 
         'description':'Created automatically via seed:seed_tests', 
         'parameters_conditions_attributes':_ConditionTest__parameters_01}
        resp = Condition.set_condition_from_dict(self.cal_client, expect)
        expect_app_info = {'name': ['has already been taken']}
        self.assert_find_error(MODULE_NAME, resp, expect_app_info)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        num_params = len(expect['parameters_conditions_attributes'])
        num_params_h = {'num_parameters': num_params}
        self.assert_eq_hfield(receive, num_params_h, 'num_parameters', NUMBER)


if __name__ == '__main__':
    unittest.main()