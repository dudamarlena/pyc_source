# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_requirement_hook.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.hooks.ConsentRequirementHook."""
from __future__ import unicode_literals
from djblets.extensions.extension import Extension
from djblets.extensions.tests import ExtensionTestsMixin
from djblets.privacy.consent import BaseConsentRequirement, get_consent_requirements_registry
from djblets.privacy.consent.hooks import ConsentRequirementHook
from djblets.testing.testcases import TestCase

class MyExtension(Extension):
    pass


class MyConsentRequirement(BaseConsentRequirement):
    requirement_id = b'my-requirement'
    name = b'My Requirement'
    summary = b'We would like to use this thing'
    intent_description = b'We need this for testing.'
    data_use_description = b'Sending all the things.'


class ConsentRequirementHookTests(ExtensionTestsMixin, TestCase):
    """Unit tests for djblets.privacy.consent.hooks.ConsentRequirementHook."""
    extension_class = MyExtension

    def setUp(self):
        super(ConsentRequirementHookTests, self).setUp()
        self.registry = get_consent_requirements_registry()
        self.extension = self.setup_extension(MyExtension)
        self.consent_requirement = MyConsentRequirement()
        self.consent_requirement_id = self.consent_requirement.requirement_id

    def tearDown(self):
        super(ConsentRequirementHookTests, self).tearDown()
        self.assertNotIn(self.consent_requirement, self.registry)

    def test_registration(self):
        """Testing ConsentRequirementHook registration"""
        self.assertIsNone(self.registry.get_consent_requirement(self.consent_requirement_id))
        ConsentRequirementHook(self.extension, self.consent_requirement)
        self.assertEqual(self.registry.get_consent_requirement(self.consent_requirement_id), self.consent_requirement)

    def test_unregistration(self):
        """Testing ConsentRequirementHook unregistration"""
        self.assertIsNone(self.registry.get_consent_requirement(self.consent_requirement_id))
        ConsentRequirementHook(self.extension, self.consent_requirement)
        self.assertEqual(self.registry.get_consent_requirement(self.consent_requirement_id), self.consent_requirement)
        self.extension.shutdown()
        self.assertIsNone(self.registry.get_consent_requirement(self.consent_requirement_id))