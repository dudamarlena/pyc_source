# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_user_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import DocSection
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.serializers import serialize
from sentry.models import EventUser

class ProjectUserDetailsEndpoint(ProjectEndpoint):
    doc_section = DocSection.PROJECTS

    def get(self, request, project, user_hash):
        euser = EventUser.objects.get(project_id=project.id, hash=user_hash)
        return Response(serialize(euser, request.user))