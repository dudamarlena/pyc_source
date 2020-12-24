# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_api_key_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import status
from rest_framework.response import Response
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationAdminPermission
from sentry.api.serializers import serialize
from sentry.models import ApiKey, AuditLogEntryEvent
DEFAULT_SCOPES = [
 'project:read', 'event:read', 'team:read', 'org:read', 'member:read']

class OrganizationApiKeyIndexEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationAdminPermission,)

    def get(self, request, organization):
        """
        List an Organization's API Keys
        ```````````````````````````````````

        :pparam string organization_slug: the organization short name
        :auth: required
        """
        queryset = sorted(ApiKey.objects.filter(organization=organization), key=lambda x: x.label)
        return Response(serialize(queryset, request.user))

    def post(self, request, organization):
        """
        Create an Organization API Key
        ```````````````````````````````````

        :pparam string organization_slug: the organization short name
        :auth: required
        """
        key = ApiKey.objects.create(organization=organization, scope_list=DEFAULT_SCOPES)
        self.create_audit_entry(request, organization=organization, target_object=key.id, event=AuditLogEntryEvent.APIKEY_ADD, data=key.get_audit_log_data())
        return Response(serialize(key, request.user), status=status.HTTP_201_CREATED)