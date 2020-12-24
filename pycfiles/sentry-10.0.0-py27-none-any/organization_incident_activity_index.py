# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_incident_activity_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.incident import IncidentPermission, IncidentEndpoint
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.incidents.logic import get_incident_activity

class OrganizationIncidentActivityIndexEndpoint(IncidentEndpoint):
    permission_classes = (
     IncidentPermission,)

    def get(self, request, organization, incident):
        if request.GET.get('desc', '1') == '1':
            order_by = '-date_added'
        else:
            order_by = 'date_added'
        return self.paginate(request=request, queryset=get_incident_activity(incident), order_by=order_by, paginator_cls=OffsetPaginator, on_results=lambda x: serialize(x, request.user))