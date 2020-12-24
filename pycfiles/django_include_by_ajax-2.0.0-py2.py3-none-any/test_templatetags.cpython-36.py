# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/archatas/Projects/django_include_by_ajax/project/django_include_by_ajax/include_by_ajax/tests/test_templatetags.py
# Compiled at: 2018-10-27 22:50:42
# Size of source mod 2**32: 1843 bytes
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import RequestFactory
from include_by_ajax.templatetags.include_by_ajax_tags import include_by_ajax

class IncludeByAjaxTemplateTagTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.factory = RequestFactory()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_first_access(self):
        request = self.factory.get('/')
        template_name = 'included.html'
        context = include_by_ajax(context={'request': request}, template_name=template_name)
        self.assertEquals(context['include_by_ajax_no_placeholder_wrapping'], False)
        self.assertEquals(context['include_by_ajax_full_render'], False)
        self.assertEquals(context['template_name'], template_name)

    def test_access_by_ajax(self):
        request = self.factory.get('/', {'include_by_ajax_full_render': '1'},
          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        template_name = 'included.html'
        context = include_by_ajax(context={'request': request}, template_name=template_name)
        self.assertEquals(context['include_by_ajax_no_placeholder_wrapping'], False)
        self.assertEquals(context['include_by_ajax_full_render'], True)
        self.assertEquals(context['template_name'], template_name)

    def test_web_crawler_access(self):
        request = self.factory.get('/', HTTP_USER_AGENT='Googlebot')
        template_name = 'included.html'
        context = include_by_ajax(context={'request': request}, template_name=template_name)
        self.assertEquals(context['include_by_ajax_no_placeholder_wrapping'], True)
        self.assertEquals(context['include_by_ajax_full_render'], True)
        self.assertEquals(context['template_name'], template_name)