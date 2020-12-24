# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/tests/test_views.py
# Compiled at: 2017-07-06 07:47:29
from django.test import TestCase
from django.test.client import Client
from link import models

class ViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_data = {'title': 'Link 1 Title', 
           'slug': 'link-1-title', 
           'url': '/link-1/'}
        self.link = models.Link.objects.create(**self.link_data)

    def test_detail(self):
        response = self.client.get('/link/%s/' % self.link_data['slug'])
        self.assertContains(response, self.link_data['title'])

    def test_list(self):
        link_data2 = {'title': 'Link 2 Title', 
           'slug': 'link-2-title', 
           'url': '/link-2/'}
        models.Link.objects.create(**link_data2)
        response = self.client.get('/link/')
        self.assertContains(response, self.link_data['title'])
        self.assertContains(response, link_data2['title'])

    def tearDown(self):
        pass