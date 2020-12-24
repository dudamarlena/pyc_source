# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acollabauth/backends.py
# Compiled at: 2011-02-21 16:14:08
from django.conf import settings
from django.contrib.auth.models import User
import urllib

class ActiveCollabBackend(object):
    """ Logs into a given Active Collab site and creates
    a new user based on a successful login there """
    supports_object_permissions = False
    supports_inactive_user = False
    supports_anonymous_user = False

    def __init__(self):
        self.login_url = settings.AC_URL + '/login'

    def authenticate(self, username=None, password=None):
        try:
            email_user = username[:username.index('@')]
        except ValueError:
            return

        data = {'login[email]': username, 
           'login[password]': password, 
           'login[remember]': 1, 
           'submitted': 'submitted'}
        response = urllib.urlopen(self.login_url, urllib.urlencode(data))
        if 're_route=dashboard' in response.geturl():
            try:
                user = User.objects.get(username=email_user)
            except User.DoesNotExist:
                user = User(username=email_user, email=username)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()

            return user
        return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return

        return