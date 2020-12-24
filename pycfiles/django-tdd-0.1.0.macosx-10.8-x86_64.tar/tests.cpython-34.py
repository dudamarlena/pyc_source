# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kevin/workspace/Django_TDD/lib/python3.4/site-packages/django_tdd/tests.py
# Compiled at: 2014-04-11 16:35:30
# Size of source mod 2**32: 587 bytes
from django.test import TestCase
from django.core.management import call_command

class TDDTestCase(TestCase):
    __doc__ = "\n    The most meta test case ever. Test that 'python manage.py tdd'\n    runs any tests in the project then starts the development server\n    "

    def setUp(self):
        pass

    def test_command_runs_tests_and_starts_server(self):
        self.fail('FINISH THE TEST')