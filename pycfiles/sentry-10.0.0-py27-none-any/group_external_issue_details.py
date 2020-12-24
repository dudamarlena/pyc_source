# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_external_issue_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.group import GroupEndpoint
from sentry.mediators import external_issues
from sentry.models import PlatformExternalIssue

class GroupExternalIssueDetailsEndpoint(GroupEndpoint):

    def delete(self, request, external_issue_id, group):
        try:
            external_issue = PlatformExternalIssue.objects.get(id=external_issue_id, group_id=group.id)
        except PlatformExternalIssue.DoesNotExist:
            return Response(status=404)

        external_issues.Destroyer.run(external_issue=external_issue)
        return Response(status=204)