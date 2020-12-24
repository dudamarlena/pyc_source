# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_user_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from sentry.app import tsdb
from sentry.api.base import EnvironmentMixin
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import Environment

class ProjectUserStatsEndpoint(EnvironmentMixin, ProjectEndpoint):

    def get(self, request, project):
        try:
            environment_id = self._get_environment_id_from_request(request, project.organization_id)
        except Environment.DoesNotExist:
            raise ResourceDoesNotExist

        now = timezone.now()
        then = now - timedelta(days=30)
        results = tsdb.get_distinct_counts_series(tsdb.models.users_affected_by_project, (
         project.id,), then, now, rollup=86400, environment_id=environment_id)[project.id]
        return Response(results)