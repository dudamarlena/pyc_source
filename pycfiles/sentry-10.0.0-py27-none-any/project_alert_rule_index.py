# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/incidents/endpoints/project_alert_rule_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import status
from rest_framework.response import Response
from sentry import features
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.incidents.models import AlertRule
from sentry.incidents.endpoints.serializers import AlertRuleSerializer

class ProjectAlertRuleIndexEndpoint(ProjectEndpoint):

    def get(self, request, project):
        """
        Fetches alert rules for a project
        """
        if not features.has('organizations:incidents', project.organization, actor=request.user):
            raise ResourceDoesNotExist
        return self.paginate(request, queryset=AlertRule.objects.fetch_for_project(project), order_by='-date_added', paginator_cls=OffsetPaginator, on_results=lambda x: serialize(x, request.user), default_per_page=25)

    def post(self, request, project):
        """
        Create an alert rule
        """
        if not features.has('organizations:incidents', project.organization, actor=request.user):
            raise ResourceDoesNotExist
        serializer = AlertRuleSerializer(context={'project': project}, data=request.data)
        if serializer.is_valid():
            alert_rule = serializer.save()
            return Response(serialize(alert_rule, request.user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)