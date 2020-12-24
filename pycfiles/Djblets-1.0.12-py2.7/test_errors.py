# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_errors.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from djblets.testing.testcases import TestCase
from djblets.webapi.errors import WebAPIError

class WebAPIErrorTests(TestCase):
    """Unit tests for djblets.webapi.errors."""

    def test_with_message(self):
        """Testing WebAPIError.with_message"""
        orig_msg = b'Original message'
        new_msg = b'New message'
        headers = {b'foo': b'bar'}
        orig_error = WebAPIError(123, orig_msg, http_status=500, headers=headers)
        new_error = orig_error.with_message(new_msg)
        self.assertNotEqual(orig_error, new_error)
        self.assertEqual(new_error.msg, new_msg)
        self.assertEqual(new_error.headers, headers)
        self.assertEqual(new_error.code, orig_error.code)
        self.assertEqual(new_error.http_status, orig_error.http_status)
        self.assertEqual(orig_error.msg, orig_msg)
        self.assertEqual(orig_error.headers, headers)

    def test_with_overrides(self):
        """Testing WebAPIError.with_overrides"""
        orig_msg = b'Original message'
        new_msg = b'New message'
        orig_headers = {b'foo': b'bar'}
        new_headers = {b'abc': b'123'}
        orig_error = WebAPIError(123, orig_msg, http_status=500, headers=orig_headers)
        new_error = orig_error.with_overrides(new_msg, headers=new_headers)
        self.assertNotEqual(orig_error, new_error)
        self.assertEqual(new_error.msg, new_msg)
        self.assertEqual(new_error.headers, new_headers)
        self.assertEqual(new_error.code, orig_error.code)
        self.assertEqual(new_error.http_status, orig_error.http_status)
        self.assertEqual(orig_error.msg, orig_msg)
        self.assertEqual(orig_error.headers, orig_headers)