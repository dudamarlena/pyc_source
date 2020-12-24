# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/run_api.py
# Compiled at: 2017-06-28 20:05:41
# Size of source mod 2**32: 1670 bytes
"""RunApi module class"""
import json
from common.base import Base

class RunApi(Base):

    def create_run_api(self, run):
        api_url = self._RunApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(run)))

    def delete_run_api(self, run_id):
        api_url = self._RunApi__get_api_url(run_id)
        return self.api_delete(api_url)

    def update_run_api(self, run_id, run):
        api_url = self._RunApi__get_api_url(run_id)
        return self.api_put(api_url, data=(json.dumps(run)))

    def get_run_by_id_api(self, run_id):
        api_url = self._RunApi__get_api_url(run_id)
        return self.api_get(api_url, params={})

    def get_all_runs_by_run_number_api(self, run_number):
        api_url = self._RunApi__get_api_url()
        return self.api_get(api_url, params={'run_number': run_number})

    def get_run_by_run_number_and_experiment_id_api(self, run_number, experiment_id):
        api_url = self._RunApi__get_api_url()
        return self.api_get(api_url, params={'run_number':run_number,  'experiment_id':experiment_id})

    def get_run_all_raw_data_groups_ids_api(self, run_number, proposal_number):
        api_url = self._RunApi__get_api_url('all_raw_data_groups_ids')
        return self.api_get(api_url, params={'run_number':run_number, 
         'proposal_number':proposal_number})

    def __get_api_url(self, api_specifics=''):
        model_name = 'runs/'
        return self.get_api_url(model_name, api_specifics)