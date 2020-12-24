# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_analytics/dynamic_providers/web_property_provider.py
# Compiled at: 2020-03-24 13:31:56
# Size of source mod 2**32: 1874 bytes
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service
SCOPES = ['https://www.googleapis.com/auth/analytics.edit']

class WebPropertyProvider(ResourceProvider):

    def create(self, props):
        service = get_service('analytics', 'v3', SCOPES, props['key_location'])
        properties = service.management().webproperties().list(accountId=(props['account_id']),
          fields='items').execute()
        if properties.get('items'):
            for p in properties.get('items'):
                if props['site_name'] == p.get('name'):
                    return CreateResult(id_=(props['account_id']),
                      outs={**{'tracking_id': p['id']}, **props})

        web_property = service.management().webproperties().insert(accountId=(props['account_id']),
          fields='id',
          body={'websiteUrl':props['site_url'], 
         'name':props['site_name']}).execute()
        return CreateResult(id_=(props['account_id']),
          outs={**{'tracking_id': web_property['id']}, **props})

    def update(self, id, _olds, props):
        service = get_service('analytics', 'v3', SCOPES, props['key_location'])
        web_property = service.management().webproperties().update(accountId=(props['account_id']),
          webPropertyId=(_olds['tracking_id']),
          body={'websiteUrl':props['site_url'], 
         'name':props['site_url']}).execute()
        return UpdateResult(outs={**{'tracking_id': web_property['id']}, **props})