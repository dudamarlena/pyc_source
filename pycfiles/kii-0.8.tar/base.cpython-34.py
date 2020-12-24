# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/user/tests/base.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 1224 bytes
import django
from django.conf import settings
from django.contrib.auth.models import Group
from guardian.utils import get_anonymous_user
from django.core.urlresolvers import reverse
from ...app.tests import base

class UserTestCase(base.BaseTestCase):

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()
        super(UserTestCase, self).setUp()
        self.users = {0: self.user_model(username='test0'), 
         1: self.user_model(username='test1'), 
         2: self.user_model(username='test2')}
        for key, user in self.users.items():
            user.set_password('test')
            user.save()

        self.all_users_group = Group.objects.get(name=settings.ALL_USERS_GROUP)
        self.anonymous_user = get_anonymous_user()

    def login(self, username, password='test'):
        return self.client.post(reverse(settings.LOGIN_URL), {'username': username,  'password': password})

    def logout(self):
        return self.client.get(settings.LOGOUT_URL)

    def tearDown(self):
        self.logout()

    def assertRedirectsLogin(self, response, next):
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + '?next=' + next)