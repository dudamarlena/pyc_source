# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_integrations.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry import integrations, features
from sentry.api.bases import GroupEndpoint
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.api.serializers.models.integration import IntegrationIssueSerializer
from sentry.integrations.base import IntegrationFeatures
from sentry.models import Integration

class GroupIntegrationsEndpoint(GroupEndpoint):

    def get(self, request, group):
        has_issue_basic = features.has('organizations:integrations-issue-basic', group.organization, actor=request.user)
        has_issue_sync = features.has('organizations:integrations-issue-sync', group.organization, actor=request.user)
        if not (has_issue_basic or has_issue_sync):
            return self.respond([])
        providers = [ i.key for i in integrations.all() if i.has_feature(IntegrationFeatures.ISSUE_BASIC) or i.has_feature(IntegrationFeatures.ISSUE_SYNC)
                    ]
        return self.paginate(queryset=Integration.objects.filter(organizations=group.organization, provider__in=providers), request=request, order_by='name', on_results=lambda x: serialize(x, request.user, IntegrationIssueSerializer(group)), paginator_cls=OffsetPaginator)