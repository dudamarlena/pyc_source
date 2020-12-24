# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_incident_activity_email.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
from sentry.models import User
from django.views.generic import View
from sentry.incidents.models import Incident, IncidentActivity, IncidentActivityType
from sentry.models.organization import Organization
from sentry.incidents.tasks import generate_incident_activity_email
from .mail import MailPreview

class DebugIncidentActivityEmailView(View):

    def get(self, request):
        organization = Organization(slug='myorg')
        incident = Incident(identifier=123, organization=organization, title='Something broke')
        activity = IncidentActivity(incident=incident, user=User(name='Hello There'), type=IncidentActivityType.COMMENT.value, comment='hi')
        email = generate_incident_activity_email(activity)
        return MailPreview(html_template=email.html_template, text_template=email.template, context=email.context).render(request)