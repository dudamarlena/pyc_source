# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/parameter_api.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 1658 bytes
"""ParameterApi module class"""
import json
from common.base import Base

class ParameterApi(Base):

    def create_parameter_api(self, parameter):
        api_url = self._ParameterApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(parameter)))

    def create_bulk_parameter_api(self, parameters_list):
        api_url = self._ParameterApi__get_api_url('bulk_create')
        return self.api_post(api_url, data=(json.dumps(parameters_list)))

    def delete_bulk_parameter_api_by_data_group_id(self, data_group_id):
        parameters_list = {'parameter': {'data_group_id': int(data_group_id)}}
        api_url = self._ParameterApi__get_api_url('bulk_delete')
        return self.api_post(api_url, data=(json.dumps(parameters_list)))

    def delete_parameter_api(self, parameter_id):
        api_url = self._ParameterApi__get_api_url(parameter_id)
        return self.api_delete(api_url)

    def update_parameter_api(self, parameter_id, parameter):
        api_url = self._ParameterApi__get_api_url(parameter_id)
        return self.api_put(api_url, data=(json.dumps(parameter)))

    def get_parameter_by_id_api(self, parameter_id):
        api_url = self._ParameterApi__get_api_url(parameter_id)
        return self.api_get(api_url, params={})

    def get_all_parameters_by_data_source_and_name_api(self, data_source, name):
        api_url = self._ParameterApi__get_api_url()
        return self.api_get(api_url, params={'data_source':data_source, 
         'name':name})

    def __get_api_url(self, api_specifics=''):
        model_name = 'parameters/'
        return self.get_api_url(model_name, api_specifics)