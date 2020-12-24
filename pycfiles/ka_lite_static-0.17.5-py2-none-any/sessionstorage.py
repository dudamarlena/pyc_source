# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/formtools/tests/wizard/sessionstorage.py
# Compiled at: 2018-07-11 18:15:30
from django.test import TestCase
from django.contrib.auth.tests.utils import skipIfCustomUser
from django.contrib.formtools.tests.wizard.storage import TestStorage
from django.contrib.formtools.wizard.storage.session import SessionStorage

@skipIfCustomUser
class TestSessionStorage(TestStorage, TestCase):

    def get_storage(self):
        return SessionStorage