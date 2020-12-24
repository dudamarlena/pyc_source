# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_requirement_field.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.forms.ConsentRequirementField."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from djblets.privacy.consent import BaseConsentRequirement, Consent, get_consent_tracker
from djblets.privacy.consent.forms import ConsentRequirementField
from djblets.privacy.tests.testcases import ConsentTestCase

class MyConsentRequirement(BaseConsentRequirement):
    requirement_id = b'my-requirement'
    name = b'My Requirement'
    summary = b'We would like to use this thing'
    intent_description = b'We need this for testing.'
    data_use_description = b'Sending all the things.'
    icons = {b'1x': b'/static/consent.png', 
       b'2x': b'/static/consent@2x.png'}


class ConsentRequirementFieldTests(ConsentTestCase):
    """Unit tests for ConsentRequirementField."""

    def setUp(self):
        super(ConsentRequirementFieldTests, self).setUp()
        self.consent_requirement = MyConsentRequirement()
        self.field = ConsentRequirementField(consent_requirement=self.consent_requirement, consent_source=b'https://example.com/consent/', extra_consent_data={b'test': True})
        self.user = User.objects.create(username=b'test-user')

    def test_init_with_user_and_no_existing_consent(self):
        """Testing ConsentRequirementField.__init__ with user and no existing
        consent data
        """
        self.field.set_initial_from_user(self.user)
        self.assertEqual(self.field.initial, Consent.UNSET)

    def test_init_with_user_and_existing_consent(self):
        """Testing ConsentRequirementField.__init__ with user and existing
        consent data
        """
        get_consent_tracker().record_consent_data(self.user, self.consent_requirement.build_consent_data(granted=True))
        self.field.set_initial_from_user(self.user)
        self.assertEqual(self.field.initial, Consent.GRANTED)

    def test_set_initial_from_user(self):
        """Testing ConsentRequirementField.set_initial_from_user"""
        get_consent_tracker().record_consent_data(self.user, self.consent_requirement.build_consent_data(granted=False))
        self.field.set_initial_from_user(self.user)
        self.assertEqual(self.field.initial, Consent.DENIED)

    def test_prepare_value(self):
        """Testing ConsentRequirementField.prepare_value"""
        self.assertEqual(self.field.prepare_value(Consent.GRANTED), b'allow')
        self.assertEqual(self.field.prepare_value(Consent.DENIED), b'block')
        self.assertIsNone(self.field.prepare_value(Consent.UNSET))

    def test_clean_with_allow(self):
        """Testing ConsentRequirementField.clean with allow"""
        consent_data = self.field.clean(b'allow')
        self.assertIsNotNone(consent_data)
        self.assertEqual(consent_data.requirement_id, b'my-requirement')
        self.assertEqual(consent_data.source, b'https://example.com/consent/')
        self.assertTrue(consent_data.granted)
        self.assertEqual(consent_data.extra_data, {b'test': True})

    def test_clean_with_block(self):
        """Testing ConsentRequirementField.clean with block"""
        consent_data = self.field.clean(b'block')
        self.assertIsNotNone(consent_data)
        self.assertEqual(consent_data.requirement_id, b'my-requirement')
        self.assertEqual(consent_data.source, b'https://example.com/consent/')
        self.assertFalse(consent_data.granted)
        self.assertEqual(consent_data.extra_data, {b'test': True})

    def test_clean_with_unset(self):
        """Testing ConsentRequirementField.clean with unset"""
        message = b'You must choose Allow or Block to continue.'
        with self.assertRaisesMessage(ValidationError, message):
            self.field.clean(None)
        return