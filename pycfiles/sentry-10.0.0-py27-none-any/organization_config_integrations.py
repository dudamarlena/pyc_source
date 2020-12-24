# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_config_integrations.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import integrations
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.serializers import serialize, IntegrationProviderSerializer

class OrganizationConfigIntegrationsEndpoint(OrganizationEndpoint):

    def get(self, request, organization):
        providers = list(integrations.all())
        providers.sort(key=lambda i: i.key)
        serialized = serialize(providers, organization=organization, serializer=IntegrationProviderSerializer())
        return Response({'providers': serialized})