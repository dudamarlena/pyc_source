# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_func_create_user_in_admin.py
# Compiled at: 2017-01-18 10:56:11
# Size of source mod 2**32: 732 bytes
from django.test import TestCase
from pprint import pprint

class AddUserTestCase(TestCase):
    fixtures = [
     'accounting_tests']

    def test_create_user(self):
        """ Test user creation with django admin """
        new_user = {'username':'bill.test', 
         'first_name':'Bill',  'last_name':'Test',  'password1':'azerty',  'password2':'azerty'}
        c = self.client
        c.login(username='bill', password='jobs')
        response = c.post('/admin/auth/user/add', new_user, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input class="vTextField" id="id_userprofile-0-accounting_number" maxlength="8" name="userprofile-0-accounting_number" type="text">', html=True)