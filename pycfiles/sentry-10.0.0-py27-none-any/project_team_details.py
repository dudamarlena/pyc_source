# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_team_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.http import Http404
from rest_framework.response import Response
from sentry.api.bases.project import ProjectEndpoint, ProjectPermission
from sentry.api.serializers import serialize
from sentry.api.serializers.models.project import ProjectWithTeamSerializer
from sentry.models import Team

class ProjectTeamsPermission(ProjectPermission):
    scope_map = {'GET': [
             'project:read', 'project:write', 'project:admin'], 
       'POST': [
              'project:write', 'project:admin'], 
       'PUT': [
             'project:write', 'project:admin'], 
       'DELETE': [
                'project:write', 'project:admin']}


class ProjectTeamDetailsEndpoint(ProjectEndpoint):
    permission_classes = (
     ProjectTeamsPermission,)

    def post(self, request, project, team_slug):
        """
        Give a team access to a project
        ```````````````````````````````
        :pparam string organization_slug: the slug of the organization.
        :pparam string project_slug: the slug of the project.
        :pparam string team_slug: the slug of the project.
        :auth: required
        """
        try:
            team = Team.objects.get(organization_id=project.organization_id, slug=team_slug)
        except Team.DoesNotExist:
            raise Http404

        if not request.access.has_team_scope(team, 'project:write'):
            return Response({'detail': ['You do not have permission to perform this action.']}, status=403)
        project.add_team(team)
        return Response(serialize(project, request.user, ProjectWithTeamSerializer()), status=201)

    def delete(self, request, project, team_slug):
        """
        Revoke a team's access to a project
        ```````````````````````````````````
        :pparam string organization_slug: the slug of the organization.
        :pparam string project_slug: the slug of the project.
        :pparam string team_slug: the slug of the project.
        :auth: required
        """
        try:
            team = Team.objects.get(organization_id=project.organization_id, slug=team_slug)
        except Team.DoesNotExist:
            raise Http404

        if not request.access.has_team_scope(team, 'project:write'):
            return Response({'detail': ['You do not have permission to perform this action.']}, status=403)
        project.remove_team(team)
        return Response(serialize(project, request.user, ProjectWithTeamSerializer()), status=200)