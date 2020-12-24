# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/base_test.py
# Compiled at: 2020-02-09 14:11:55
# Size of source mod 2**32: 948 bytes
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
HERE = Path(__file__).parent

class BaseTest(TestCase):
    fixtures = [
     Path(HERE, 'testdump.json')]

    def setUp(self):
        user = User(username=(settings.DEBUG_ADMIN_NAME), is_superuser=True, is_staff=True)
        user.set_password(settings.DEBUG_ADMIN_PASSWORD)
        user.save()
        self.client = Client()

    def tearDown(self):
        self.logout()

    def login(self):
        """ Log the user in. """
        is_logged = self.client.login(username=(settings.DEBUG_ADMIN_NAME), password=(settings.DEBUG_ADMIN_PASSWORD))
        if not is_logged:
            raise Exception("Login failed for test user! Tests won't work.")

    def logout(self):
        """ Log the user out. """
        self.client.logout()