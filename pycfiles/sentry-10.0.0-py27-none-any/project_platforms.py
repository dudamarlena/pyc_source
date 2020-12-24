# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_platforms.py
# Compiled at: 2019-08-16 12:27:39
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.project import ProjectEndpoint
from sentry.models import ProjectPlatform
from sentry.api.serializers import serialize

class ProjectPlatformsEndpoint(ProjectEndpoint):

    def get(self, request, project):
        queryset = ProjectPlatform.objects.filter(project_id=project.id)
        return Response(serialize(list(queryset), request.user))