# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/vsts/search.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.integration import IntegrationEndpoint
from rest_framework.response import Response
from sentry.models import Integration

class VstsSearchEndpoint(IntegrationEndpoint):

    def get(self, request, organization, integration_id):
        try:
            integration = Integration.objects.get(organizations=organization, id=integration_id, provider='vsts')
        except Integration.DoesNotExist:
            return Response(status=404)

        field = request.GET.get('field')
        query = request.GET.get('query')
        if field is None:
            return Response({'detail': 'field is a required parameter'}, status=400)
        else:
            if not query:
                return Response({'detail': 'query is a required parameter'}, status=400)
            installation = integration.get_installation(organization.id)
            if field == 'externalIssue':
                if not query:
                    return Response([])
                resp = installation.get_client().search_issues(integration.name, query)
                return Response([ {'label': '(%s) %s' % (i['fields']['system.id'], i['fields']['system.title']), 'value': i['fields']['system.id']} for i in resp.get('results', [])
                                ])
            return Response(status=400)