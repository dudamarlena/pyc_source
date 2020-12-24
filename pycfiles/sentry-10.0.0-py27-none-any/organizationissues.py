# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/bases/organizationissues.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import EnvironmentMixin
from sentry.api.serializers import serialize, StreamGroupSerializer
from sentry.api.paginator import OffsetPaginator
from sentry.models import Group, GroupStatus, OrganizationMemberTeam, Project, ProjectStatus
from .organizationmember import OrganizationMemberEndpoint
ERR_INVALID_STATS_PERIOD = "Invalid stats_period. Valid choices are '', '24h', and '14d'"

class OrganizationIssuesEndpoint(OrganizationMemberEndpoint, EnvironmentMixin):

    def get_queryset(self, request, organization, member, project_list):
        return Group.objects.none()

    def get(self, request, organization, member):
        """
        Return a list of issues assigned to the given member.
        """
        stats_period = request.GET.get('statsPeriod')
        if stats_period not in (None, '', '24h', '14d'):
            return Response({'detail': ERR_INVALID_STATS_PERIOD}, status=400)
        else:
            if stats_period is None:
                stats_period = '24h'
            else:
                if stats_period == '':
                    stats_period = None
                project_list = Project.objects.filter(organization=organization, teams__in=OrganizationMemberTeam.objects.filter(organizationmember=member).values('team'))
                queryset = self.get_queryset(request, organization, member, project_list)
                status = request.GET.get('status', 'unresolved')
                if status == 'unresolved':
                    queryset = queryset.filter(status=GroupStatus.UNRESOLVED)
                elif status:
                    return Response({'status': 'Invalid status choice'}, status=400)
            queryset = queryset.filter(project__status=ProjectStatus.VISIBLE)

            def on_results(results):
                results = serialize(results, request.user, StreamGroupSerializer(environment_func=self._get_environment_func(request, organization.id), stats_period=stats_period))
                if request.GET.get('status') == 'unresolved':
                    results = [ r for r in results if r['status'] == 'unresolved' ]
                return results

            return self.paginate(request=request, queryset=queryset, order_by='-sort_by', paginator_cls=OffsetPaginator, on_results=on_results)