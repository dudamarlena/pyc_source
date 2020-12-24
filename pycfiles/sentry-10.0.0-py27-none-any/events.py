# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/incidents/events.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry import analytics

class BaseIncidentEvent(analytics.Event):
    attributes = (
     analytics.Attribute('incident_id'),
     analytics.Attribute('organization_id'),
     analytics.Attribute('incident_type'))


class IncidentCreatedEvent(BaseIncidentEvent):
    type = 'incident.created'


class IncidentStatusUpdatedEvent(BaseIncidentEvent):
    type = 'incident.status_change'
    attributes = BaseIncidentEvent.attributes + (
     analytics.Attribute('prev_status'),
     analytics.Attribute('status'))


class IncidentCommentCreatedEvent(BaseIncidentEvent):
    type = 'incident.comment'
    attributes = BaseIncidentEvent.attributes + (
     analytics.Attribute('user_id', required=False),
     analytics.Attribute('activity_id', required=False))


analytics.register(IncidentCreatedEvent)
analytics.register(IncidentStatusUpdatedEvent)
analytics.register(IncidentCommentCreatedEvent)