# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_member_issues_assigned.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases import OrganizationIssuesEndpoint
from sentry.models import Group, OrganizationMemberTeam, Team
from django.db.models import Q

class OrganizationMemberIssuesAssignedEndpoint(OrganizationIssuesEndpoint):

    def get_queryset(self, request, organization, member, project_list):
        teams = Team.objects.filter(id__in=OrganizationMemberTeam.objects.filter(organizationmember=member, is_active=True).values('team'))
        return Group.objects.filter(Q(assignee_set__user=member.user, assignee_set__project__in=project_list) | Q(assignee_set__team__in=teams)).extra(select={'sort_by': 'sentry_groupasignee.date_added'}).order_by('-sort_by')