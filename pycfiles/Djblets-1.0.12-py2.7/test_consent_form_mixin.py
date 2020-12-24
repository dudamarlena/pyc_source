# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_form_mixin.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.forms.ConsentFormMixin."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.forms import Form
from djblets.privacy.consent import BaseConsentRequirement, Consent, get_consent_requirements_registry
from djblets.privacy.consent.forms import ConsentFormMixin
from djblets.privacy.tests.testcases import ConsentTestCase

class MyForm(ConsentFormMixin, Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(MyForm, self).__init__(*args, **kwargs)

    def get_consent_user(self):
        return self.user

    def get_consent_source(self):
        return b'https://example.com/consent/'

    def get_extra_consent_data(self):
        return {b'test': True}


class MyConsentRequirement1(BaseConsentRequirement):
    requirement_id = b'my-requirement-1'
    name = b'My Requirement 1'
    summary = b'We would like to use this thing'
    intent_description = b'We need this for testing.'
    data_use_description = b'Sending all the things.'
    icons = {b'1x': b'/static/consent.png', 
       b'2x': b'/static/consent@2x.png'}


class MyConsentRequirement2(BaseConsentRequirement):
    requirement_id = b'my-requirement-2'
    name = b'My Requirement 2'
    summary = b'We would also like this'
    intent_description = b'We need this for dancing.'
    data_use_description = b'Dancing all the things.'


class ConsentFormMixinTests(ConsentTestCase):
    """Unit tests for ConsentFormMixinTests."""

    def setUp(self):
        super(ConsentFormMixinTests, self).setUp()
        self.registry = get_consent_requirements_registry()
        self.consent_requirement_1 = MyConsentRequirement1()
        self.registry.register(self.consent_requirement_1)
        self.consent_requirement_2 = MyConsentRequirement2()
        self.registry.register(self.consent_requirement_2)
        self.user = User.objects.create(username=b'test-user')

    def test_init(self):
        """Testing ConsentFormMixin.__init__ defines field"""
        form = MyForm()
        self.assertIn(b'consent', form.fields)
        field = form.fields[b'consent']
        self.assertEqual(field.consent_requirements, [
         self.consent_requirement_1, self.consent_requirement_2])
        for subfield in field.fields:
            self.assertEqual(subfield.consent_source, b'https://example.com/consent/')
            self.assertEqual(subfield.extra_consent_data, {b'test': True})

    def test_save_consent(self):
        """Testing ConsentFormMixin.save_consent"""
        form = MyForm(data={b'consent_my-requirement-1_choice': b'allow', 
           b'consent_my-requirement-2_choice': b'block'})
        self.assertTrue(form.is_valid())
        self.assertEqual(self.consent_requirement_1.get_consent(self.user), Consent.UNSET)
        self.assertEqual(self.consent_requirement_2.get_consent(self.user), Consent.UNSET)
        form.save_consent(self.user)
        self.assertEqual(self.consent_requirement_1.get_consent(self.user), Consent.GRANTED)
        self.assertEqual(self.consent_requirement_2.get_consent(self.user), Consent.DENIED)