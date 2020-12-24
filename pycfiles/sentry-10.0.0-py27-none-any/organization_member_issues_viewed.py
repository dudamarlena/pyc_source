# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_member_issues_viewed.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases import OrganizationIssuesEndpoint
from sentry.models import Group

class OrganizationMemberIssuesViewedEndpoint(OrganizationIssuesEndpoint):

    def get_queryset(self, request, organization, member, project_list):
        return Group.objects.filter(groupseen__user=member.user, groupseen__project__in=project_list).extra(select={'sort_by': 'sentry_groupseen.last_seen'}).order_by('-sort_by')