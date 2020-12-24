# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_tags.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import OrganizationEventsEndpointBase, OrganizationEventsError, NoProjects
from sentry.api.serializers import serialize
from sentry.tagstore.snuba.backend import SnubaTagStorage

class OrganizationTagsEndpoint(OrganizationEventsEndpointBase):

    def get(self, request, organization):
        try:
            filter_params = self.get_filter_params(request, organization)
        except OrganizationEventsError as exc:
            return Response({'detail': exc.message}, status=400)
        except NoProjects:
            return Response([])

        tagstore = SnubaTagStorage()
        results = tagstore.get_tag_keys_for_projects(filter_params['project_id'], filter_params.get('environment'), filter_params['start'], filter_params['end'])
        return Response(serialize(results, request.user))