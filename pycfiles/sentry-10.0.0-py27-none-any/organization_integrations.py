# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_integrations.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationIntegrationsPermission
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.models import ObjectStatus, OrganizationIntegration

class OrganizationIntegrationsEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationIntegrationsPermission,)

    def get(self, request, organization):
        integrations = OrganizationIntegration.objects.filter(organization=organization, status=ObjectStatus.VISIBLE)
        if 'provider_key' in request.GET:
            integrations = integrations.filter(integration__provider=request.GET['provider_key'])
        return self.paginate(queryset=integrations, request=request, order_by='integration__name', on_results=lambda x: serialize(x, request.user), paginator_cls=OffsetPaginator)