# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/tests/test_feature.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from datetime import datetime, timedelta
import settings_local
from kgb import SpyAgency
from rbpowerpack.sshdb.feature import SSHDBFeature
from rbpowerpack.testing.testcases import FeatureTestCase
from rbpowerpack.sshdb.secrets import has_valid_sshdb_secret_key
from rbpowerpack.sshdb.storage import disable_sshdb, enable_sshdb

class SSHDBFeatureTests(SpyAgency, FeatureTestCase):
    """Unit tests for rbpowerpack.sshdb.feature.SSHDBFeature."""
    feature_class = SSHDBFeature

    def test_check_availability_valid_full_license(self):
        """Testing SSHDBFeature.check_availability with a valid full license"""
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() + timedelta(days=20), trial=False)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_valid_trial_license(self):
        """Testing SSHDBFeature.check_availability with a valid trial license
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() + timedelta(days=20), trial=True)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_no_license(self):
        """Testing SSHDBFeature.check_availability without any license object
        set
        """
        self.install_license(None)
        self.assertEqual(self.feature.check_availability(), (
         False, b'Requires a valid Power Pack license.'))
        return

    def test_check_availability_unlicensed(self):
        """Testing SSHDBFeature.check_availability when unlicensed"""
        self.install_unlicensed()
        self.assertEqual(self.feature.check_availability(), (
         False,
         b'Requires a full license or an active trial of Power Pack.'))

    def test_check_availability_full_soft_expired(self):
        """Testing SSHDBFeature.check_availability with a soft-expired full
        license
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=1), grace_period=3, trial=False)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_full_hard_expired(self):
        """Testing SSHDBFeature.check_availability with a hard-expired full
        license
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=10), grace_period=0, trial=False)
        self.assertEqual(self.feature.check_availability(), (
         False, b'Requires a valid Power Pack license.'))

    def test_check_availability_trial_soft_expired(self):
        """Testing SSHDBFeature.check_availability with a soft-expired trial
        license
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=1), grace_period=3, trial=True)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_trial_hard_expired_no_perpetual_users(self):
        """Testing GitHubEnterpriseFeature.check_availability with a
        hard-expired trial license without perpetual user mode
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=10), grace_period=0, perpetual_users=0, trial=True)
        self.assertEqual(self.feature.check_availability(), (
         False, b'Requires a valid Power Pack license.'))

    def test_check_availability_trial_hard_expired_perpetual_users(self):
        """Testing GitHubEnterpriseFeature.check_availability with a
        hard-expired trial license with perpetual user mode
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=10), grace_period=0, perpetual_users=2, trial=True)
        self.assertEqual(self.feature.check_availability(), (
         False,
         b'Requires a full license or an active trial of Power Pack.'))

    def test_check_availability_no_valid_secret_key(self):
        """Testing GitHubEnterpriseFeature.check_availability without a
        valid SSHDB secret key
        """
        self.spy_on(has_valid_sshdb_secret_key, call_fake=lambda : False)
        self.assertEqual(self.feature.check_availability(), (
         False,
         b'To enable this feature, a valid SSHDB_SECRET_KEY must be set to a 32-character unguessable string in %s.' % settings_local.__file__.replace(b'.pyc', b'.py')))

    def test_enable_with_keys_imported(self):
        """Testing SSHDBFeature.enable with keys previously imported"""
        self.spy_on(enable_sshdb, call_fake=lambda import_keys: True)
        self.spy_on(self.extension.settings.save, call_original=False)
        self.extension.settings[b'sshdb_keys_imported'] = True
        self.check_enable()
        self.assertTrue(enable_sshdb.spy.called_with(import_keys=False))
        self.assertTrue(self.extension.settings[b'sshdb_keys_imported'])
        self.assertFalse(self.extension.settings.save.called)

    def test_enable_without_keys_imported(self):
        """Testing SSHDBFeature.enable without keys previously imported"""
        self.spy_on(enable_sshdb, call_fake=lambda import_keys: True)
        self.spy_on(self.extension.settings.save, call_original=False)
        self.assertTrue(hasattr(self.extension.settings.save, b'called'))
        self.extension.settings[b'sshdb_keys_imported'] = False
        self.check_enable()
        self.assertTrue(enable_sshdb.spy.called_with(import_keys=True))
        self.assertTrue(self.extension.settings[b'sshdb_keys_imported'])
        self.assertTrue(self.extension.settings.save.called)

    def test_disable(self):
        """Testing SSHDBFeature.disable"""
        self.spy_on(disable_sshdb, call_original=False)
        self.check_disable()
        self.assertTrue(disable_sshdb.spy.called)