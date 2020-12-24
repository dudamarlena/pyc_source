# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/facade/identity.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2800 bytes
from oci.identity import IdentityClient
from oci.pagination import list_call_get_all_results
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently

class IdentityFacade:

    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._client = IdentityClient(self._credentials.config)

    async def get_users(self):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.list_users, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to retrieve users: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_user_api_keys(self, user_id):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.list_api_keys, user_id))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to retrieve user api keys: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_groups(self):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.list_groups, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to retrieve groups: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_group_users(self, group_id):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results((self._client.list_user_group_memberships), (self._credentials.get_scope()),
              group_id=group_id))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to retrieve group users: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_policies(self):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.list_policies, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to retrieve policies: {}'.format(e))
                return
            finally:
                e = None
                del e

    async def get_authentication_policy(self):
        try:
            response = await run_concurrently(lambda : self._client.get_authentication_policy(self._credentials.config['tenancy']))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to retrieve authentication policy: {}'.format(e))
                return []
            finally:
                e = None
                del e