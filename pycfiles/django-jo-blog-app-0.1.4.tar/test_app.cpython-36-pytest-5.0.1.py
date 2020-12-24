# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/tests/test_app.py
# Compiled at: 2019-07-30 03:50:32
# Size of source mod 2**32: 217 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from django.test import TestCase
from contact.apps import ContactConfig

class ContactTests(TestCase):

    def test_app_name(self):
        app_name = ContactConfig.name
        self.assertEqual(app_name, 'contact')