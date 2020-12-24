# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_key_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from collections import OrderedDict
from django.db.models import F
from rest_framework.response import Response
from sentry import tsdb
from sentry.api.base import StatsMixin
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import ProjectKey

class ProjectKeyStatsEndpoint(ProjectEndpoint, StatsMixin):

    def get(self, request, project, key_id):
        try:
            key = ProjectKey.objects.get(project=project, public_key=key_id, roles=F('roles').bitor(ProjectKey.roles.store))
        except ProjectKey.DoesNotExist:
            raise ResourceDoesNotExist

        try:
            stat_args = self._parse_args(request)
        except ValueError:
            return Response({'detail': 'Invalid request data'}, status=400)

        stats = OrderedDict()
        for model, name in (
         (
          tsdb.models.key_total_received, 'total'),
         (
          tsdb.models.key_total_blacklisted, 'filtered'),
         (
          tsdb.models.key_total_rejected, 'dropped')):
            result = tsdb.get_range(model=model, keys=[key.id, six.text_type(key.id)], **stat_args)
            for key_id, points in six.iteritems(result):
                for ts, count in points:
                    bucket = stats.setdefault(int(ts), {})
                    bucket.setdefault(name, 0)
                    bucket[name] += count

        return Response([ {'ts': ts, 'total': data['total'], 'dropped': data['dropped'], 'filtered': data['filtered'], 'accepted': data['total'] - data['dropped'] - data['filtered']} for ts, data in six.iteritems(stats)
                        ])