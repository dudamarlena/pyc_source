# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/modules/parameter.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 5153 bytes
"""Parameter module class"""
from apis.parameter_api import ParameterApi
from common.base import Base
from ..common.config import *
MODULE_NAME = PARAMETER

class Parameter(ParameterApi):

    def __init__(self, metadata_client, data_source, name, value, minimum, maximum, mean, standard_deviation, data_type_id, parameter_type_id, unit_id, unit_prefix, flg_available, description='', data_groups_parameters_attributes=None):
        self.metadata_client = metadata_client
        self.id = None
        self.data_source = data_source
        self.name = name
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.data_type_id = data_type_id
        self.parameter_type_id = parameter_type_id
        self.unit_id = unit_id
        self.unit_prefix = unit_prefix
        self.flg_available = flg_available
        self.description = description
        self.data_groups_parameters_attributes = data_groups_parameters_attributes

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_parameter_api(self._Parameter__get_resource())
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        if res['success']:
            self.id = res['data']['id']
        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_parameter_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_parameter_api(self.id, self._Parameter__get_resource())
        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def create_multiple_from_dict(mdc_client, parameter_list):
        response = mdc_client.create_bulk_parameter_api(parameter_list)
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        return res

    @staticmethod
    def get_by_id(mdc_client, parameter_id):
        response = mdc_client.get_parameter_by_id_api(parameter_id)
        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_data_source_and_name(mdc_client, data_source, name):
        response = mdc_client.get_all_parameters_by_data_source_and_name_api(data_source, name)
        Base.cal_debug(MODULE_NAME, 'get_all_parameters_by_data_source_and_name_api', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def delete_by_id(mdc_client, parameter_id):
        resp = mdc_client.delete_parameter_api(parameter_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)
        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    def __get_resource(self):
        parameter = {MODULE_NAME: {'data_source':self.data_source, 
                       'name':self.name, 
                       'value':self.value, 
                       'minimum':self.minimum, 
                       'maximum':self.maximum, 
                       'mean':self.mean, 
                       'standard_deviation':self.standard_deviation, 
                       'data_type_id':self.data_type_id, 
                       'parameter_type_id':self.parameter_type_id, 
                       'unit_id':self.unit_id, 
                       'unit_prefix':self.unit_prefix, 
                       'flg_available':self.flg_available, 
                       'description':self.description, 
                       'data_groups_parameters_attributes':self.data_groups_parameters_attributes}}
        return parameter