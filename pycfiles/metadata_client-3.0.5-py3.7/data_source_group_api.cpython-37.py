# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/data_source_group_api.py
# Compiled at: 2019-08-08 05:58:56
# Size of source mod 2**32: 456 bytes
"""DataSourceGroupApi module class"""
import json
from common.base import Base

class DataSourceGroupApi(Base):

    def get_data_source_group_by_name_api(self, name):
        api_url = self._DataSourceGroupApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def __get_api_url(self, api_specifics=''):
        model_name = 'data_source_groups/'
        return self.get_api_url(model_name, api_specifics)