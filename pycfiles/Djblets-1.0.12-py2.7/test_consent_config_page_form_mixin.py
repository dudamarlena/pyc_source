# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_config_page_form_mixin.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.forms.ConsentConfigPageFormMixin."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from djblets.configforms.forms import ConfigPageForm
from djblets.configforms.pages import ConfigPage
from djblets.configforms.views import ConfigPagesView
from djblets.privacy.consent import BaseConsentRequirement, Consent, get_consent_tracker, get_consent_requirements_registry
from djblets.privacy.consent.forms import ConsentConfigPageFormMixin
from djblets.privacy.tests.testcases import ConsentTestCase

class MyForm(ConsentConfigPageFormMixin, ConfigPageForm):

    def get_extra_consent_data(self):
        return {b'test': True}


class MyPage(ConfigPage):
    form_classes = [
     MyForm]


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


class ConsentConfigPageFormMixinTests(ConsentTestCase):
    """Unit tests for ConsentConfigPageFormMixinTests."""

    def setUp(self):
        super(ConsentConfigPageFormMixinTests, self).setUp()
        self.registry = get_consent_requirements_registry()
        self.consent_requirement_1 = MyConsentRequirement1()
        self.registry.register(self.consent_requirement_1)
        self.consent_requirement_2 = MyConsentRequirement2()
        self.registry.register(self.consent_requirement_2)
        self.user = User.objects.create(username=b'test-user')
        self.request = RequestFactory().get(b'/consent/')
        self.request.user = self.user
        SessionMiddleware().process_request(self.request)
        MessageMiddleware().process_request(self.request)
        self.page = MyPage(config_view=ConfigPagesView(), request=self.request, user=self.user)

    def test_init(self):
        """Testing ConsentConfigPageFormMixin.__init__ defines field"""
        get_consent_tracker().record_consent_data(self.user, self.consent_requirement_2.build_consent_data(granted=False))
        form = MyForm(page=self.page, request=self.request, user=self.user)
        self.assertIn(b'consent', form.fields)
        field = form.fields[b'consent']
        self.assertEqual(field.initial, [Consent.UNSET, Consent.DENIED])
        self.assertEqual(field.consent_requirements, [
         self.consent_requirement_1, self.consent_requirement_2])
        for subfield in field.fields:
            self.assertEqual(subfield.consent_source, b'http://testserver/consent/')
            self.assertEqual(subfield.extra_consent_data, {b'test': True})

    def test_save(self):
        """Testing ConsentConfigPageFormMixin.save"""
        form = MyForm(page=self.page, request=self.request, user=self.user, data={b'consent_my-requirement-1_choice': b'allow', 
           b'consent_my-requirement-2_choice': b'block'})
        self.assertTrue(form.is_valid())
        self.assertEqual(self.consent_requirement_1.get_consent(self.user), Consent.UNSET)
        self.assertEqual(self.consent_requirement_2.get_consent(self.user), Consent.UNSET)
        form.save()
        self.assertEqual(self.consent_requirement_1.get_consent(self.user), Consent.GRANTED)
        self.assertEqual(self.consent_requirement_2.get_consent(self.user), Consent.DENIED)
        messages = list(get_messages(self.request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, b'Your choices have been saved. You can make changes to these at any time.')