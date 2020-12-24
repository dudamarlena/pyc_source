# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/tests/test_forms.py
# Compiled at: 2019-07-30 05:48:56
# Size of source mod 2**32: 707 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from django.test import TestCase
from contact.forms import ContactForm

class ContactTests(TestCase):

    def test_forms_is_valid(self):
        form_data = {'email':'test@gmail.com', 
         'message':'some message'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_forms_is_invalid(self):
        form_data = {'email':'testgmail.com', 
         'message':'some message'}
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_send_email(self):
        form_data = {'email':'test@gmail.com', 
         'message':'some message'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.send_email)