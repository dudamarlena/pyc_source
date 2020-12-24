# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/parameter_api.py
# Compiled at: 2019-08-12 09:02:46
# Size of source mod 2**32: 1058 bytes
__doc__ = 'ParameterApi module class'
import json
from ..common.base import Base

class ParameterApi(Base):

    def create_parameter_api(self, parameter):
        api_url = self._ParameterApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(parameter)))

    def delete_parameter_api(self, parameter_id):
        api_url = self._ParameterApi__get_api_url(parameter_id)
        return self.api_delete(api_url)

    def update_parameter_api(self, parameter_id, parameter):
        api_url = self._ParameterApi__get_api_url(parameter_id)
        return self.api_put(api_url, data=(json.dumps(parameter)))

    def get_parameter_by_id_api(self, parameter_id):
        api_url = self._ParameterApi__get_api_url(parameter_id)
        return self.api_get(api_url, params={})

    def get_all_parameters_by_name_api(self, name):
        api_url = self._ParameterApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def __get_api_url(self, api_specifics=''):
        model_name = 'parameters/'
        return self.get_api_url(model_name, api_specifics)