# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_servicehook_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from collections import OrderedDict
from sentry import tsdb
from sentry.api.base import StatsMixin
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import ServiceHook

class ProjectServiceHookStatsEndpoint(ProjectEndpoint, StatsMixin):

    def get(self, request, project, hook_id):
        try:
            hook = ServiceHook.objects.get(project_id=project.id, guid=hook_id)
        except ServiceHook.DoesNotExist:
            raise ResourceDoesNotExist

        stat_args = self._parse_args(request)
        stats = OrderedDict()
        for model, name in ((tsdb.models.servicehook_fired, 'total'),):
            result = tsdb.get_range(model=model, keys=[hook.id], **stat_args)[hook.id]
            for ts, count in result:
                stats.setdefault(int(ts), {})[name] = count

        return self.respond([ {'ts': ts, 'total': data['total']} for ts, data in six.iteritems(stats) ])