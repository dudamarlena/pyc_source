# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/workspace_provider.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 1478 bytes
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location
SCOPES = [
 'https://www.googleapis.com/auth/tagmanager.edit.containers',
 'https://www.googleapis.com/auth/tagmanager.delete.containers',
 'https://www.googleapis.com/auth/tagmanager.edit.containerversions']

class WorkspaceProvider(ResourceProvider):

    def create(self, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        workspace = service.accounts().containers().workspaces().create(parent=(props['container_path']),
          body={'name': props['workspace_name']}).execute()
        return CreateResult(id_=(props['container_path']), outs={**props, **workspace})

    def update(self, id, _olds, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        workspace = service.accounts().containers().workspaces().update(path=(_olds['path']),
          body={'name': props['workspace_name']}).execute()
        return UpdateResult(outs={**props, **workspace})

    def delete(self, id, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        service.accounts().containers().workspaces().delete(path=(props['path'])).execute()