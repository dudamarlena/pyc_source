# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_app_installation_external_requests.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import SentryAppInstallationBaseEndpoint
from sentry.mediators import external_requests
from sentry.models import Project

class SentryAppInstallationExternalRequestsEndpoint(SentryAppInstallationBaseEndpoint):

    def get(self, request, installation):
        try:
            project = Project.objects.get(id=request.GET.get('projectId'), organization_id=installation.organization_id)
        except Project.DoesNotExist:
            project = None

        kwargs = {'install': installation, 
           'uri': request.GET.get('uri'), 
           'query': request.GET.get('query')}
        if project:
            kwargs.update({'project': project})
        try:
            choices = external_requests.SelectRequester.run(**kwargs)
        except Exception:
            return Response({'error': 'Error communicating with Sentry App service'}, status=400)

        return Response(choices)