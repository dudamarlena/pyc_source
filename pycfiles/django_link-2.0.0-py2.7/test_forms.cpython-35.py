# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/tests/test_forms.py
# Compiled at: 2018-05-10 08:23:26
# Size of source mod 2**32: 1006 bytes
from django.test import TestCase
from link import forms

class FormTestCase(TestCase):

    def setUp(self):
        self.form_data = {'title': 'Link 1 Title', 
         'slug': 'link-1-title'}

    def test_admin_form(self):
        admin_form = forms.LinkAdminForm(self.form_data)
        admin_form.full_clean()
        self.assertEqual(len(admin_form.errors['__all__']), 1)
        self.form_data['url'] = '/test-link/'
        admin_form = forms.LinkAdminForm(self.form_data)
        self.assertTrue(admin_form.is_valid())
        self.assertEqual(len(admin_form.errors), 0)
        self.form_data['view_name'] = 'link-1'
        admin_form = forms.LinkAdminForm(self.form_data)
        admin_form.full_clean()
        self.assertEqual(len(admin_form.errors['__all__']), 1)

    def tearDown(self):
        pass