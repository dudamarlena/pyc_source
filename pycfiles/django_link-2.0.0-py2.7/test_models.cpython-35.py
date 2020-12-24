# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/tests/test_models.py
# Compiled at: 2017-07-06 07:47:29
# Size of source mod 2**32: 1561 bytes
from django.test import TestCase
from link import models

class ModelTestCase(TestCase):

    def setUp(self):
        self.link_data = {'title': 'Link 1 Title', 
         'url': '/link-1/'}
        self.viewparam_data = {'key': 'slug', 
         'value': '1'}

    def test_link(self):
        link = models.Link.objects.create(**self.link_data)
        for key, value in self.link_data.items():
            self.assertEqual(getattr(link, key), value)

        self.assertEqual(link.absolute_url, '/link-1/')
        link.view_name = 'link-2'
        self.assertEqual(link.absolute_url, '/link/2/')
        content_link_data = self.link_data.copy()
        content_link_data['url'] = '/content/1/'
        content_link = models.Link.objects.create(**content_link_data)
        link.view_name = None
        link.target = content_link
        self.assertEqual(link.absolute_url, '/content/1/')

    def test_viewparam(self):
        link = models.Link.objects.create(**self.link_data)
        viewparam = models.ViewParam.objects.create(**self.viewparam_data)
        link.view_params.add(viewparam)
        link.view_name = 'link:link-detail'
        self.assertEqual(link.absolute_url, '/link/1/')