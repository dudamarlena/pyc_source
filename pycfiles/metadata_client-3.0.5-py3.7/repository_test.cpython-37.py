# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/modules/repository_test.py
# Compiled at: 2019-08-14 10:42:37
# Size of source mod 2**32: 6372 bytes
"""RepositoryTest class"""
import unittest
from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
from modules.repository import Repository
MODULE_NAME = REPOSITORY

class RepositoryTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.mdc_client = MetadataClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
          base_api_url=BASE_API_URL)
        _RepositoryTest__unique_name1 = Generators.generate_unique_name('Repository01')
        _RepositoryTest__unique_identifier1 = Generators.generate_unique_identifier()
        self.repo_1 = {'name':_RepositoryTest__unique_name1, 
         'identifier':_RepositoryTest__unique_identifier1, 
         'mount_point':_RepositoryTest__unique_identifier1, 
         'transfer_agent_identifier':'new_special_repo_identifier', 
         'transfer_agent_server_url':'new_repo_address:new_repo_port', 
         'flg_context':'L', 
         'flg_available':'true', 
         'description':'desc 01'}
        _RepositoryTest__unique_name_upd = Generators.generate_unique_name('RepositoryUpd1')
        _RepositoryTest__unique_identifier_upd = Generators.generate_unique_identifier(1)
        self.repo_01_upd = {'name':_RepositoryTest__unique_name_upd, 
         'identifier':_RepositoryTest__unique_identifier_upd, 
         'mount_point':_RepositoryTest__unique_identifier_upd, 
         'transfer_agent_identifier':'updated_special_repo_identifier', 
         'transfer_agent_server_url':'updated_repo_address:update_repo_port', 
         'flg_context':'L', 
         'flg_available':'false', 
         'description':'desc 01 Updated!'}

    def test_create_repository(self):
        repo_01 = Repository(metadata_client=(self.mdc_client),
          name=(self.repo_1['name']),
          identifier=(self.repo_1['identifier']),
          mount_point=(self.repo_1['mount_point']),
          transfer_agent_identifier=(self.repo_1['transfer_agent_identifier']),
          transfer_agent_server_url=(self.repo_1['transfer_agent_server_url']),
          flg_context=(self.repo_1['flg_context']),
          flg_available=(self.repo_1['flg_available']),
          description=(self.repo_1['description']))
        result1 = repo_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.repo_1)
        repository = result1['data']
        repository_id = result1['data']['id']
        repository_name = result1['data']['name']
        repo_01_dup = repo_01
        result2 = repo_01_dup.create()
        expect_app_info = {'name': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)
        result3 = Repository.get_by_name(self.mdc_client, repository_name)
        self.assert_find_success(MODULE_NAME, result3, self.repo_1)
        result4 = Repository.get_by_id(self.mdc_client, repository_id)
        self.assert_find_success(MODULE_NAME, result4, self.repo_1)
        result5 = Repository.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)
        repo_01.name = self.repo_01_upd['name']
        repo_01.identifier = self.repo_01_upd['identifier']
        repo_01.mount_point = self.repo_01_upd['mount_point']
        repo_01.transfer_agent_identifier = self.repo_01_upd['transfer_agent_identifier']
        repo_01.transfer_agent_server_url = self.repo_01_upd['transfer_agent_server_url']
        repo_01.flg_context = self.repo_01_upd['flg_context']
        repo_01.flg_available = self.repo_01_upd['flg_available']
        repo_01.description = self.repo_01_upd['description']
        result6 = repo_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.repo_01_upd)
        repo_01.name = '#############################################################'
        repo_01.flg_context = self.repo_01_upd['flg_context']
        repo_01.flg_available = self.repo_01_upd['flg_available']
        repo_01.description = self.repo_01_upd['description']
        result7 = repo_01.update()
        expect_app_info = {'name': ['is too long (maximum is 60 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)
        result8 = repo_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)
        result9 = repo_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'mount_point', STRING)
        self.assert_eq_hfield(receive, expect, 'transfer_agent_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'transfer_agent_server_url', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_context', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)


if __name__ == '__main__':
    unittest.main()