# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_users.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.models import OrganizationMemberWithProjectsSerializer
from sentry.models import OrganizationMember

class OrganizationUsersEndpoint(OrganizationEndpoint):

    def get(self, request, organization):
        projects = self.get_projects(request, organization)
        qs = OrganizationMember.objects.filter(user__is_active=True, organization=organization, teams__projectteam__project__in=projects).select_related('user').prefetch_related('teams', 'teams__projectteam_set', 'teams__projectteam_set__project').order_by('user__email').distinct()
        return Response(serialize(list(qs), request.user, serializer=OrganizationMemberWithProjectsSerializer(project_ids=[ p.id for p in projects ])))