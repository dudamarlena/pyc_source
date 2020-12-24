# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/group_event_json.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, division
from django.http import Http404, HttpResponse
from sentry import eventstore
from sentry.models import Event, Group, GroupMeta, get_group_with_redirect
from sentry.utils import json
from sentry.web.frontend.base import OrganizationView

class GroupEventJsonView(OrganizationView):
    required_scope = 'event:read'

    def get(self, request, organization, group_id, event_id_or_latest):
        try:
            group, _ = get_group_with_redirect(group_id)
        except Group.DoesNotExist:
            raise Http404

        if event_id_or_latest == 'latest':
            event = group.get_latest_event()
        else:
            event = eventstore.get_event_by_id(group.project.id, event_id_or_latest)
        if event is None:
            raise Http404
        Event.objects.bind_nodes([event], 'data')
        GroupMeta.objects.populate_cache([group])
        return HttpResponse(json.dumps(event.as_dict()), content_type='application/json')