# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_environments.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import OrganizationEndpoint
from sentry.api.helpers.environments import environment_visibility_filter_options
from sentry.api.serializers import serialize
from sentry.models import Environment, EnvironmentProject

class OrganizationEnvironmentsEndpoint(OrganizationEndpoint):

    def get(self, request, organization):
        visibility = request.GET.get('visibility', 'visible')
        if visibility not in environment_visibility_filter_options:
            return Response({'detail': ("Invalid value for 'visibility', valid values are: {!r}").format(environment_visibility_filter_options.keys())}, status=400)
        environment_projects = EnvironmentProject.objects.filter(project__in=self.get_projects(request, organization))
        add_visibility_filters = environment_visibility_filter_options[visibility]
        environment_projects = add_visibility_filters(environment_projects).values('environment')
        queryset = Environment.objects.filter(id__in=environment_projects).exclude(name='').order_by('name')
        return Response(serialize(list(queryset), request.user))