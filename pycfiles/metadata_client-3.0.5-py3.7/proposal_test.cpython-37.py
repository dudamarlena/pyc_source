# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/modules/proposal_test.py
# Compiled at: 2020-02-20 06:10:10
# Size of source mod 2**32: 12139 bytes
"""ProposalTest class"""
import unittest
from datetime import datetime, timedelta, timezone
from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
import common.util_datetime as util_dt
from modules.proposal import Proposal
MODULE_NAME = PROPOSAL

class ProposalTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.mdc_client = MetadataClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
          base_api_url=BASE_API_URL)
        _ProposalTest__utc = timezone(timedelta())
        _ProposalTest__now = datetime.now()
        _ProposalTest__end_at = datetime((_ProposalTest__now.year), (_ProposalTest__now.month), (_ProposalTest__now.day), (_ProposalTest__now.hour), (_ProposalTest__now.minute),
          (_ProposalTest__now.second), (_ProposalTest__now.microsecond), tzinfo=_ProposalTest__utc)
        _ProposalTest__yesterday = _ProposalTest__now - timedelta(1)
        _ProposalTest__begin_at = datetime((_ProposalTest__yesterday.year), (_ProposalTest__yesterday.month), (_ProposalTest__yesterday.day),
          (_ProposalTest__yesterday.hour), (_ProposalTest__yesterday.minute),
          (_ProposalTest__yesterday.second), (_ProposalTest__yesterday.microsecond),
          tzinfo=_ProposalTest__utc)
        _ProposalTest__tomorrow = _ProposalTest__now + timedelta(1)
        _ProposalTest__release_at = datetime((_ProposalTest__tomorrow.year), (_ProposalTest__tomorrow.month), (_ProposalTest__tomorrow.day),
          (_ProposalTest__tomorrow.hour), (_ProposalTest__tomorrow.minute),
          (_ProposalTest__tomorrow.second), (_ProposalTest__tomorrow.microsecond),
          tzinfo=_ProposalTest__utc)
        _ProposalTest__unique_proposal_id1 = Generators.generate_unique_id(min_value=2017, max_value=799999)
        self.prop_1 = {'number':_ProposalTest__unique_proposal_id1, 
         'title':_ProposalTest__unique_proposal_id1, 
         'abstract':'', 
         'url':'https://in.xfel.eu/upex/proposal/{0}'.format(_ProposalTest__unique_proposal_id1), 
         'instrument_id':'1', 
         'instrument_cycle_id':'-1', 
         'principal_investigator_id':'1', 
         'main_proposer_id':'1', 
         'begin_at':util_dt.datetime_to_local_tz_str(_ProposalTest__begin_at), 
         'end_at':util_dt.datetime_to_local_tz_str(_ProposalTest__end_at), 
         'release_at':util_dt.datetime_to_local_tz_str(_ProposalTest__release_at), 
         'flg_beamtime_status':'T', 
         'beamtime_start_at':util_dt.datetime_to_local_tz_str(_ProposalTest__begin_at + timedelta(1)), 
         'beamtime_end_at':util_dt.datetime_to_local_tz_str(_ProposalTest__end_at + timedelta(2)), 
         'flg_proposal_system':'U', 
         'flg_available':'true', 
         'description':'desc 01'}
        _ProposalTest__end_at_upd = _ProposalTest__end_at + timedelta(1)
        _ProposalTest__release_at_upd = _ProposalTest__release_at + timedelta(1)
        self.prop1_upd = {'number':_ProposalTest__unique_proposal_id1, 
         'title':_ProposalTest__unique_proposal_id1, 
         'abstract':'', 
         'url':'https://in.xfel.eu/upex/proposal/{0}_2'.format(_ProposalTest__unique_proposal_id1), 
         'instrument_id':'2', 
         'instrument_cycle_id':'-1', 
         'principal_investigator_id':'1', 
         'main_proposer_id':'1', 
         'begin_at':util_dt.datetime_to_local_tz_str(_ProposalTest__begin_at), 
         'end_at':util_dt.datetime_to_local_tz_str(_ProposalTest__end_at_upd), 
         'release_at':util_dt.datetime_to_local_tz_str(_ProposalTest__release_at_upd), 
         'flg_beamtime_status':'T', 
         'beamtime_start_at':util_dt.datetime_to_local_tz_str(_ProposalTest__begin_at + timedelta(-1)), 
         'beamtime_end_at':util_dt.datetime_to_local_tz_str(_ProposalTest__end_at_upd + timedelta(1)), 
         'flg_proposal_system':'U', 
         'flg_available':'false', 
         'description':'desc 01 updated!!!'}

    def test_create_proposal(self):
        proposal_01 = Proposal(metadata_client=(self.mdc_client),
          number=(self.prop_1['number']),
          title=(self.prop_1['title']),
          abstract=(self.prop_1['abstract']),
          url=(self.prop_1['url']),
          instrument_id=(self.prop_1['instrument_id']),
          instrument_cycle_id=(self.prop_1['instrument_cycle_id']),
          principal_investigator_id=(self.prop_1['principal_investigator_id']),
          main_proposer_id=(self.prop_1['main_proposer_id']),
          begin_at=(self.prop_1['begin_at']),
          end_at=(self.prop_1['end_at']),
          release_at=(self.prop_1['release_at']),
          flg_beamtime_status=(self.prop_1['flg_beamtime_status']),
          beamtime_start_at=(self.prop_1['beamtime_start_at']),
          beamtime_end_at=(self.prop_1['beamtime_end_at']),
          flg_proposal_system=(self.prop_1['flg_proposal_system']),
          flg_available=(self.prop_1['flg_available']),
          description=(self.prop_1['description']))
        result1 = proposal_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.prop_1)
        proposal = result1['data']
        proposal_id = result1['data']['id']
        number = result1['data']['number']
        self.assertEqual(int(result1['data']['proposal_folder'][1:]), number)
        proposal_01_dup = proposal_01
        result2 = proposal_01_dup.create()
        expect_app_info = {'number':['has already been taken'],  'url':[
          'has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)
        result3 = Proposal.get_by_number(self.mdc_client, number)
        self.assert_find_success(MODULE_NAME, result3, self.prop_1)
        non_existing_number = 12345
        expected_return = 'Proposal number 12345 not found'
        result31 = Proposal.get_by_number(self.mdc_client, non_existing_number)
        self.assert_find_error(MODULE_NAME, result31, expected_return)
        result4 = Proposal.get_by_id(self.mdc_client, proposal_id)
        self.assert_find_success(MODULE_NAME, result4, self.prop_1)
        result5 = Proposal.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)
        proposal_01.number = self.prop1_upd['number']
        proposal_01.title = self.prop1_upd['title']
        proposal_01.abstract = self.prop1_upd['abstract']
        proposal_01.url = self.prop1_upd['url']
        proposal_01.instrument_id = self.prop1_upd['instrument_id']
        proposal_01.instrument_cycle_id = self.prop1_upd['instrument_cycle_id']
        proposal_01.principal_investigator_id = self.prop1_upd['principal_investigator_id']
        proposal_01.main_proposer_id = self.prop1_upd['main_proposer_id']
        proposal_01.begin_at = self.prop1_upd['begin_at']
        proposal_01.end_at = self.prop1_upd['end_at']
        proposal_01.release_at = self.prop1_upd['release_at']
        proposal_01.flg_beamtime_status = self.prop1_upd['flg_beamtime_status']
        proposal_01.beamtime_start_at = self.prop1_upd['beamtime_start_at']
        proposal_01.beamtime_end_at = self.prop1_upd['beamtime_end_at']
        proposal_01.flg_proposal_system = self.prop1_upd['flg_proposal_system']
        proposal_01.flg_available = self.prop1_upd['flg_available']
        proposal_01.description = self.prop1_upd['description']
        result6 = proposal_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.prop1_upd)
        proposal_01.number = 1234567
        proposal_01.flg_available = self.prop1_upd['flg_available']
        proposal_01.description = self.prop1_upd['description']
        result7 = proposal_01.update()
        expect_app_info = {'number': ['cannot be updated',
                    'must be less than or equal to 799999']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)
        result8 = proposal_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)
        result9 = proposal_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_proposal_from_dict(self):
        result1 = Proposal.create_from_dict(self.mdc_client, self.prop_1)
        self.assert_create_success(MODULE_NAME, result1, self.prop_1)
        proposal = result1['data']
        proposal_id = proposal['id']
        result2 = Proposal.create_from_dict(self.mdc_client, self.prop_1)
        expect_app_info = {'number':['has already been taken'],  'url':[
          'has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)
        result8 = Proposal.delete_by_id(self.mdc_client, proposal_id)
        self.assert_delete_success(MODULE_NAME, result8)
        result9 = Proposal.delete_by_id(self.mdc_client, proposal_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

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
        self.assert_eq_hfield(receive, expect, 'flg_proposal_system', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        expect['proposal_folder'] = 'p{0:06d}'.format(expect['number'])
        self.assert_eq_hfield(receive, expect, 'proposal_folder', STRING)


if __name__ == '__main__':
    unittest.main()