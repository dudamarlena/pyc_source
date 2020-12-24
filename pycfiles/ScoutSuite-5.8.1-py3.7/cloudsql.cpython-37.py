# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/facade/cloudsql.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1824 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.gcp.facade.utils import GCPFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class CloudSQLFacade(GCPBaseFacade):

    def __init__(self):
        super(CloudSQLFacade, self).__init__('sqladmin', 'v1beta4')

    async def get_backups(self, project_id: str, instance_name: str):
        try:
            cloudsql_client = self._get_client()
            backups_group = cloudsql_client.backupRuns()
            request = backups_group.list(project=project_id, instance=instance_name)
            return await GCPFacadeUtils.get_all('items', request, backups_group)
        except Exception as e:
            try:
                print_exception('Failed to retrieve database instance backups: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_database_instances(self, project_id: str):
        try:
            cloudsql_client = self._get_client()
            instances_group = cloudsql_client.instances()
            request = instances_group.list(project=project_id)
            return await GCPFacadeUtils.get_all('items', request, instances_group)
        except Exception as e:
            try:
                print_exception('Failed to retrieve database instances: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_users(self, project_id: str, instance_name: str):
        try:
            cloudsql_client = self._get_client()
            response = await run_concurrently(lambda : cloudsql_client.users().list(project=project_id, instance=instance_name).execute())
            return response.get('items', [])
        except Exception as e:
            try:
                print_exception('Failed to retrieve database instance users: {}'.format(e))
                return []
            finally:
                e = None
                del e