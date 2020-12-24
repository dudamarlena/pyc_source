# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_incident_suspects_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.incident import IncidentEndpoint, IncidentPermission
from sentry.api.serializers import serialize
from sentry.api.serializers.models.commit import CommitSerializer
from sentry.incidents.logic import get_incident_suspects

class OrganizationIncidentSuspectsIndexEndpoint(IncidentEndpoint):
    permission_classes = (
     IncidentPermission,)

    def get(self, request, organization, incident):
        """
        Fetches potential causes of an Incident.
        ````````````````````````````````````````
        Fetches potential causes of an Incident. Currently this is just suspect
        commits for all related Groups.
        :auth: required
        """
        projects = [ project for project in incident.projects.all() if request.access.has_project_access(project)
                   ]
        commits = list(get_incident_suspects(incident, projects))
        serialized_suspects = serialize(commits, request.user, serializer=CommitSerializer())
        return self.respond([ {'type': 'commit', 'data': suspect} for suspect in serialized_suspects ])