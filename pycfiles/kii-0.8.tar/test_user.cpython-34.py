# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/user/tests/test_user.py
# Compiled at: 2014-10-07 12:57:05
# Size of source mod 2**32: 603 bytes
from . import base
from ...tests import test_user
from django.contrib.auth.models import Group
from django.conf import settings

class TestUserData(base.UserTestCase):

    def test_users_are_added_to_default_group_on_creation_except_anonymous_user(self):
        users = self.user_model.objects.all().exclude(pk=self.anonymous_user.pk)
        self.assertEqual(len(users), len(self.all_users_group.user_set.all()))
        for u in users:
            self.assertIn(u, self.all_users_group.user_set.all())

        self.assertNotIn(self.anonymous_user, self.all_users_group.user_set.all())