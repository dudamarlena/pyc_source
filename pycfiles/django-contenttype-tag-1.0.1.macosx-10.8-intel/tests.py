# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-contenttype-tag/generic_ct_tag/tests.py
# Compiled at: 2013-07-25 03:14:52
from django.utils import unittest
from django.contrib.auth.models import User
from django.template import Context, Template

class TemplateTagsTestCase(unittest.TestCase):

    def setUp(self):
        self.user = User(username='name', email='user@example.com')
        self.user.save()
        self.template = '{% load generic_ct %}'

    def tearDown(self):
        self.user.delete()

    def test_render_type(self):
        template = Template(self.template + '{% content_type obj %}')
        context = Context({'obj': self.user})
        html = template.render(context)
        self.assertIn('auth.user', html, 'Content type was not render')

    def test_render_as_name(self):
        template = Template(self.template + '{% content_type obj as ct %}{{ ct.app_label }}.{{ ct.model }}')
        context = Context({'obj': self.user})
        html = template.render(context)
        self.assertIn('auth.user', html, 'Content type was not render')