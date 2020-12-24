# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/tests/test_admin.py
# Compiled at: 2017-07-06 08:35:55
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from navbuilder.tests.test_base import load_fixtures

class AdminTestCase(TestCase):

    def setUp(self):
        load_fixtures(self)
        self.client = Client()
        self.editor = get_user_model().objects.create(username='editor', email='editor@test.com', is_superuser=True, is_staff=True)
        self.editor.set_password('password')
        self.editor.save()
        self.client.login(username='editor', password='password')

    def test_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_menu(self):
        response = self.client.get('/admin/navbuilder/menu/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/admin/navbuilder/menu/add/')
        self.assertEqual(response.status_code, 200)

    def test_admin_menuitem(self):
        response = self.client.get('/admin/navbuilder/menuitem/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.menuitem.title)
        self.assertContains(response, self.menuitem.link.get_absolute_url())
        response = self.client.get('/admin/navbuilder/menuitem/add/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()