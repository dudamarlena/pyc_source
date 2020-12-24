# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_serializers.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.serializers."""
from __future__ import unicode_literals
from datetime import datetime
from djblets.testing.testcases import TestCase
from djblets.util.serializers import DjbletsJSONEncoder

class DjbletsJSONEncoderTests(TestCase):
    """Unit tests for djblets.util.serializers.DjbletsJSONEncoder."""

    def test_object_to_json(self):
        """Testing DjbletsJSONEncoder.encode for an object with a to_json()
        method
        """

        class TestObject(object):

            def to_json(self):
                return {b'foo': 1}

        obj = TestObject()
        encoder = DjbletsJSONEncoder()
        self.assertEqual(encoder.encode(obj), b'{"foo": 1}')

    def test_datetime(self):
        """Testing DjbletsJSONENcoder.encode with datetimes"""
        encoder = DjbletsJSONEncoder()
        self.assertEqual(encoder.encode(datetime(2016, 8, 26, 3, 3, 26, 123456)), b'"2016-08-26T03:03:26"')

    def test_datetime_with_strip_ms(self):
        """Testing DjbletsJSONENcoder.encode with datetimes when using
        strip_datetime_ms=False
        """
        encoder = DjbletsJSONEncoder(strip_datetime_ms=False)
        self.assertEqual(encoder.encode(datetime(2016, 8, 26, 3, 3, 26, 123456)), b'"2016-08-26T03:03:26.123"')