# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_multi_consent_requirement_widget.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.forms.MultiConsentRequirementsWidget.
"""
from __future__ import unicode_literals
from djblets.privacy.consent import BaseConsentRequirement
from djblets.privacy.consent.forms import MultiConsentRequirementsWidget
from djblets.testing.testcases import TestCase

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


class MultiConsentRequirementsWidgetTests(TestCase):
    """Unit tests for MultiConsentRequirementsWidget."""

    def setUp(self):
        super(MultiConsentRequirementsWidgetTests, self).setUp()
        self.widget = MultiConsentRequirementsWidget(consent_requirements=[
         MyConsentRequirement1(),
         MyConsentRequirement2()])

    def test_render(self):
        """Testing MultiConsentRequirementsWidget.render with value=[]"""
        html = self.widget.render(name=b'consent', value=[], attrs={b'id': b'my_consent'})
        self.assertIn(b'<div id="my_consent_my-requirement-1" class="privacy-consent-field privacy-consent-field-has-icon">', html)
        self.assertIn(b'<h2>We would like to use this thing</h2>', html)
        self.assertIn(b'<p>We need this for testing.</p>', html)
        self.assertIn(b'<p>Sending all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-1_choice_allow" name="consent_my-requirement-1_choice" value="allow">', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-1_choice_block" name="consent_my-requirement-1_choice" value="block">', html)
        self.assertIn(b'<div id="my_consent_my-requirement-2" class="privacy-consent-field">', html)
        self.assertIn(b'<h2>We would also like this</h2>', html)
        self.assertIn(b'<p>We need this for dancing.</p>', html)
        self.assertIn(b'<p>Dancing all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-2_choice_allow" name="consent_my-requirement-2_choice" value="allow">', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-2_choice_block" name="consent_my-requirement-2_choice" value="block">', html)

    def test_render_with_values(self):
        """Testing MultiConsentRequirementsWidget.render with values"""
        html = self.widget.render(name=b'consent', value=[
         b'allow', b'block'], attrs={b'id': b'my_consent'})
        self.assertIn(b'<div id="my_consent_my-requirement-1" class="privacy-consent-field privacy-consent-field-has-icon">', html)
        self.assertIn(b'<h2>We would like to use this thing</h2>', html)
        self.assertIn(b'<p>We need this for testing.</p>', html)
        self.assertIn(b'<p>Sending all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-1_choice_allow" name="consent_my-requirement-1_choice" value="allow" checked>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-1_choice_block" name="consent_my-requirement-1_choice" value="block">', html)
        self.assertIn(b'<div id="my_consent_my-requirement-2" class="privacy-consent-field">', html)
        self.assertIn(b'<h2>We would also like this</h2>', html)
        self.assertIn(b'<p>We need this for dancing.</p>', html)
        self.assertIn(b'<p>Dancing all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-2_choice_allow" name="consent_my-requirement-2_choice" value="allow">', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_my-requirement-2_choice_block" name="consent_my-requirement-2_choice" value="block" checked>', html)

    def test_value_from_datadict_with_value(self):
        """Testing MultiConsentRequirementsWidget.value_from_datadict with
        values
        """
        data = {b'consent_my-requirement-1_choice': b'allow', 
           b'consent_my-requirement-2_choice': b'block'}
        self.assertEqual(self.widget.value_from_datadict(data=data, files={}, name=b'consent'), [
         b'allow', b'block'])

    def test_value_from_datadict_without_values(self):
        """Testing MultiConsentRequirementsWidget.value_from_datadict without
        values
        """
        self.assertEqual(self.widget.value_from_datadict(data={}, files={}, name=b'consent'), [
         None, None])
        return