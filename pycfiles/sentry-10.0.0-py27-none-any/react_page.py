# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/react_page.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.conf import settings
from django.http import HttpResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.template import loader, Context
from sentry.models import Project
from sentry.signals import first_event_pending
from sentry.web.frontend.base import BaseView, OrganizationView

class ReactMixin(object):

    def get_context(self, request):
        return {'request': request, 'CSRF_COOKIE_NAME': settings.CSRF_COOKIE_NAME}

    def handle_react(self, request):
        context = Context(self.get_context(request))
        get_csrf_token(request)
        template = loader.render_to_string('sentry/bases/react.html', context)
        response = HttpResponse(template)
        response['Content-Type'] = 'text/html'
        return response


class ReactPageView(OrganizationView, ReactMixin):

    def handle_auth_required(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.handle_react(request)
        return super(ReactPageView, self).handle_auth_required(request, *args, **kwargs)

    def handle(self, request, organization, **kwargs):
        if 'project_id' in kwargs and request.GET.get('onboarding'):
            project = Project.objects.filter(organization=organization, slug=kwargs['project_id']).first()
            first_event_pending.send(project=project, user=request.user, sender=self)
        return self.handle_react(request)


class GenericReactPageView(BaseView, ReactMixin):

    def handle(self, request, **kwargs):
        return self.handle_react(request)