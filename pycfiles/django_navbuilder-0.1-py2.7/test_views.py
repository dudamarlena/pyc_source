# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/tests/test_views.py
# Compiled at: 2017-07-06 08:35:55
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from navbuilder import models
from navbuilder.tests.test_base import load_fixtures

class ViewTestCase(TestCase):

    def setUp(self):
        super(ViewTestCase, self).setUp()
        load_fixtures(self)

    def test_detail(self):
        response = self.client.get(reverse('navbuilder:menu-detail', kwargs={'slug': self.menu_data['slug']}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.menu.slug)
        self.assertContains(response, self.menuitem.slug)
        self.assertContains(response, self.sub_menuitem.slug)
        self.assertContains(response, self.menuitem.link.slug)

    def test_list(self):
        menu_data2 = {'title': 'Menu 2 Title', 
           'slug': 'menu-2-title'}
        menu2 = models.Menu.objects.create(**menu_data2)
        response = self.client.get(reverse('navbuilder:menu-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.menu.slug)
        self.assertContains(response, menu2.slug)

    def tearDown(self):
        pass