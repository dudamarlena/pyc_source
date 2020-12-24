# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_events_oldest.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api import client
from sentry.api.base import DocSection
from sentry.api.bases.group import GroupEndpoint
from sentry.models import Group
from sentry.utils.apidocs import scenario, attach_scenarios
from sentry.api.helpers.environments import get_environments

@scenario('GetOldestGroupSample')
def get_oldest_group_sample_scenario(runner):
    project = runner.default_project
    group = Group.objects.filter(project=project).last()
    runner.request(method='GET', path='/issues/%s/events/oldest/' % group.id)


class GroupEventsOldestEndpoint(GroupEndpoint):
    doc_section = DocSection.EVENTS

    @attach_scenarios([get_oldest_group_sample_scenario])
    def get(self, request, group):
        """
        Retrieve the Oldest Event for an Issue
        ``````````````````````````````````````

        Retrieves the details of the oldest event for an issue.

        :pparam string group_id: the ID of the issue
        """
        environments = [ e.name for e in get_environments(request, group.project.organization) ]
        event = group.get_oldest_event_for_environments(environments)
        if not event:
            return Response({'detail': 'No events found for group'}, status=404)
        try:
            return client.get(('/projects/{}/{}/events/{}/').format(event.organization.slug, event.project.slug, event.event_id), request=request)
        except client.ApiError as e:
            return Response(e.body, status=e.status_code)