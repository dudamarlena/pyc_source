# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_environments.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import DocSection
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.helpers.environments import environment_visibility_filter_options
from sentry.api.serializers import serialize
from sentry.models import EnvironmentProject
from sentry.utils.apidocs import scenario, attach_scenarios

@scenario('ListEnvironmentsForProject')
def list_project_environments_scenario(runner):
    runner.request(method='GET', path='/projects/%s/%s/environments/' % (runner.org.slug, runner.default_project.slug))


class ProjectEnvironmentsEndpoint(ProjectEndpoint):
    doc_section = DocSection.PROJECTS

    @attach_scenarios([list_project_environments_scenario])
    def get(self, request, project):
        """
        List a Project's Environments
        ```````````````````````````````

        Return environments for a given project.

        :qparam string visibility: when omitted only visible environments are
                                   returned. Set to ``"hidden"`` for only hidden
                                   environments, or ``"all"`` for both hidden
                                   and visible environments.

        :pparam string organization_slug: the slug of the organization the project
                                          belongs to.

        :pparam string project_slug: the slug of the project.

        :auth: required
        """
        queryset = EnvironmentProject.objects.filter(project=project, environment__organization_id=project.organization_id).exclude(environment__name='').select_related('environment').order_by('environment__name')
        visibility = request.GET.get('visibility', 'visible')
        if visibility not in environment_visibility_filter_options:
            return Response({'detail': ("Invalid value for 'visibility', valid values are: {!r}").format(environment_visibility_filter_options.keys())}, status=400)
        add_visibility_filters = environment_visibility_filter_options[visibility]
        queryset = add_visibility_filters(queryset)
        return Response(serialize(list(queryset), request.user))