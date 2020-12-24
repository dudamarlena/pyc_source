# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/currencies/tests.py
# Compiled at: 2016-12-06 14:30:11
# Size of source mod 2**32: 954 bytes
from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ohm2_handlers import utils as h_utils
from ohm2_handlers import settings as h_settings
from ohm2_handlers.currencies import utils as currencies_utils
from ohm2_handlers.currencies import serializers as currencies_serializers
from ohm2_handlers.currencies import settings
from ohm2_handlers.currencies import errors as currencies_errors
import simplejson as json

class ApiTestCase(TestCase):
    test_username = 'slipktonesraton@gmail.com'
    test_email = 'slipktonesraton@gmail.com'
    test_password = '123123123'

    def setUp(self):
        call_command('currencies_init')
        user = User.objects.create_user(self.test_username, self.test_email, self.test_password)

    def test_asd(self):
        pass