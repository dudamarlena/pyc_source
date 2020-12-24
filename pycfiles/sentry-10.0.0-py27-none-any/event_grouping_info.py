# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/event_grouping_info.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from django.http import HttpResponse
from sentry import eventstore
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.grouping.api import GroupingConfigNotFound
from sentry.models import Event
from sentry.utils import json

class EventGroupingInfoEndpoint(ProjectEndpoint):

    def get(self, request, project, event_id):
        """
        Returns the grouping information for an event
        `````````````````````````````````````````````

        This endpoint returns a JSON dump of the metadata that went into the
        grouping algorithm.
        """
        event = eventstore.get_event_by_id(project.id, event_id)
        if event is None:
            raise ResourceDoesNotExist
        Event.objects.bind_nodes([event], 'data')
        rv = {}
        config_name = request.GET.get('config') or None
        hashes = event.get_hashes()
        try:
            variants = event.get_grouping_variants(force_config=config_name, normalize_stacktraces=True)
        except GroupingConfigNotFound:
            raise ResourceDoesNotExist(detail='Unknown grouping config')

        for key, variant in six.iteritems(variants):
            d = variant.as_dict()
            d['hashMismatch'] = d['hash'] is not None and d['hash'] not in hashes
            d['key'] = key
            rv[key] = d

        return HttpResponse(json.dumps(rv), content_type='application/json')