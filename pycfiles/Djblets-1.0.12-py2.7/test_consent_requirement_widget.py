# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_requirement_widget.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.forms.ConsentRequirementWidget."""
from __future__ import unicode_literals
from djblets.privacy.consent import BaseConsentRequirement
from djblets.privacy.consent.forms import ConsentRequirementWidget
from djblets.privacy.tests.testcases import ConsentTestCase

class MyConsentRequirement(BaseConsentRequirement):
    requirement_id = b'my-requirement'
    name = b'My Requirement'
    summary = b'We would like to use this thing'
    intent_description = b'We need this for testing.'
    data_use_description = b'Sending all the things.'
    icons = {b'1x': b'/static/consent.png', 
       b'2x': b'/static/consent@2x.png'}


class ConsentRequirementWidgetTests(ConsentTestCase):
    """Unit tests for ConsentRequirementWidget."""

    def setUp(self):
        super(ConsentRequirementWidgetTests, self).setUp()
        self.widget = ConsentRequirementWidget(consent_requirement=MyConsentRequirement())

    def test_render(self):
        """Testing ConsentRequirementWidget.render with value=None"""
        html = self.widget.render(name=b'consent', value=None, attrs={b'id': b'my_consent'})
        self.assertIn(b'<div id="my_consent" class="privacy-consent-field privacy-consent-field-has-icon">', html)
        self.assertIn(b'<h2>We would like to use this thing</h2>', html)
        self.assertIn(b'<p>We need this for testing.</p>', html)
        self.assertIn(b'<p>Sending all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_choice_allow" name="consent_choice" value="allow">', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_choice_block" name="consent_choice" value="block">', html)
        return

    def test_render_with_value_allow(self):
        """Testing ConsentRequirementWidget.render with value=allow"""
        html = self.widget.render(name=b'consent', value=b'allow', attrs={b'id': b'my_consent'})
        self.assertIn(b'<div id="my_consent" class="privacy-consent-field privacy-consent-field-has-icon">', html)
        self.assertIn(b'<h2>We would like to use this thing</h2>', html)
        self.assertIn(b'<p>We need this for testing.</p>', html)
        self.assertIn(b'<p>Sending all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_choice_allow" name="consent_choice" value="allow" checked>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_choice_block" name="consent_choice" value="block">', html)

    def test_render_with_value_block(self):
        """Testing ConsentRequirementWidget.render with value=block"""
        html = self.widget.render(name=b'consent', value=b'block', attrs={b'id': b'my_consent'})
        self.assertIn(b'<div id="my_consent" class="privacy-consent-field privacy-consent-field-has-icon">', html)
        self.assertIn(b'<h2>We would like to use this thing</h2>', html)
        self.assertIn(b'<p>We need this for testing.</p>', html)
        self.assertIn(b'<p>Sending all the things.</p>', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_choice_allow" name="consent_choice" value="allow">', html)
        self.assertInHTML(b'<input type="radio" id="my_consent_choice_block" name="consent_choice" value="block" checked>', html)

    def test_value_from_datadict_with_value(self):
        """Testing ConsentRequirementWidget.value_from_datadict with value"""
        data = {b'consent_choice': b'allow'}
        self.assertEqual(self.widget.value_from_datadict(data=data, files={}, name=b'consent'), b'allow')

    def test_value_from_datadict_with_none(self):
        """Testing ConsentRequirementWidget.value_from_datadict without value
        """
        self.assertIsNone(self.widget.value_from_datadict(data={}, files={}, name=b'consent'))