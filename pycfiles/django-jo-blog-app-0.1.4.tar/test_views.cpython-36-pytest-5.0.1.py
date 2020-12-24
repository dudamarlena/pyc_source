# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/tests/test_views.py
# Compiled at: 2019-07-30 03:46:43
# Size of source mod 2**32: 682 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from django.contrib.auth import get_user_model
from django.test import TestCase, client
from django.urls import reverse

class ContactTests(TestCase):

    def test_contact_url_state(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')