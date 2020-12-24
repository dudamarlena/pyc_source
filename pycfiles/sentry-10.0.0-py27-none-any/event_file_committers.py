# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/event_file_committers.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import eventstore
from sentry.api.bases.project import ProjectEndpoint
from sentry.models import Commit, Event, Release
from sentry.utils.committers import get_serialized_event_file_committers

class EventFileCommittersEndpoint(ProjectEndpoint):

    def get(self, request, project, event_id):
        """
        Retrieve Committer information for an event
        ```````````````````````````````````````````

        Return commiters on an individual event, plus a per-frame breakdown.

        :pparam string project_slug: the slug of the project the event
                                     belongs to.
        :pparam string event_id: the hexadecimal ID of the event to
                                 retrieve (as reported by the raven client).
        :auth: required
        """
        event = eventstore.get_event_by_id(project.id, event_id)
        if event is None:
            return Response({'detail': 'Event not found'}, status=404)
        else:
            Event.objects.bind_nodes([event], 'data')
            try:
                committers = get_serialized_event_file_committers(project, event, frame_limit=int(request.GET.get('frameLimit', 25)))
            except Release.DoesNotExist:
                return Response({'detail': 'Release not found'}, status=404)
            except Commit.DoesNotExist:
                return Response({'detail': 'No Commits found for Release'}, status=404)

            data = {'committers': committers}
            return Response(data)