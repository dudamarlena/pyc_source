# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_requirements_registry.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.registry."""
from __future__ import unicode_literals
from djblets.privacy.consent import BaseConsentRequirement
from djblets.privacy.consent.errors import ConsentRequirementConflictError
from djblets.privacy.consent.registry import ConsentRequirementsRegistry
from djblets.privacy.tests.testcases import ConsentTestCase

class MyConsentRequirement(BaseConsentRequirement):
    requirement_id = b'test-requirement'
    name = b'Test Requirement'
    summary = b'We want this.'
    intent_description = b'Test.'
    data_use_description = b'All.'


class ConsentRequirementsRegistryTests(ConsentTestCase):
    """Unit tests for ConsentRequirementsRegistry."""

    def setUp(self):
        super(ConsentRequirementsRegistryTests, self).setUp()
        self.registry = ConsentRequirementsRegistry()

    def test_register(self):
        """Testing ConsentRequirementsRegistry.register"""
        requirement = MyConsentRequirement()
        self.registry.register(requirement)
        self.assertEqual(list(self.registry), [requirement])

    def test_register_with_conflict(self):
        """Testing ConsentRequirementsRegistry.register with conflicting ID"""
        requirement = MyConsentRequirement()
        self.registry.register(requirement)
        with self.assertRaises(ConsentRequirementConflictError):
            self.registry.register(requirement)

    def test_get_consent_requirement(self):
        """Testing ConsentRequirementsRegistry.get_consent_requirement"""
        requirement = MyConsentRequirement()
        self.registry.register(requirement)
        self.assertEqual(self.registry.get_consent_requirement(b'test-requirement'), requirement)

    def test_get_consent_requirement_with_invalid_id(self):
        """Testing ConsentRequirementsRegistry.get_consent_requirement with
        invalid ID
        """
        self.assertIsNone(self.registry.get_consent_requirement(b'test-requirement'))