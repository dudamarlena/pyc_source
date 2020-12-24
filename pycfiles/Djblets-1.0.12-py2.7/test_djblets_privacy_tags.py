# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_djblets_privacy_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.templatetags.djblets_privacy."""
from __future__ import unicode_literals
from django.template import Context, Template
from django.test.client import RequestFactory
try:
    from django.urls import ResolverMatch
except ImportError:
    from django.core.urlresolvers import ResolverMatch

from djblets.testing.testcases import TestCase

class PIISafePageURLTemplateTagTests(TestCase):
    """Unit tests for the {% pii_safe_page_url %} template tag."""

    def test_with_pii(self):
        """Testing {% pii_safe_page_url %} with PII in URL"""
        url = self._render_url(b'/users/test/', kwargs={b'username': b'test'})
        self.assertEqual(url, b'/users/&lt;REDACTED&gt;/')

    def test_without_pii(self):
        """Testing {% pii_safe_page_url %} without PII in URL"""
        self.assertEqual(self._render_url(b'/groups/test/'), b'/groups/test/')

    def _render_url(self, path, kwargs={}):
        request = RequestFactory().get(path)
        request.resolver_match = ResolverMatch(func=lambda : None, args=(), kwargs=kwargs)
        t = Template(b'{% load djblets_privacy %}{% pii_safe_page_url %}')
        return t.render(Context({b'request': request}))