# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/modules/module_base.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 4604 bytes
"""BaseTest Class with helper methods common to all modules tests"""
import unittest
from common.util import Util

class ModuleBase(Util, unittest.TestCase):

    def assert_create_success(self, module_name, receive, exp_data):
        msg = '{0} created successfully'.format(module_name)
        exp = {'success':True,  'info':msg,  'app_info':{},  'data':exp_data}
        self._ModuleBase__assert_success(receive, exp)

    def assert_find_success(self, module_name, receive, exp_data):
        msg = 'Got {0} successfully'.format(module_name)
        exp = {'success':True,  'info':msg,  'app_info':{},  'data':exp_data}
        self._ModuleBase__assert_success(receive, exp)

    def assert_not_found_success(self, module_name, receive, exp_data, unique_id):
        if unique_id:
            msg = '{0} "{1}" could not be found!'.format(module_name, unique_id)
        else:
            info_msg = 'No {0} could be found respecting the specified search criteria'
            msg = info_msg.format(module_name)
        exp = {'success':True,  'info':msg,  'app_info':{},  'data':exp_data}
        self._ModuleBase__assert_success(receive, exp)

    def assert_update_success(self, module_name, receive, exp_data):
        msg = '{0} updated successfully'.format(module_name)
        exp = {'success':True,  'info':msg,  'app_info':{},  'data':exp_data}
        self._ModuleBase__assert_success(receive, exp)

    def assert_delete_success(self, module_name, receive):
        msg = '{0} deleted successfully'.format(module_name)
        exp = {'success':True,  'info':msg,  'app_info':{},  'data':{}}
        self._ModuleBase__assert_success(receive, exp)

    def assert_set_success(self, module_name, receive, exp_data):
        msg = '{0} set successfully'.format(module_name)
        exp = {'success':True,  'info':msg,  'app_info':{},  'data':exp_data}
        self._ModuleBase__assert_success(receive, exp)

    def assert_create_error(self, module_name, receive, exp_info):
        msg = 'Error creating {0}'.format(module_name)
        exp = {'success':False,  'info':msg,  'app_info':exp_info,  'data':{}}
        self._ModuleBase__assert_error(receive, exp)

    def assert_find_error(self, module_name, receive, exp_info):
        msg = '{0} not found!'.format(module_name)
        exp = {'success':False,  'info':msg,  'app_info':exp_info,  'data':{}}
        self._ModuleBase__assert_error(receive, exp)

    def assert_update_error(self, module_name, receive, exp_info):
        msg = 'Error updating {0}'.format(module_name)
        exp = {'success':False,  'info':msg,  'app_info':exp_info,  'data':{}}
        self._ModuleBase__assert_error(receive, exp)

    def assert_delete_error(self, module_name, receive, exp_info):
        msg = 'Error deleting {0}'.format(module_name)
        exp = {'success':False,  'info':msg,  'app_info':exp_info,  'data':{}}
        self._ModuleBase__assert_error(receive, exp)

    def assert_set_error(self, module_name, receive, exp_info):
        msg = 'Error setting {0}'.format(module_name)
        exp = {'success':False,  'info':msg,  'app_info':exp_info,  'data':{}}
        self._ModuleBase__assert_error(receive, exp)

    def __assert_success(self, receive, expect):
        field = 'app_info'
        self.assert_eq_val(receive[field], {})
        expect_data = expect['data']
        if type(expect_data) is list and len(expect_data) > 0:
            for i in range(0, len(expect_data)):
                self.fields_validation(receive['data'][i], expect['data'][i])

        else:
            if type(expect_data) is dict and len(expect_data) > 0:
                self.fields_validation(receive['data'], expect['data'])
            else:
                self.assert_eq_val(receive[field], expect[field])
        field = 'info'
        self.assert_eq_val(receive[field], expect[field])
        field = 'success'
        self.assert_eq_val(receive[field], expect[field])

    def __assert_error(self, receive, expect):
        field = 'app_info'
        expect_app_info = expect[field]
        if type(expect_app_info) is dict and len(expect_app_info) > 0:
            for key, val in expect_app_info.items():
                self.assert_eq_val(receive[field][key], expect_app_info[key])

        else:
            self.assert_eq_val(receive[field], expect[field])
        field = 'data'
        self.assert_eq_val(receive[field], expect[field])
        field = 'info'
        self.assert_eq_val(receive[field], expect[field])
        field = 'success'
        self.assert_eq_val(receive[field], expect[field])