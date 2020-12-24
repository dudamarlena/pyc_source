# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/mediators/service_hooks/creator.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from collections import Iterable
from itertools import chain
from sentry.mediators import Mediator, Param
from sentry.models import ServiceHook
from sentry.models.sentryapp import EVENT_EXPANSION

def expand_events(rolled_up_events):
    """
    Convert a list of rolled up events ('issue', etc) into a list of raw event
    types ('issue.created', etc.)
    """
    return set(chain.from_iterable([ EVENT_EXPANSION.get(event, [event]) for event in rolled_up_events ]))


def consolidate_events(raw_events):
    """
    Consolidate a list of raw event types ('issue.created', etc) into a list of
    rolled up events ('issue', etc).
    """
    return set(name for name, rolled_up_events in six.iteritems(EVENT_EXPANSION) if any(set(raw_events) & set(rolled_up_events)))


class Creator(Mediator):
    application = Param('sentry.models.ApiApplication', required=False)
    actor = Param('sentry.db.models.BaseModel')
    organization = Param('sentry.models.Organization')
    projects = Param(Iterable)
    events = Param(Iterable)
    url = Param(six.string_types)

    def call(self):
        self.hook = self._create_service_hook()
        return self.hook

    def _create_service_hook(self):
        application_id = self.application.id if self.application else None
        if not self.projects:
            project_id = self.organization.project_set.first().id
        else:
            project_id = self.projects[0].id
        hook = ServiceHook.objects.create(application_id=application_id, actor_id=self.actor.id, project_id=project_id, organization_id=self.organization.id, events=expand_events(self.events), url=self.url)
        for project in self.projects:
            hook.add_project(project)

        return hook