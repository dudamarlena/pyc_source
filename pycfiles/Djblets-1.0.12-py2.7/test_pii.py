# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_pii.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.pii."""
from __future__ import unicode_literals
from django.http import QueryDict
from django.test.client import RequestFactory
try:
    from django.urls import ResolverMatch
except ImportError:
    from django.core.urlresolvers import ResolverMatch

from djblets.privacy.pii import build_pii_safe_page_url, build_pii_safe_page_url_for_request
from djblets.testing.testcases import TestCase

class BuildPIISafePageURLTests(TestCase):
    """Unit tests for build_pii_safe_page_url."""

    def test_with_pii_keyword_in_path(self):
        """Testing build_pii_safe_page_url_for_request with PII
        keyword-matching in URL path
        """
        self.assertEqual(build_pii_safe_page_url(url=b'/users/test/', url_kwargs={b'user': b'test'}), b'/users/<REDACTED>/')
        self.assertEqual(build_pii_safe_page_url(url=b'/users/test/', url_kwargs={b'username': b'test'}), b'/users/<REDACTED>/')
        self.assertEqual(build_pii_safe_page_url(url=b'/users/test/', url_kwargs={b'email': b'test'}), b'/users/<REDACTED>/')

    def test_with_pii_keyword_in_querystring(self):
        """Testing build_pii_safe_page_url with PII
        keyword-matching in URL query string
        """
        self.assertEqual(build_pii_safe_page_url(url=b'/', query_dict=QueryDict(b'user=test')), b'/?user=<REDACTED>')
        self.assertEqual(build_pii_safe_page_url(url=b'/', query_dict=QueryDict(b'username=test')), b'/?username=<REDACTED>')
        self.assertEqual(build_pii_safe_page_url(url=b'/', query_dict=QueryDict(b'email=test')), b'/?email=<REDACTED>')

    def test_with_pii_email_in_path(self):
        """Testing build_pii_safe_page_url with email-like value
        in URL path
        """
        self.assertEqual(build_pii_safe_page_url(url=b'/test/a@b.com/', url_kwargs={b'foo': b'a@b.com'}), b'/test/<REDACTED>/')

    def test_with_pii_email_in_querystring(self):
        """Testing build_pii_safe_page_url with email-like value
        in URL query string
        """
        self.assertEqual(build_pii_safe_page_url(url=b'/', query_dict=QueryDict(b'foo=a@b.com')), b'/?foo=<REDACTED>')

    def test_with_non_string_in_path(self):
        """Testing build_pii_safe_page_url with non-string value in URL path"""
        self.assertEqual(build_pii_safe_page_url(url=b'/test/', url_kwargs={b'type': object}), b'/test/')

    def test_with_no_pii(self):
        """Testing build_pii_safe_page_url with no PII"""
        self.assertEqual(build_pii_safe_page_url(url=b'/groups/test/', url_kwargs={b'groupname': b'test'}), b'/groups/test/')

    def test_with_no_keywords(self):
        """Testing build_pii_safe_page_url with no keywords in URL
        pattern
        """
        self.assertEqual(build_pii_safe_page_url(url=b'/groups/test/'), b'/groups/test/')


class BuildPIISafePageURLForRequestTests(TestCase):
    """Unit tests for build_pii_safe_page_url_for_request."""

    def test_with_pii_keyword_in_path(self):
        """Testing build_pii_safe_page_url_for_request with PII
        keyword-matching in URL path
        """
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/users/test/', {b'user': b'test'})), b'/users/<REDACTED>/')
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/users/test/', {b'username': b'test'})), b'/users/<REDACTED>/')
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/users/test/', {b'email': b'test'})), b'/users/<REDACTED>/')

    def test_with_pii_keyword_in_querystring(self):
        """Testing build_pii_safe_page_url_for_request with PII
        keyword-matching in URL query string
        """
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/?user=test')), b'/?user=<REDACTED>')
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/?username=test')), b'/?username=<REDACTED>')
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/?email=test')), b'/?email=<REDACTED>')

    def test_with_pii_email_in_path(self):
        """Testing build_pii_safe_page_url_for_request with email-like value
        in URL path
        """
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/test/a@b.com/', {b'foo': b'a@b.com'})), b'/test/<REDACTED>/')

    def test_with_pii_email_in_querystring(self):
        """Testing build_pii_safe_page_url_for_request with email-like value
        in URL query string
        """
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/?foo=a@b.com')), b'/?foo=<REDACTED>')

    def test_with_no_pii(self):
        """Testing build_pii_safe_page_url_for_request with no PII"""
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/groups/test/', {b'groupname': b'test'})), b'/groups/test/')

    def test_with_no_keywords(self):
        """Testing build_pii_safe_page_url_for_request with no keywords in URL
        pattern
        """
        self.assertEqual(build_pii_safe_page_url_for_request(self._build_request(b'/groups/test/')), b'/groups/test/')

    def test_with_no_resolver_match(self):
        """Testing build_pii_safe_page_url_for_request with no resolver match
        """
        self.assertEqual(build_pii_safe_page_url_for_request(RequestFactory().get(b'/groups/test/')), b'/groups/test/')

    def _build_request(self, path, kwargs={}):
        request = RequestFactory().get(path)
        request.resolver_match = ResolverMatch(func=lambda : None, args=(), kwargs=kwargs)
        return request