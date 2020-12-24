# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/sample_api.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 1266 bytes
"""SampleApi module class"""
import json
from common.base import Base

class SampleApi(Base):

    def create_sample_api(self, sample):
        api_url = self._SampleApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(sample)))

    def delete_sample_api(self, sample_id):
        api_url = self._SampleApi__get_api_url(sample_id)
        return self.api_delete(api_url)

    def update_sample_api(self, sample_id, sample):
        api_url = self._SampleApi__get_api_url(sample_id)
        return self.api_put(api_url, data=(json.dumps(sample)))

    def get_sample_by_id_api(self, sample_id):
        api_url = self._SampleApi__get_api_url(sample_id)
        return self.api_get(api_url, params={})

    def get_all_samples_by_proposal_id_api(self, proposal_id):
        api_url = self._SampleApi__get_api_url()
        return self.api_get(api_url, params={'proposal_id': proposal_id})

    def get_all_samples_by_name_and_proposal_id_api(self, name, proposal_id):
        api_url = self._SampleApi__get_api_url()
        return self.api_get(api_url, params={'name':name, 
         'proposal_id':proposal_id})

    def __get_api_url(self, api_specifics=''):
        model_name = 'samples/'
        return self.get_api_url(model_name, api_specifics)