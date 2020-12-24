# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_config_repositories.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.plugins import bindings

class OrganizationConfigRepositoriesEndpoint(OrganizationEndpoint):

    def get(self, request, organization):
        provider_bindings = bindings.get('repository.provider')
        providers = []
        for provider_id in provider_bindings:
            provider = provider_bindings.get(provider_id)(id=provider_id)
            if provider_id == 'github_apps':
                continue
            providers.append({'id': provider_id, 'name': provider.name, 'config': provider.get_config()})

        return Response({'providers': providers})