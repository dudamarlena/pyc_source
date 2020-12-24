# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_data.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.base.ConsentData."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils import timezone
from djblets.privacy.consent import ConsentData
from djblets.privacy.tests.testcases import ConsentTestCase

class ConsentDataTests(ConsentTestCase):
    """Unit tests for djblets.privacy.consent.base.ConsentData."""

    def test_parse_audit_info_with_all_data(self):
        """Testing ConsentData.parse_audit_info with all data"""
        consent_data = ConsentData.parse_audit_info(b'test-requirement', {b'granted': True, 
           b'timestamp': b'2018-01-02T13:14:15+00:00', 
           b'source': b'http://example.com/account/profile/#consent', 
           b'extra_data': {b'test': True}})
        self.assertEqual(consent_data.requirement_id, b'test-requirement')
        self.assertTrue(consent_data.granted)
        self.assertEqual(consent_data.timestamp, datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc))
        self.assertEqual(consent_data.source, b'http://example.com/account/profile/#consent')
        self.assertEqual(consent_data.extra_data, {b'test': True})

    def test_parse_audit_info_with_minimum_data(self):
        """Testing ConsentData.parse_audit_info with minimum required data"""
        consent_data = ConsentData.parse_audit_info(b'test-requirement', {b'granted': False, 
           b'timestamp': b'2018-01-02T13:14:15+00:00'})
        self.assertEqual(consent_data.requirement_id, b'test-requirement')
        self.assertFalse(consent_data.granted)
        self.assertEqual(consent_data.timestamp, datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc))
        self.assertIsNone(consent_data.source)
        self.assertIsNone(consent_data.extra_data)

    def test_serialize_audit_info_with_all_data(self):
        """Testing ConsentData.serialize_audit_info with all data"""
        consent_data = ConsentData(requirement_id=b'test-requirement', granted=True, timestamp=datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc), source=b'http://example.com/account/profile/#consent', extra_data={b'test': True})
        self.assertEqual(consent_data.serialize_audit_info(b'123:test@example.com'), {b'identifier': b'123:test@example.com', 
           b'granted': True, 
           b'timestamp': b'2018-01-02T13:14:15+00:00', 
           b'source': b'http://example.com/account/profile/#consent', 
           b'extra_data': {b'test': True}})

    def test_serialize_audit_info_with_minimum_data(self):
        """Testing ConsentData.serialize_audit_info with minimum required data
        """
        consent_data = ConsentData(requirement_id=b'test-requirement', granted=False, timestamp=datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc))
        self.assertEqual(consent_data.serialize_audit_info(b'123:test@example.com'), {b'identifier': b'123:test@example.com', 
           b'granted': False, 
           b'timestamp': b'2018-01-02T13:14:15+00:00'})