# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/container_provider.py
# Compiled at: 2020-03-24 15:03:11
# Size of source mod 2**32: 2337 bytes
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service
from jinja2 import Template
import importlib.resources as pkg_resources
SCOPES = [
 'https://www.googleapis.com/auth/tagmanager.edit.containers',
 'https://www.googleapis.com/auth/tagmanager.delete.containers',
 'https://www.googleapis.com/auth/tagmanager.edit.containerversions']

class ContainerProvider(ResourceProvider):

    def create(self, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        account_path = f"accounts/{props['account_id']}"
        container = service.accounts().containers().create(parent=account_path,
          body={'name':props['container_name'], 
         'usage_context':['web']}).execute()
        container_public_id = container['publicId']
        with pkg_resources.open_text('pulumi_google_tag_manager.templates', 'gtm_tag.html') as (f):
            template = Template(f.read())
            gtm_tag = template.render(container_public_id=container_public_id)
        with pkg_resources.open_text('pulumi_google_tag_manager.templates', 'gtm_tag_noscript.html') as (f):
            template = Template(f.read())
            gtm_tag_noscript = template.render(container_public_id=container_public_id)
        return CreateResult(id_=(props['account_id']),
          outs={**{'container_id':container['containerId'], 
         'gtm_tag_noscript':gtm_tag_noscript, 
         'gtm_tag':gtm_tag}, **props, **container})

    def update(self, id, _olds, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        container = service.accounts().containers().update(path=(_olds['path']),
          body={'name':props['container_name'], 
         'usage_context':['web']}).execute()
        return UpdateResult(outs={**props, **container})

    def delete(self, id, props):
        service = get_service('tagmanager', 'v2', SCOPES, props['key_location'])
        service.accounts().containers().delete(path=(props['path'])).execute()