# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import tsdb
from sentry.api.base import EnvironmentMixin, StatsMixin
from sentry.api.bases.group import GroupEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import Environment

class GroupStatsEndpoint(GroupEndpoint, EnvironmentMixin, StatsMixin):

    def get(self, request, group):
        try:
            environment_id = self._get_environment_id_from_request(request, group.project.organization_id)
        except Environment.DoesNotExist:
            raise ResourceDoesNotExist

        data = tsdb.get_range(model=tsdb.models.group, keys=[group.id], **self._parse_args(request, environment_id))[group.id]
        return Response(data)