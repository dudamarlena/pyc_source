# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/tests/test_template_tags.py
# Compiled at: 2018-02-10 10:04:26
# Size of source mod 2**32: 1518 bytes
from django.template import Template, Context
from django.test import RequestFactory
from django_files_library.templatetags.django_files_library import render_library, render_library_list
from django_files_library.tests.base_setup import BaseSetupTestCase

class LibraryFormsTestCase(BaseSetupTestCase):

    def test_render_library(self):
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.user = self.user1
        out = Template('{% load django_files_library %}{% render_library library %}').render(Context({'library':self.public_library,  'request':request,  'csrf_token':''}))
        expected_html = render_library({'library':self.public_library, 
         'request':request,  'csrf_token':''}, self.public_library)
        self.assertEqual(out, expected_html)

    def test_render_library_list(self):
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.user = self.user1
        out = Template('{% load django_files_library %}{% render_library_list library %}').render(Context({'library':self.public_library,  'request':request,  'csrf_token':''}))
        expected_html = render_library_list({'library':self.public_library, 
         'request':request,  'csrf_token':''}, self.public_library)
        self.assertEqual(out, expected_html)