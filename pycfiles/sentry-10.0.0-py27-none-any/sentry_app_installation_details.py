# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_app_installation_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import SentryAppInstallationBaseEndpoint
from sentry.api.serializers import serialize
from sentry.mediators.sentry_app_installations import Destroyer, Updater
from sentry.api.serializers.rest_framework import SentryAppInstallationSerializer

class SentryAppInstallationDetailsEndpoint(SentryAppInstallationBaseEndpoint):

    def get(self, request, installation):
        return Response(serialize(installation))

    def delete(self, request, installation):
        Destroyer.run(install=installation, user=request.user, request=request)
        return Response(status=204)

    def put(self, request, installation):
        serializer = SentryAppInstallationSerializer(installation, data=request.data, partial=True)
        if serializer.is_valid():
            result = serializer.validated_data
            updated_installation = Updater.run(user=request.user, sentry_app_installation=installation, status=result.get('status'))
            return Response(serialize(updated_installation, request.user))
        return Response(serializer.errors, status=400)