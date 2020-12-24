# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_incident_subscription_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.incident import IncidentEndpoint, IncidentPermission
from sentry.incidents.logic import subscribe_to_incident, unsubscribe_from_incident

class IncidentSubscriptionPermission(IncidentPermission):
    scope_map = IncidentPermission.scope_map.copy()
    scope_map['DELETE'] = [
     'org:write',
     'org:admin',
     'project:read',
     'project:write',
     'project:admin']


class OrganizationIncidentSubscriptionIndexEndpoint(IncidentEndpoint):
    permission_classes = (
     IncidentSubscriptionPermission,)

    def post(self, request, organization, incident):
        """
        Subscribes the authenticated user to the incident.
        ``````````````````````````````````````````````````
        Subscribes the user to the incident. If they are already subscribed
        then no-op.
        :auth: required
        """
        subscribe_to_incident(incident, request.user)
        return Response({}, status=201)

    def delete(self, request, organization, incident):
        """
        Unsubscribes the authenticated user from the incident.
        ``````````````````````````````````````````````````````
        Unsubscribes the user from the incident. If they are not subscribed then
        no-op.
        :auth: required
        """
        unsubscribe_from_incident(incident, request.user)
        return Response({}, status=200)