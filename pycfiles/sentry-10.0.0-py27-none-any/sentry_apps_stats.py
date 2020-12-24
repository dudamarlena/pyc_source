# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_apps_stats.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from django.db.models import Count
from sentry.api.bases import SentryAppsBaseEndpoint
from sentry.models import SentryApp
from sentry.api.permissions import SuperuserPermission

class SentryAppsStatsEndpoint(SentryAppsBaseEndpoint):
    permission_classes = (
     SuperuserPermission,)

    def get(self, request):
        sentry_apps = SentryApp.objects.filter(installations__date_deleted=None).annotate(Count('installations'))
        results = []
        for app in sentry_apps:
            results.append({'id': app.id, 
               'slug': app.slug, 
               'name': app.name, 
               'installs': app.installations__count})

        return Response(results)