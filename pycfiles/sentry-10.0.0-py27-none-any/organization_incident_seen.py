# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_incident_seen.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.incident import IncidentEndpoint, IncidentPermission
from sentry.incidents.logic import set_incident_seen

class OrganizationIncidentSeenEndpoint(IncidentEndpoint):
    permission_classes = (
     IncidentPermission,)

    def post(self, request, organization, incident):
        """
        Mark an incident as seen by the user
        ````````````````````````````````````

        :auth: required
        """
        set_incident_seen(incident=incident, user=request.user)
        return Response({}, status=201)