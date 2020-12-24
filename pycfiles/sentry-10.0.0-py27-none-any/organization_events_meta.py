# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_events_meta.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import OrganizationEventsEndpointBase, OrganizationEventsError, NoProjects
from sentry.utils.snuba import raw_query

class OrganizationEventsMetaEndpoint(OrganizationEventsEndpointBase):

    def get(self, request, organization):
        try:
            params = self.get_filter_params(request, organization)
            snuba_args = self.get_snuba_query_args(request, organization, params)
        except OrganizationEventsError as exc:
            return Response({'detail': exc.message}, status=400)
        except NoProjects:
            return Response({'count': 0})

        data = raw_query(aggregations=[
         [
          'count()', '', 'count']], referrer='api.organization-event-meta', **snuba_args)['data'][0]
        return Response({'count': data['count']})