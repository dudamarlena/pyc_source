# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_apply_license_view.py
# Compiled at: 2019-06-17 15:11:31
"""Unit tests for beanbag_licensing.views.ApplyLicenseView."""
from __future__ import unicode_literals
import base64, json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from kgb import SpyAgency
from reviewboard.admin.support import get_install_key
from beanbag_licensing.license import License
from beanbag_licensing.tests.keys import invalid_private_key, test_private_key
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase
from beanbag_licensing.views import logger

class ApplyLicenseViewTests(SpyAgency, LicensedExtensionTestCase):
    """Unit tests for beanbag_licensing.views.ApplyLicenseView."""

    def setUp(self):
        super(ApplyLicenseViewTests, self).setUp()
        User.objects.create_superuser(username=b'test-user', email=b'test@example.com', password=b'test-pass')
        self.assertTrue(self.client.login(username=b'test-user', password=b'test-pass'))
        self.spy_on(logger.error)
        self.url = reverse(b'test-apply-license')

    def test_get_with_valid_license_data(self):
        """Testing apply_license_view GET with valid license data"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=30), grace_period=3, trial=False, install_keys=[
         get_install_key()])
        response = self.client.get(self.url, data={b'license-data': base64.b64encode(license.write_str(test_private_key))})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response[b'Location'], b'http://testserver/admin/extensions/%s/config/' % self.extension.id)
        self.assertFalse(logger.error.called)
        self.assertEqual(self.extension.license_settings.license, license)

    def test_get_with_no_license_data(self):
        """Testing apply_license_view GET with no license data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received empty %s license data at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)

    def test_get_with_invalid_base64(self):
        """Testing apply_license_view GET with invalid base64 license data"""
        response = self.client.get(self.url, data={b'license-data': b'ZZZ'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received non-base64 %s license data at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)

    def test_get_with_invalid_signature(self):
        """Testing apply_license_view GET with invalid license signature"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=30), grace_period=3, trial=False, install_keys=[
         get_install_key()])
        response = self.client.get(self.url, data={b'license-data': base64.b64encode(license.write_str(invalid_private_key))})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received %s license data with bad signature at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)

    def test_get_with_invalid_install_key(self):
        """Testing apply_license_view GET with invalid install key"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=30), grace_period=3, trial=False, install_keys=[
         b'z' * 40])
        response = self.client.get(self.url, data={b'license-data': base64.b64encode(license.write_str(test_private_key))})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received %s license data for wrong install key at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)

    def test_post_with_valid_license_data(self):
        """Testing apply_license_view POST with valid license data"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=30), grace_period=3, trial=False, install_keys=[
         get_install_key()])
        response = self.client.post(self.url, data={b'license-data': license.write_str(test_private_key)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response[b'Content-Type'], b'application/json; charset=utf-8')
        data = json.loads(response.content)
        self.assertEqual(data[b'company'], b'FooCorp')
        self.assertEqual(data[b'installKey'], license.install_keys[0])
        self.assertFalse(logger.error.called)
        self.assertEqual(self.extension.license_settings.license, license)

    def test_post_with_no_license_data(self):
        """Testing apply_license_view POST with no license data"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received empty %s license data at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)

    def test_post_with_invalid_signature(self):
        """Testing apply_license_view GET with invalid license signature"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=30), grace_period=3, trial=False, install_keys=[
         get_install_key()])
        response = self.client.post(self.url, data={b'license-data': license.write_str(invalid_private_key)})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received %s license data with bad signature at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)

    def test_post_with_invalid_install_key(self):
        """Testing apply_license_view GET with invalid install key"""
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=30), grace_period=3, trial=False, install_keys=[
         b'z' * 40])
        response = self.client.post(self.url, data={b'license-data': license.write_str(test_private_key)})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(logger.error.called_with(b'Received %s license data for wrong install key at %s', b'Test Extension', b'/admin/extensions/%s/config/apply-license/' % self.extension.id))
        self.assertNotEqual(self.extension.license_settings.license, license)