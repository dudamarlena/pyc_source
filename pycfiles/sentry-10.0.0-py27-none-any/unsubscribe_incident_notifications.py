# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/unsubscribe_incident_notifications.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.core.urlresolvers import reverse
from django.http import Http404
from sentry.incidents.logic import unsubscribe_from_incident
from sentry.incidents.models import Incident
from sentry.utils.http import absolute_uri
from sentry.web.frontend.unsubscribe_notifications import UnsubscribeBaseView

class UnsubscribeIncidentNotificationsView(UnsubscribeBaseView):
    object_type = 'incident'

    def fetch_instance(self, incident_id):
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404

        return incident

    def build_link(self, instance):
        return absolute_uri(reverse('sentry-incident', kwargs={'organization_slug': instance.organization.slug, 
           'incident_id': instance.identifier}))

    def unsubscribe(self, instance, user):
        unsubscribe_from_incident(instance, user)