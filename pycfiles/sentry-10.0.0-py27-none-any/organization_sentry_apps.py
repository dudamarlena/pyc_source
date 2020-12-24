# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_sentry_apps.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases import OrganizationEndpoint, add_integration_platform_metric_tag
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.models import SentryApp

class OrganizationSentryAppsEndpoint(OrganizationEndpoint):

    @add_integration_platform_metric_tag
    def get(self, request, organization):
        queryset = SentryApp.objects.filter(owner=organization)
        return self.paginate(request=request, queryset=queryset, order_by='-date_added', paginator_cls=OffsetPaginator, on_results=lambda x: serialize(x, request.user))