# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_external_issues.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.group import GroupEndpoint
from sentry.api.serializers import serialize
from sentry.models import PlatformExternalIssue

class GroupExternalIssuesEndpoint(GroupEndpoint):

    def get(self, request, group):
        external_issues = PlatformExternalIssue.objects.filter(group_id=group.id)
        return self.paginate(request=request, queryset=external_issues, order_by='id', on_results=lambda x: serialize(x, request.user))