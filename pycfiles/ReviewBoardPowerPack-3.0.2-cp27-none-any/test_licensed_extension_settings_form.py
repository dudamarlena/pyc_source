# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_licensed_extension_settings_form.py
# Compiled at: 2019-06-17 15:11:31
"""Unit tests for beanbag_licensing.forms.LicensedExtensionSettingsForm."""
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from reviewboard.admin.support import get_install_key
from beanbag_licensing.forms import LicensedExtensionSettingsForm
from beanbag_licensing.keys import TEST_PUBLIC_KEY
from beanbag_licensing.license import License
from beanbag_licensing.tests.keys import test_private_key
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase

class LicensedExtensionSettingsFormTests(LicensedExtensionTestCase):
    """Unit tests for beanbag_licensing.forms.LicensedExtensionSettingsForm."""

    def test_clean_with_valid_license(self):
        """Testing LicensedExtensionSettingsForm.clean with valid license file
        """
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=1), grace_period=3, trial=False, install_keys=[
         get_install_key()])
        license_data = license.write_str(test_private_key)
        form = LicensedExtensionSettingsForm(extension=self.extension, license_public_key=TEST_PUBLIC_KEY, files={b'license_file': SimpleUploadedFile(b'license.lic', license_data)})
        form.is_valid()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'license_data'], license_data)
        self.assertNotIn(b'license_file', form.cleaned_data)

    def test_clean_license_file_with_non_license(self):
        """Testing LicensedExtensionSettingsForm.clean_license_file with
        non-license file
        """
        form = LicensedExtensionSettingsForm(extension=self.extension, license_public_key=TEST_PUBLIC_KEY, files={b'license_file': SimpleUploadedFile(b'license.lic', b'akjfdhasfk')})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[b'license_file'], [
         b'The uploaded file does not appear to be a valid Test license file.'])
        self.assertNotIn(b'license_data', form.cleaned_data)
        self.assertNotIn(b'license_file', form.cleaned_data)

    def test_clean_license_file_with_wrong_install_key(self):
        """Testing LicensedExtensionSettingsForm.clean_license_file with
        license for wrong install key
        """
        license = License(product=b'Test', company=b'FooCorp', users=10, expiration=datetime.utcnow() + timedelta(days=1), grace_period=3, trial=False, install_keys=[
         b'z' * 40])
        license_data = license.write_str(test_private_key)
        form = LicensedExtensionSettingsForm(extension=self.extension, license_public_key=TEST_PUBLIC_KEY, files={b'license_file': SimpleUploadedFile(b'license.lic', license_data)})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[b'license_file'], [
         b'The uploaded Test license file is not valid for this server.'])
        self.assertNotIn(b'license_data', form.cleaned_data)
        self.assertNotIn(b'license_file', form.cleaned_data)