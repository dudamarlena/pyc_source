# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/custom_html_tag_provider.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 2134 bytes
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location
SCOPES = [
 'https://www.googleapis.com/auth/tagmanager.edit.containers',
 'https://www.googleapis.com/auth/tagmanager.delete.containers',
 'https://www.googleapis.com/auth/tagmanager.edit.containerversions']

class CustomHtmlTagProvider(ResourceProvider):

    def create(self, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        tag_body = self._get_tag_body(props)
        tag = service.accounts().containers().workspaces().tags().create(parent=(props['workspace_path']),
          body=tag_body).execute()
        return CreateResult(id_=(props['workspace_path']), outs={**props, **tag})

    def update(self, id, _olds, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        tag_body = self._get_tag_body(props)
        tag = service.accounts().containers().workspaces().tags().update(path=(_olds['path']),
          body=tag_body).execute()
        return UpdateResult(outs={**props, **tag})

    def delete(self, id, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        service.accounts().containers().workspaces().tags().delete(path=(props['path'])).execute()

    def _get_tag_body(self, props):
        params = [
         {'key':'html', 
          'type':'template', 
          'value':props['html']}]
        if props.get('supportDocumentWrite') is not None:
            params.append({'key':'supportDocumentWrite', 
             'type':'boolean', 
             'value':str(props['supportDocumentWrite']).lower()})
        tag_body = {'name':props['tag_name'], 
         'type':'html', 
         'parameter':params}
        return tag_body