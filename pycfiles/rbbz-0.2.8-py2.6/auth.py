# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbbz/auth.py
# Compiled at: 2014-10-30 01:23:05
import logging
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.translation import ugettext as _
from reviewboard.accounts.backends import AuthBackend
from reviewboard.accounts.errors import UserQueryError
from rbbz.bugzilla import Bugzilla
from rbbz.errors import BugzillaError, BugzillaUrlError
from rbbz.forms import BugzillaAuthSettingsForm
from rbbz.models import get_or_create_bugzilla_users

class BugzillaBackend(AuthBackend):
    """
    Authenticate a user via Bugzilla XMLRPC.
    """
    backend_id = _('bugzilla')
    name = _('Bugzilla')
    login_instructions = _('using your Bugzilla credentials.')
    settings_form = BugzillaAuthSettingsForm

    def bz_error_response(self, request):
        logout(request)
        return PermissionDenied

    def authenticate(self, username, password, cookie=False):
        username = username.strip()
        if not cookie:
            try:
                username = User.objects.get(username=username).email
            except User.DoesNotExist:
                pass

        try:
            bugzilla = Bugzilla()
        except BugzillaUrlError:
            logging.warn('Login failure for user %s: Bugzilla URL not set.' % username)
            return
        else:
            try:
                user_data = bugzilla.log_in(username, password, cookie)
            except BugzillaError, e:
                logging.error('Login failure for user %s: %s' % (username, e))
                return

        if not user_data:
            return
        else:
            users = get_or_create_bugzilla_users(user_data)
            if not users:
                logging.error('Login failure for user %s: failed to create user.' % username)
                return
            user = users[0]
            if not user.is_active:
                logging.error('Login failure for user %s: user is not active.' % username)
                return
            if not cookie:
                (user.bzlogin, user.bzcookie) = bugzilla.cookies()
            return user

    def get_or_create_user(self, username, request):
        """Always check Bugzilla for updates."""
        username = username.strip()
        try:
            bugzilla = Bugzilla(*self._session_cookies(request.session))
        except BugzillaUrlError:
            return
        except BugzillaError:
            raise PermissionDenied

        user_data = bugzilla.get_user(username)
        if not user_data:
            raise self.bz_error_response(request)
        get_or_create_bugzilla_users(user_data)
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return

        return

    def query_users(self, query, request):
        if not query:
            return
        try:
            bugzilla = Bugzilla(*self._session_cookies(request.session))
        except BugzillaError, e:
            raise UserQueryError('Bugzilla error: %s' % e.msg)

        try:
            get_or_create_bugzilla_users(bugzilla.query_users(query))
        except BugzillaError, e:
            raise UserQueryError('Bugzilla error: %s' % e.msg)

    def search_users(self, query, request):
        """Search anywhere in name to support BMO :irc_nick convention."""
        q = Q(username__icontains=query)
        q = q | Q(email__icontains=query)
        if request.GET.get('fullname', None):
            q = q | (Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return q

    def _session_cookies(self, session):
        return (
         session.get('Bugzilla_login'),
         session.get('Bugzilla_logincookie'))