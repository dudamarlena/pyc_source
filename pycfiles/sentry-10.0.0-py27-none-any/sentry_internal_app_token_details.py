# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_internal_app_token_details.py
# Compiled at: 2019-08-21 05:33:05
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from sentry.api.bases import SentryInternalAppTokenPermission, SentryAppBaseEndpoint
from sentry.models import ApiToken
from sentry.mediators.sentry_app_installation_tokens import Destroyer

class SentryInternalAppTokenDetailsEndpoint(SentryAppBaseEndpoint):
    permission_classes = (
     SentryInternalAppTokenPermission,)

    def convert_args(self, request, sentry_app_slug, api_token, *args, **kwargs):
        args, kwargs = super(SentryInternalAppTokenDetailsEndpoint, self).convert_args(request, sentry_app_slug, *args, **kwargs)
        try:
            kwargs['api_token'] = ApiToken.objects.get(token=api_token)
        except ApiToken.DoesNotExist:
            raise Http404

        return (args, kwargs)

    def delete(self, request, sentry_app, api_token):
        if api_token.application_id != sentry_app.application_id:
            raise Http404
        if not sentry_app.is_internal:
            return Response('This route is limited to internal integrations only', status=status.HTTP_403_FORBIDDEN)
        Destroyer.run(api_token=api_token, user=request.user, request=request)
        return Response(status=204)