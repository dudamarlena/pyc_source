# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/tag_provider.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 2047 bytes
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location
SCOPES = [
 'https://www.googleapis.com/auth/tagmanager.edit.containers',
 'https://www.googleapis.com/auth/tagmanager.delete.containers',
 'https://www.googleapis.com/auth/tagmanager.edit.containerversions']

class TagProvider(ResourceProvider):

    def create(self, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        tag_body = {'name':props['tag_name'], 
         'type':'ua', 
         'parameter':[
          {'key':'trackingId', 
           'type':'template', 
           'value':str(props['tracking_id'])}]}
        tag = service.accounts().containers().workspaces().tags().create(parent=(props['workspace_path']),
          body=tag_body).execute()
        return CreateResult(id_=(props['workspace_path']), outs={**props, **tag})

    def update(self, id, _olds, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        tag_body = {'name':props['tag_name'], 
         'type':'ua', 
         'parameter':[
          {'key':'trackingId', 
           'type':'template', 
           'value':str(props['tracking_id'])}]}
        tag = service.accounts().containers().workspaces().tags().update(path=(_olds['path']),
          body=tag_body).execute()
        return UpdateResult(outs={**props, **tag})

    def delete(self, id, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        service.accounts().containers().workspaces().tags().delete(path=(props['path'])).execute()