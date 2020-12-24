# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_auth_providers.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.auth import manager
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationAuthProviderPermission
from sentry.api.serializers import serialize

class OrganizationAuthProvidersEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationAuthProviderPermission,)

    def get(self, request, organization):
        """
        List available auth providers that are available to use for an Organization
        ```````````````````````````````````````````````````````````````````````````

        :pparam string organization_slug: the organization short name
        :auth: required
        """
        provider_list = []
        for k, v in manager:
            provider_list.append({'key': k, 'name': v.name, 'requiredFeature': v.required_feature})

        return Response(serialize(provider_list, request.user))