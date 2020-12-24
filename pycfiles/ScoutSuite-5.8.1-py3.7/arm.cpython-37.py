# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/facade/arm.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1193 bytes
from azure.mgmt.authorization import AuthorizationManagementClient
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently

class ARMFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return AuthorizationManagementClient((self.credentials.arm_credentials), subscription_id=subscription_id)

    async def get_roles(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = '/subscriptions/{}'.format(subscription_id)
            return await run_concurrently(lambda : list(client.role_definitions.list(scope=scope)))
        except Exception as e:
            try:
                print_exception('Failed to retrieve roles: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_role_assignments(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.role_assignments.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve role assignments: {}'.format(e))
                return []
            finally:
                e = None
                del e