# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_base_consent_requirement.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.base.BaseConsentRequirement."""
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from djblets.privacy.consent import BaseConsentRequirement, Consent, ConsentData, get_consent_tracker
from djblets.privacy.tests.testcases import ConsentTestCase

class MyConsentRequirement(BaseConsentRequirement):
    requirement_id = b'my-requirement'
    name = b'My Requirement'
    summary = b'We would like to use this thing'
    intent_description = b'We need this for testing.'
    data_use_description = b'Sending all the things.'


class BaseConsentRequirementTests(ConsentTestCase):
    """Unit tests for djblets.privacy.consent.base.BaseConsentRequirement."""

    def test_build_consent_data(self):
        """Testing BaseConsentRequirement.build_consent_data"""
        requirement = MyConsentRequirement()
        timestamp = datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc)
        consent_data = requirement.build_consent_data(granted=False, timestamp=timestamp, source=b'http://example.com/account/profile/#consent', extra_data={b'test': True})
        self.assertEqual(consent_data.requirement_id, b'my-requirement')
        self.assertFalse(consent_data.granted)
        self.assertEqual(consent_data.timestamp, timestamp)
        self.assertEqual(consent_data.source, b'http://example.com/account/profile/#consent')
        self.assertEqual(consent_data.extra_data, {b'test': True})

    def test_get_consent(self):
        """Testing BaseConsentRequirement.get_consent"""
        requirement = MyConsentRequirement()
        timestamp = datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc)
        user = User.objects.create(username=b'test-user')
        consent_data = ConsentData(requirement_id=b'my-requirement', granted=True, timestamp=timestamp, source=b'http://example.com/account/profile/#consent', extra_data={b'test': True})
        get_consent_tracker().record_consent_data(user, consent_data)
        self.assertEqual(requirement.get_consent(user), Consent.GRANTED)