# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/shared_group_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from rest_framework.response import Response
from sentry.api.base import Endpoint, EnvironmentMixin
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize, SharedEventSerializer, SharedGroupSerializer, SharedProjectSerializer
from sentry.models import Group

class SharedGroupDetailsEndpoint(Endpoint, EnvironmentMixin):
    permission_classes = ()

    def get(self, request, share_id):
        """
        Retrieve an aggregate

        Return details on an individual aggregate specified by it's shared ID.

            {method} {path}

        Note: This is not the equivilant of what you'd receive with the standard
        group details endpoint. Data is more restrictive and designed
        specifically for sharing.

        """
        try:
            group = Group.from_share_id(share_id)
        except Group.DoesNotExist:
            raise ResourceDoesNotExist

        if group.organization.flags.disable_shared_issues:
            raise ResourceDoesNotExist
        event = group.get_latest_event()
        context = serialize(group, request.user, SharedGroupSerializer(environment_func=self._get_environment_func(request, group.project.organization_id)))
        context['latestEvent'] = serialize(event, request.user, SharedEventSerializer())
        context['project'] = serialize(group.project, request.user, SharedProjectSerializer())
        return Response(context)