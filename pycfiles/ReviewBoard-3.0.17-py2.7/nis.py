# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/backends/nis.py
# Compiled at: 2020-02-11 04:03:56
"""NIS authentication backend."""
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from reviewboard.accounts.backends.base import BaseAuthBackend
from reviewboard.accounts.forms.auth import NISSettingsForm

class NISBackend(BaseAuthBackend):
    """Authenticate against a user on an NIS server."""
    backend_id = b'nis'
    name = _(b'NIS')
    settings_form = NISSettingsForm
    login_instructions = _(b'Use your standard NIS username and password.')

    def authenticate(self, username, password, **kwargs):
        """Authenticate the user.

        This will authenticate the username and return the appropriate User
        object, or None.
        """
        import crypt, nis
        username = username.strip()
        try:
            passwd = nis.match(username, b'passwd').split(b':')
            original_crypted = passwd[1]
            new_crypted = crypt.crypt(password, original_crypted)
            if original_crypted == new_crypted:
                return self.get_or_create_user(username, None, passwd)
        except nis.error:
            pass

        return

    def get_or_create_user(self, username, request, passwd=None):
        """Get an existing user, or create one if it does not exist."""
        import nis
        username = username.strip()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                if not passwd:
                    passwd = nis.match(username, b'passwd').split(b':')
                names = passwd[4].split(b',')[0].split(b' ', 1)
                first_name = names[0]
                last_name = None
                if len(names) > 1:
                    last_name = names[1]
                email = b'%s@%s' % (username, settings.NIS_EMAIL_DOMAIN)
                user = User(username=username, password=b'', first_name=first_name, last_name=last_name or b'', email=email)
                user.is_staff = False
                user.is_superuser = False
                user.set_unusable_password()
                user.save()
            except nis.error:
                pass

        return user