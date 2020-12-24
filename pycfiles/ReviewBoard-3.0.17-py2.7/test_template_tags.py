# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_template_tags.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.template import Context, Template
from django.test.client import RequestFactory
from reviewboard.accounts.models import Profile
from reviewboard.testing import TestCase

class MarkdownTemplateTagsTests(TestCase):
    """Unit tests for Markdown-related template tags."""

    def setUp(self):
        super(MarkdownTemplateTagsTests, self).setUp()
        self.user = User.objects.create_user(b'test', b'test@example.com')
        Profile.objects.create(user=self.user, default_use_rich_text=False)
        request_factory = RequestFactory()
        request = request_factory.get(b'/')
        request.user = self.user
        self.context = Context({b'request': request})

    def test_normalize_text_for_edit_escape_html(self):
        """Testing {% normalize_text_for_edit %} escaping for HTML"""
        t = Template(b"{% load reviewtags %}{% normalize_text_for_edit '&lt;foo **bar**' True %}")
        self.assertEqual(t.render(self.context), b'&amp;lt;foo **bar**')

    def test_normalize_text_for_edit_escaping_js(self):
        """Testing {% normalize_text_for_edit %} escaping for JavaScript"""
        t = Template(b"{% load reviewtags %}{% normalize_text_for_edit '&lt;foo **bar**' True True %}")
        self.assertEqual(t.render(self.context), b'\\u0026lt\\u003Bfoo **bar**')