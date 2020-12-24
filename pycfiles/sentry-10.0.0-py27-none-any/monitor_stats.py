# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/monitor_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from collections import OrderedDict
from rest_framework.response import Response
from sentry import tsdb
from sentry.api.base import StatsMixin
from sentry.api.bases.monitor import MonitorEndpoint
from sentry.models import MonitorCheckIn, CheckInStatus

class MonitorStatsEndpoint(MonitorEndpoint, StatsMixin):

    def get(self, request, project, monitor):
        args = self._parse_args(request)
        stats = OrderedDict()
        current = tsdb.normalize_to_epoch(args['start'], args['rollup'])
        end = tsdb.normalize_to_epoch(args['end'], args['rollup'])
        while current <= end:
            stats[current] = {CheckInStatus.OK: 0, CheckInStatus.ERROR: 0}
            current += args['rollup']

        history = MonitorCheckIn.objects.filter(monitor=monitor, status__in=[
         CheckInStatus.OK, CheckInStatus.ERROR], date_added__gt=args['start'], date_added__lte=args['end']).values_list('date_added', 'status')
        for datetime, status in history.iterator():
            stats[tsdb.normalize_to_epoch(datetime, args['rollup'])][status] += 1

        return Response([ {'ts': ts, 'ok': data[CheckInStatus.OK], 'error': data[CheckInStatus.ERROR]} for ts, data in six.iteritems(stats)
                        ])