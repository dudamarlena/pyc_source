# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_internal_app_tokens.py
# Compiled at: 2019-08-21 05:33:05
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework import status
from sentry.api.bases import SentryInternalAppTokenPermission, SentryAppBaseEndpoint
from sentry.models import ApiToken, SentryAppInstallation
from sentry.mediators.sentry_app_installation_tokens import Creator
from sentry.api.serializers.models.apitoken import ApiTokenSerializer
from sentry.exceptions import ApiTokenLimitError

class SentryInternalAppTokensEndpoint(SentryAppBaseEndpoint):
    permission_classes = (
     SentryInternalAppTokenPermission,)

    def get(self, request, sentry_app):
        if not sentry_app.is_internal:
            return Response([])
        else:
            tokens = ApiToken.objects.filter(application_id=sentry_app.application_id)
            attrs = {'application': None}
            return Response(ApiTokenSerializer().serialize(token, attrs, request.user) for token in tokens)

    def post(self, request, sentry_app):
        if not sentry_app.is_internal:
            return Response('This route is limited to internal integrations only', status=status.HTTP_403_FORBIDDEN)
        else:
            sentry_app_installation = SentryAppInstallation.objects.get(sentry_app=sentry_app)
            try:
                api_token = Creator.run(request=request, sentry_app_installation=sentry_app_installation, user=request.user)
            except ApiTokenLimitError as e:
                return Response(e.message, status=status.HTTP_403_FORBIDDEN)

            attrs = {'application': None}
            return Response(ApiTokenSerializer().serialize(api_token, attrs, request.user), status=201)