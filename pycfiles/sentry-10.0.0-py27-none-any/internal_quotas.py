# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/internal_quotas.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.conf import settings
from rest_framework.response import Response
from sentry import options
from sentry.api.base import Endpoint
from sentry.api.permissions import SuperuserPermission

class InternalQuotasEndpoint(Endpoint):
    permission_classes = (
     SuperuserPermission,)

    def get(self, request):
        return Response({'backend': settings.SENTRY_QUOTAS, 
           'options': {'system.rate-limit': options.get('system.rate-limit')}})