# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/proposal_api.py
# Compiled at: 2019-08-14 10:42:37
# Size of source mod 2**32: 1656 bytes
"""ProposalApi module class"""
import json
from common.base import Base

class ProposalApi(Base):

    def create_proposal_api(self, proposal):
        api_url = self._ProposalApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(proposal)))

    def delete_proposal_api(self, proposal_id):
        api_url = self._ProposalApi__get_api_url(proposal_id)
        return self.api_delete(api_url)

    def update_proposal_api(self, proposal_id, proposal):
        api_url = self._ProposalApi__get_api_url(proposal_id)
        return self.api_put(api_url, data=(json.dumps(proposal)))

    def get_proposal_by_id_api(self, proposal_id):
        api_url = self._ProposalApi__get_api_url(proposal_id)
        return self.api_get(api_url, params={})

    def get_proposal_by_number_api(self, number):
        api_url = self._ProposalApi__get_api_url('{0}{1}'.format('/by_number/', number))
        return self.api_get(api_url, params={})

    def get_runs_by_proposal_number_api(self, proposal_number, run_number=None):
        api_specifics = '{0}{1}{2}'.format('by_number/', proposal_number, '/runs')
        if run_number:
            api_specifics = '{0}/{1}'.format(api_specifics, run_number)
        api_url = self._ProposalApi__get_api_url(api_specifics)
        return self.api_get(api_url)

    def get_all_proposals_by_number_api(self, number):
        api_url = self._ProposalApi__get_api_url()
        return self.api_get(api_url, params={'number': number})

    def __get_api_url(self, api_specifics=''):
        model_name = 'proposals/'
        return self.get_api_url(model_name, api_specifics)