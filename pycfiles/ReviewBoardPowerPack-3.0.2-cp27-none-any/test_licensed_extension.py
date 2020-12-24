# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_licensed_extension.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from datetime import datetime, timedelta
from kgb import SpyAgency
from beanbag_licensing.keys import TEST_PUBLIC_KEY
from beanbag_licensing.license import License
from beanbag_licensing.tests.extension import TestExtension
from beanbag_licensing.tests.keys import test_private_key
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase

class LicensedExtensionTests(SpyAgency, LicensedExtensionTestCase):
    """Unit tests for LicensedExtension."""
    should_install_default_license = False

    def test_init_no_license(self):
        """Testing LicensedExtension initialization without a license"""
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.license.unlicensed)
        self.assertEqual(extension.license.user_cap, 2)
        self.assertTrue(extension.hooks_initialized)

    def test_init_valid_license(self):
        """Testing LicensedExtension initialization with valid license"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=1), grace_period=3, trial=True, install_keys=[])
        TestExtension.registration.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.hooks_initialized)

    def test_init_expired_license(self):
        """Testing LicensedExtension initialization with soft-expired license
        """
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() - timedelta(days=1), grace_period=3, trial=True, install_keys=[])
        TestExtension.registration.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.hooks_initialized)

    def test_init_hard_expired_license(self):
        """Testing LicensedExtension initialization with hard-expired license
        """
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() - timedelta(days=2), grace_period=0, trial=True, install_keys=[])
        TestExtension.registration.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertFalse(extension.hooks_initialized)

    def test_activating_valid_license(self):
        """Testing LicensedExtension activating valid license"""
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=1), grace_period=3, trial=True, install_keys=[])
        extension.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension.update_license()
        self.assertIsNotNone(extension.license)
        self.assertFalse(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)

    def test_activating_expired_license(self):
        """Testing LicensedExtension activating soft-expired license"""
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() - timedelta(days=1), grace_period=3, trial=True, install_keys=[])
        extension.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension.update_license()
        self.assertIsNotNone(extension.license)
        self.assertFalse(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)

    def test_activating_hard_expired_license(self):
        """Testing LicensedExtension activating hard-expired license"""
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() - timedelta(days=2), grace_period=0, trial=True, install_keys=[])
        extension.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension.update_license()
        self.assertIsNotNone(extension.license)
        self.assertFalse(extension.license.unlicensed)
        self.assertFalse(extension.hooks_initialized)

    def test_activating_license_wrong_install_key(self):
        """Testing LicensedExtension license with wrong install key"""
        extension = TestExtension(self.ext_manager)
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=1), grace_period=3, trial=True, install_keys=[
         b'z' * 40])
        extension.settings.update({b'license_public_key': TEST_PUBLIC_KEY, 
           b'license_data': license.write_str(test_private_key)})
        extension.update_license()
        self.assertIsNotNone(extension.license)
        self.assertTrue(extension.license.unlicensed)
        self.assertTrue(extension.hooks_initialized)