# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_auth_provider_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import status
from rest_framework.response import Response
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationAuthProviderPermission
from sentry.api.serializers import serialize
from sentry.models import AuthProvider

class OrganizationAuthProviderDetailsEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationAuthProviderPermission,)

    def get(self, request, organization):
        """
        Retrieve details about Organization's SSO settings and
        currently installed auth_provider
        ``````````````````````````````````````````````````````

        :pparam string organization_slug: the organization short name
        :auth: required
        """
        try:
            auth_provider = AuthProvider.objects.get(organization=organization)
        except AuthProvider.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        auth_provider._organization_cache = organization
        return Response(serialize(auth_provider, request.user))