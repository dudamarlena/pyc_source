# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_environment_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers
from rest_framework.response import Response
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.models import Environment, EnvironmentProject

class ProjectEnvironmentSerializer(serializers.Serializer):
    isHidden = serializers.BooleanField()


class ProjectEnvironmentDetailsEndpoint(ProjectEndpoint):

    def get(self, request, project, environment):
        try:
            instance = EnvironmentProject.objects.select_related('environment').get(project=project, environment__name=Environment.get_name_from_path_segment(environment))
        except EnvironmentProject.DoesNotExist:
            raise ResourceDoesNotExist

        return Response(serialize(instance, request.user))

    def put(self, request, project, environment):
        try:
            instance = EnvironmentProject.objects.select_related('environment').get(project=project, environment__name=Environment.get_name_from_path_segment(environment))
        except EnvironmentProject.DoesNotExist:
            raise ResourceDoesNotExist

        serializer = ProjectEnvironmentSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        data = serializer.validated_data
        fields = {}
        if 'isHidden' in data:
            fields['is_hidden'] = data['isHidden']
        if fields:
            instance.update(**fields)
        return Response(serialize(instance, request.user))