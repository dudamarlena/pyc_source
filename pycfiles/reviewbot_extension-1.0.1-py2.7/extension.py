# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/extension.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
from celery import Celery
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from djblets.db.query import get_object_or_none
from reviewboard.accounts.backends import auth_backends
from reviewboard.admin.server import get_server_url
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import IntegrationHook
from reviewbotext.integration import ReviewBotIntegration
from reviewbotext.resources import review_bot_review_resource, tool_resource

class ReviewBotExtension(Extension):
    """An extension for communicating with Review Bot."""
    metadata = {b'Name': b'Review Bot', 
       b'Summary': _(b'Performs automated analysis and review on code posted to Review Board.'), 
       b'Author': b'Review Board', 
       b'Author-URL': b'http://www.reviewboard.org/'}
    is_configurable = True
    has_admin_site = True
    resources = [
     review_bot_review_resource,
     tool_resource]
    default_settings = {b'broker_url': b'', 
       b'user': None}
    css_bundles = {b'extension-config': {b'source_filenames': [
                                                 b'css/extension-config.less'], 
                             b'apply_to': [
                                         b'reviewbot-configure']}, 
       b'integration-config': {b'source_filenames': [
                                                   b'css/integration-config.less']}}
    js_bundles = {b'extension-config': {b'source_filenames': [
                                                 b'js/extensionConfig.es6.js'], 
                             b'apply_to': [
                                         b'reviewbot-configure']}, 
       b'integration-config': {b'source_filenames': [
                                                   b'js/integrationConfig.es6.js']}}

    @property
    def user(self):
        """The configured user."""
        return get_object_or_none(User, pk=self.settings.get(b'user'))

    @property
    def celery(self):
        """The celery instance."""
        self._celery.conf[b'BROKER_URL'] = self.settings[b'broker_url']
        self._celery.conf[b'CELERY_TASK_SERIALIZER'] = b'json'
        return self._celery

    @property
    def is_configured(self):
        """Whether the extension has been properly configured."""
        return self.settings[b'user'] and self.settings[b'broker_url']

    def initialize(self):
        """Initialize the extension."""
        IntegrationHook(self, ReviewBotIntegration)
        self._celery = Celery(b'reviewbot.tasks')

    def login_user(self):
        """Log in as the configured user.

        This does not depend on the auth backend (hopefully). This is based on
        Client.login() with a small hack that does not require the call to
        authenticate().

        Returns:
            unicode:
            The session key of the new user session.
        """
        user = self.user
        backend_cls = auth_backends.get(b'backend_id', b'builtin')
        user.backend = b'%s.%s' % (backend_cls.__module__, backend_cls.__name__)
        engine = import_module(settings.SESSION_ENGINE)
        request = HttpRequest()
        request.session = engine.SessionStore()
        login(request, user)
        request.session.save()
        return request.session.session_key

    def send_refresh_tools(self):
        """Request workers to update tool list."""
        payload = {b'session': self.login_user(), 
           b'url': get_server_url()}
        self.celery.control.broadcast(b'update_tools_list', payload=payload)