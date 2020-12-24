# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/event_owners.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import eventstore
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.fields.actor import Actor
from sentry.api.serializers import serialize
from sentry.api.serializers.models.actor import ActorSerializer
from sentry.models import Event, ProjectOwnership

class EventOwnersEndpoint(ProjectEndpoint):

    def get(self, request, project, event_id):
        """
        Retrieve suggested owners information for an event
        ``````````````````````````````````````````````````

        :pparam string project_slug: the slug of the project the event
                                     belongs to.
        :pparam string event_id: the id of the event.
        :auth: required
        """
        event = eventstore.get_event_by_id(project.id, event_id)
        if event is None:
            return Response({'detail': 'Event not found'}, status=404)
        else:
            Event.objects.bind_nodes([event], 'data')
            owners, rules = ProjectOwnership.get_owners(project.id, event.data)
            if owners == ProjectOwnership.Everyone:
                owners = []
            return Response({'owners': serialize(Actor.resolve_many(owners), request.user, ActorSerializer()), 
               'rule': rules[0].matcher if rules else None, 
               'rules': rules or []})