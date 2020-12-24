# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_member_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db.models import Q
from rest_framework.response import Response
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.serializers import serialize
from sentry.models import OrganizationMember

class ProjectMemberIndexEndpoint(ProjectEndpoint):

    def get(self, request, project):
        queryset = OrganizationMember.objects.filter(Q(user__is_active=True) | Q(user__isnull=True), organization=project.organization, teams=project.teams.all()).select_related('user').distinct()
        member_list = sorted(queryset, key=lambda x: x.user.get_display_name() if x.user_id else x.email)
        context = serialize(member_list, request.user)
        return Response(context)