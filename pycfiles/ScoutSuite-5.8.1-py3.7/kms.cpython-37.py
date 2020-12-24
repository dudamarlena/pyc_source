# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/facade/kms.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1321 bytes
from oci.key_management import KmsManagementClient, KmsVaultClient
from oci.pagination import list_call_get_all_results
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.providers.utils import run_concurrently

class KMSFacade:

    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._vault_client = KmsVaultClient(self._credentials.config)

    async def get_vaults(self):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._vault_client.list_vaults, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to get KMS vaults: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_keys(self, keyvault):
        try:
            key_client = KmsManagementClient(self._credentials.config, keyvault['management_endpoint'])
            response = await run_concurrently(lambda : list_call_get_all_results(key_client.list_keys, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to get KMS vaults: {}'.format(e))
                return []
            finally:
                e = None
                del e