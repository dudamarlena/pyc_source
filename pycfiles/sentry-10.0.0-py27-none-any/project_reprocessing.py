# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_reprocessing.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.project import ProjectEndpoint, ProjectReleasePermission
from sentry.reprocessing import trigger_reprocessing

class ProjectReprocessingEndpoint(ProjectEndpoint):
    permission_classes = (
     ProjectReleasePermission,)

    def post(self, request, project):
        """
        Triggers the reporcessing process as a task
        """
        trigger_reprocessing(project)
        return Response(status=200)