# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/data_type_api.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 1056 bytes
"""DataTypeApi module class"""
import json
from common.base import Base

class DataTypeApi(Base):

    def create_data_type_api(self, data_type):
        api_url = self._DataTypeApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(data_type)))

    def delete_data_type_api(self, data_type_id):
        api_url = self._DataTypeApi__get_api_url(data_type_id)
        return self.api_delete(api_url)

    def update_data_type_api(self, data_type_id, data_type):
        api_url = self._DataTypeApi__get_api_url(data_type_id)
        return self.api_put(api_url, data=(json.dumps(data_type)))

    def get_data_type_by_id_api(self, data_type_id):
        api_url = self._DataTypeApi__get_api_url(data_type_id)
        return self.api_get(api_url, params={})

    def get_all_data_types_by_name_api(self, name):
        api_url = self._DataTypeApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def __get_api_url(self, api_specifics=''):
        model_name = 'data_types/'
        return self.get_api_url(model_name, api_specifics)