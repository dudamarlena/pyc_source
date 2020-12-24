# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_fn_user_admin.py
# Compiled at: 2017-04-05 12:00:50
# Size of source mod 2**32: 627 bytes
from django.test import TestCase
from django.contrib.auth.models import User

class UserAdminFormTestCase(TestCase):
    __doc__ = '\n    Test case for create and change user information and profile\n    '
    fixtures = ['test_user.yaml']

    def setUp(self):
        admin = User.objects.get(pk=1)
        self.client.force_login(admin)

    def test_user_add_form(self):
        data = {'username':'foobar', 
         'password1':'barfoo',  'password2':'barfoo'}
        response = self.client.post('/admin/auth/user/add/', data)
        print(response)
        self.assertTrue(response.status_code, 200)