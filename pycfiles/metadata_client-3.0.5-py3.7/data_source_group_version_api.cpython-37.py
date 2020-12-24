# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/data_source_group_version_api.py
# Compiled at: 2019-08-14 10:42:37
# Size of source mod 2**32: 818 bytes
"""DataSourceGroupVersionApi module class"""
import json
from common.base import Base

class DataSourceGroupVersionApi(Base):

    def get_data_source_group_version_api(self, data_source_group_id, version_name):
        api_url = self._DataSourceGroupVersionApi__get_api_url()
        return self.api_get(api_url,
          params={'data_source_group_id':data_source_group_id, 
         'name':version_name})

    def update_data_source_group_version_api(self, id, params):
        api_url = self._DataSourceGroupVersionApi__get_api_url(id)
        return self.api_put(api_url, data=(json.dumps(params)))

    def __get_api_url(self, api_specifics=''):
        model_name = 'data_source_group_versions/'
        return self.get_api_url(model_name, api_specifics)