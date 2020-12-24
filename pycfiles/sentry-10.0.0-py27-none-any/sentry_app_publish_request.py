# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_app_publish_request.py
# Compiled at: 2019-08-21 05:33:05
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import options
from sentry.api.bases.sentryapps import SentryAppBaseEndpoint
from sentry.utils import email

class SentryAppPublishRequestEndpoint(SentryAppBaseEndpoint):

    def post(self, request, sentry_app):
        if sentry_app.is_published:
            return Response({'detail': 'Cannot publish already published integration'}, status=400)
        if sentry_app.is_internal:
            return Response({'detail': 'Cannot publish internal integration'}, status=400)
        message = 'User %s of organization %s wants to publish %s' % (
         request.user.email,
         sentry_app.owner.slug,
         sentry_app.slug)
        email.send_mail('Sentry App Publication Request', message, options.get('mail.from'), [
         'partners@sentry.io'], fail_silently=False)
        return Response(status=201)