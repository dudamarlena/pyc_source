# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/tests/test_app.py
# Compiled at: 2017-03-29 10:08:47
from django.apps import AppConfig
from django.test import TestCase
from thema.apps import ThemaConfig

class TestThemaConfig(TestCase):

    def test_name(self):
        self.assertEqual(ThemaConfig.name, 'thema')
        self.assertTrue(issubclass(ThemaConfig, AppConfig))