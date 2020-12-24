# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/proposal_api_test.py
# Compiled at: 2020-02-20 06:10:10
# Size of source mod 2**32: 10767 bytes
"""ProposalApiTest class"""
import unittest
from datetime import date, datetime, timedelta, timezone
from .api_base import ApiBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
import common.util_datetime as util_dt
from ...metadata_client_api import MetadataClientApi

class ProposalApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)
    _ProposalApiTest__utc = timezone(timedelta())
    _ProposalApiTest__now = datetime.now()
    end_at = datetime((_ProposalApiTest__now.year), (_ProposalApiTest__now.month), (_ProposalApiTest__now.day), (_ProposalApiTest__now.hour),
      (_ProposalApiTest__now.minute), (_ProposalApiTest__now.second), (_ProposalApiTest__now.microsecond),
      tzinfo=_ProposalApiTest__utc)
    _ProposalApiTest__yesterday = _ProposalApiTest__now - timedelta(1)
    begin_at = datetime((_ProposalApiTest__yesterday.year), (_ProposalApiTest__yesterday.month), (_ProposalApiTest__yesterday.day), (_ProposalApiTest__yesterday.hour),
      (_ProposalApiTest__yesterday.minute), (_ProposalApiTest__yesterday.second),
      (_ProposalApiTest__yesterday.microsecond), tzinfo=_ProposalApiTest__utc)
    _ProposalApiTest__tomorrow = _ProposalApiTest__now + timedelta(1)
    release_at = datetime((_ProposalApiTest__tomorrow.year), (_ProposalApiTest__tomorrow.month), (_ProposalApiTest__tomorrow.day), (_ProposalApiTest__tomorrow.hour),
      (_ProposalApiTest__tomorrow.minute), (_ProposalApiTest__tomorrow.second),
      (_ProposalApiTest__tomorrow.microsecond), tzinfo=_ProposalApiTest__utc)

    def test_create_proposal_api(self):
        _ProposalApiTest__unique_id = Generators.generate_unique_id(min_value=2017, max_value=799999)
        proposal = {PROPOSAL: {'number':_ProposalApiTest__unique_id, 
                    'title':'this is the title', 
                    'abstract':'this is the abstract', 
                    'url':'https://in.xfel.eu/upex/proposal/{0}'.format(_ProposalApiTest__unique_id), 
                    'instrument_id':'1', 
                    'instrument_cycle_id':'-1', 
                    'principal_investigator_id':'-1', 
                    'main_proposer_id':'-1', 
                    'begin_at':util_dt.datetime_to_local_tz_str(self.begin_at), 
                    'end_at':util_dt.datetime_to_local_tz_str(self.end_at), 
                    'release_at':util_dt.datetime_to_local_tz_str(self.release_at), 
                    'flg_beamtime_status':'N', 
                    'beamtime_start_at':util_dt.datetime_to_local_tz_str(self.begin_at + timedelta(1)), 
                    'beamtime_end_at':util_dt.datetime_to_local_tz_str(self.end_at + timedelta(2)), 
                    'flg_proposal_system':'U', 
                    'flg_available':'true', 
                    'description':'desc 01'}}
        expect = proposal[PROPOSAL]
        received = self._ProposalApiTest__create_entry_api(proposal, expect)
        proposal_id = received['id']
        prop_number = received['number']
        self._ProposalApiTest__create_error_entry_uk_api(proposal)
        self._ProposalApiTest__get_all_entries_by_number_api(prop_number, expect)
        self._ProposalApiTest__get_entry_by_id_api(proposal_id, expect)
        self._ProposalApiTest__update_entry_api(proposal_id, prop_number, expect)
        self._ProposalApiTest__delete_entry_by_id_api(proposal_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'number', NUMBER)
        self.assert_eq_hfield(receive, expect, 'title', STRING)
        self.assert_eq_hfield(receive, expect, 'abstract', STRING)
        self.assert_eq_hfield(receive, expect, 'url', STRING)
        self.assert_eq_hfield(receive, expect, 'instrument_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'instrument_cycle_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'principal_investigator_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'main_proposer_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'begin_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'end_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'release_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'flg_beamtime_status', STRING)
        self.assert_eq_hfield(receive, expect, 'beamtime_start_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'beamtime_end_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'flg_proposal_system', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        expect['proposal_folder'] = 'p{0:06d}'.format(expect['number'])
        self.assert_eq_hfield(receive, expect, 'proposal_folder', STRING)

    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_proposal_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_proposal_api(entry_info)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {'info': {'def_proposal_path':['has already been taken'],  'number':[
                   'has already been taken'], 
                  'proposal_folder':[
                   'has already been taken'], 
                  'url':[
                   'has already been taken']}}
        self.assertEqual(receive, expect, 'Expected result not received')
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)
        receive_msg = receive['info']['number'][0]
        expect_msg = expect['info']['number'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, prop_number, expect):
        _ProposalApiTest__end_at_upd = self.end_at + timedelta(1)
        _ProposalApiTest__release_at_upd = self.release_at + timedelta(1)
        proposal_upd = {PROPOSAL: {'number':prop_number, 
                    'title':'this is the title', 
                    'abstract':'this is the updated abstract!', 
                    'url':'https://in.xfel.eu/upex/proposal/102xxxxxxxx', 
                    'instrument_id':'2', 
                    'instrument_cycle_id':'-1', 
                    'principal_investigator_id':'-1', 
                    'main_proposer_id':'-1', 
                    'begin_at':util_dt.datetime_to_local_tz_str(self.begin_at), 
                    'end_at':util_dt.datetime_to_local_tz_str(_ProposalApiTest__end_at_upd), 
                    'release_at':util_dt.datetime_to_local_tz_str(_ProposalApiTest__release_at_upd), 
                    'flg_beamtime_status':'T', 
                    'beamtime_start_at':util_dt.datetime_to_local_tz_str(self.begin_at + timedelta(-1)), 
                    'beamtime_end_at':util_dt.datetime_to_local_tz_str(self.end_at + timedelta(1)), 
                    'flg_proposal_system':'U', 
                    'flg_available':'false', 
                    'description':'desc 01 updated!!!'}}
        res = self.client_api.update_proposal_api(entry_id, proposal_upd)
        receive = self.load_response_content(res)
        expect_upd = proposal_upd[PROPOSAL]
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(res.status_code, OK)
        field = 'number'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'title'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'begin_at'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'flg_proposal_system'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'url'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'abstract'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'instrument_id'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'instrument_cycle_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'principal_investigator_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'main_proposer_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'end_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'release_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_beamtime_status'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'beamtime_start_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'beamtime_end_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_number_api(self, number, expect):
        response = self.client_api.get_all_proposals_by_number_api(number)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_proposal_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_proposal_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()