# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/facade/cloudresourcemanager.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 840 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.gcp.facade.basefacade import GCPBaseFacade
from ScoutSuite.providers.utils import run_concurrently

class CloudResourceManagerFacade(GCPBaseFacade):

    def __init__(self):
        super(CloudResourceManagerFacade, self).__init__('cloudresourcemanager', 'v1')

    async def get_bindings(self, project_id: str):
        try:
            cloudresourcemanager_client = self._get_client()
            response = await run_concurrently(lambda : cloudresourcemanager_client.projects().getIamPolicy(resource=project_id).execute())
            return response.get('bindings', [])
        except Exception as e:
            try:
                print_exception('Failed to retrieve project IAM policy bindings: {}'.format(e))
                return []
            finally:
                e = None
                del e