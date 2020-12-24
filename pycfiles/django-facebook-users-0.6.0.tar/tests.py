# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-users/facebook_users/tests.py
# Compiled at: 2015-04-13 06:05:36
from datetime import datetime
from django.test import TestCase
from .models import User
USER_ID = '4'
USER_USERNAME = 'zuck'

class FacebookUsersTest(TestCase):

    def test_fetch_user(self):
        self.assertEqual(User.objects.count(), 0)
        User.remote.fetch(USER_ID)
        User.remote.fetch(USER_USERNAME)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.all()[0]
        self.assertEqual(user.graph_id, USER_ID)
        self.assertEqual(user.name, 'Mark Zuckerberg')
        self.assertEqual(user.first_name, 'Mark')
        self.assertEqual(user.last_name, 'Zuckerberg')
        self.assertEqual(user.link, 'https://www.facebook.com/zuck')
        self.assertEqual(user.username, USER_USERNAME)
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.locale, 'en_US')
        self.assertTrue(isinstance(user.cover, dict))
        self.assertTrue(isinstance(user.updated_time, datetime))