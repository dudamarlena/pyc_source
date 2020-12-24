# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/facade/storageaccounts.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2957 bytes
import datetime
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.storage import StorageManagementClient
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently

class StorageAccountsFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return StorageManagementClient((self.credentials.arm_credentials), subscription_id=subscription_id)

    async def get_storage_accounts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            storage_accounts = await run_concurrently(lambda : list(client.storage_accounts.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve storage accounts: {}'.format(e))
                return []
            finally:
                e = None
                del e

        else:
            await get_and_set_concurrently([self._get_and_set_activity_logs], storage_accounts, subscription_id=subscription_id)
            return storage_accounts

    async def get_blob_containers(self, resource_group_name, storage_account_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            containers = await run_concurrently(lambda : list(client.blob_containers.list(resource_group_name, storage_account_name)))
        except Exception as e:
            try:
                print_exception('Failed to retrieve blob containers: {}'.format(e))
                return []
            finally:
                e = None
                del e

        else:
            return containers

    async def _get_and_set_activity_logs(self, storage_account, subscription_id: str):
        client = MonitorManagementClient(self.credentials.arm_credentials, subscription_id)
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        utc_now = datetime.datetime.utcnow()
        timespan = datetime.timedelta(90)
        logs_filter = ' and '.join([
         'eventTimestamp ge {}'.format((utc_now - timespan).strftime(time_format)),
         'eventTimestamp le {}'.format(utc_now.strftime(time_format)),
         'resourceId eq {}'.format(storage_account.id)])
        try:
            activity_logs = await run_concurrently(lambda : list(client.activity_logs.list(filter=logs_filter, select='eventTimestamp, operationName')))
        except Exception as e:
            try:
                print_exception('Failed to retrieve activity logs: {}'.format(e))
                setattr(storage_account, 'activity_logs', [])
            finally:
                e = None
                del e

        else:
            setattr(storage_account, 'activity_logs', activity_logs)