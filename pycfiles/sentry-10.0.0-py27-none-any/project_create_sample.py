# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_create_sample.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.project import ProjectEndpoint, ProjectPermission
from sentry.api.serializers import serialize
from sentry.utils.samples import create_sample_event

class ProjectCreateSampleEndpoint(ProjectEndpoint):
    permission_classes = (
     ProjectPermission,)

    def post(self, request, project):
        event = create_sample_event(project, platform=project.platform, default='javascript')
        data = serialize(event, request.user)
        return Response(data)