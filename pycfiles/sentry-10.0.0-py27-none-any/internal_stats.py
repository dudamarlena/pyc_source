# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/internal_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import tsdb
from sentry.api.base import Endpoint, StatsMixin
from sentry.api.permissions import SuperuserPermission

class InternalStatsEndpoint(Endpoint, StatsMixin):
    permission_classes = (
     SuperuserPermission,)

    def get(self, request):
        key = request.GET['key']
        data = tsdb.get_range(model=tsdb.models.internal, keys=[key], **self._parse_args(request))[key]
        return Response(data)