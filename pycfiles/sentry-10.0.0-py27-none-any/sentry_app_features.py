# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_app_features.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.sentryapps import SentryAppBaseEndpoint
from sentry.api.serializers import serialize
from sentry.api.paginator import OffsetPaginator
from sentry.models import IntegrationFeature

class SentryAppFeaturesEndpoint(SentryAppBaseEndpoint):

    def get(self, request, sentry_app):
        features = IntegrationFeature.objects.filter(sentry_app_id=sentry_app.id)
        return self.paginate(request=request, queryset=features, paginator_cls=OffsetPaginator, on_results=lambda x: serialize(x, request.user))