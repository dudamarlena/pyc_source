# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/link/tests/test_admin.py
# Compiled at: 2018-05-10 08:40:57
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client

class AdminTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(AdminTestCase, cls).setUpTestData()
        cls.editor = get_user_model().objects.create(username='editor', email='editor@test.com', is_superuser=True, is_staff=True)
        cls.editor.set_password('password')
        cls.editor.save()

    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.client.login(username='editor', password='password')

    def test_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_link(self):
        response = self.client.get('/admin/link/link/add/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()