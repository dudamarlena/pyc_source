# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/scmtools/tests/test_tfs_feature.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from datetime import datetime, timedelta
from djblets.db.query import get_object_or_none
from rbpowerpack.scmtools.feature import TFSFeature
from reviewboard.scmtools.models import Tool
from rbpowerpack.testing.testcases import FeatureTestCase

class TFSFeatureTests(FeatureTestCase):
    """Unit tests for rbpowerpack.scmtools.feature.TFSFeature."""
    feature_class = TFSFeature

    def test_check_availability_valid_full_license(self):
        """Testing TFSFeature.check_availability with a valid full license"""
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() + timedelta(days=20), trial=False)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_valid_trial_license(self):
        """Testing TFSFeature.check_availability with a valid trial license"""
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() + timedelta(days=20), trial=True)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_no_license(self):
        """Testing TFSFeature.check_availability without any license object set
        """
        self.install_license(None)
        self.assertEqual(self.feature.check_availability(), (
         False, b'Requires a valid Power Pack license.'))
        return

    def test_check_availability_unlicensed(self):
        """Testing TFSFeature.check_availability when unlicensed"""
        self.install_unlicensed()
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_full_soft_expired(self):
        """Testing TFSFeature.check_availability with a soft-expired full
        license
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=1), grace_period=3, trial=False)
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_check_availability_full_hard_expired(self):
        """Testing TFSFeature.check_availability with a hard-expired full
        license
        """
        self.install_license_data(product=self.extension.licensed_product_name, expiration=datetime.utcnow() - timedelta(days=10), grace_period=0, trial=False)
        self.assertEqual(self.feature.check_availability(), (
         False, b'Requires a valid Power Pack license.'))

    def test_check_availability_trial_soft_expired(self):
        """Testing TFSFeature.check_availability with a soft-expired trial
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
        self.assertEqual(self.feature.check_availability(), (True, None))
        return

    def test_enable(self):
        """Testing TFSFeature.enable"""
        Tool.objects.filter(class_name__in=[
         b'rbpowerpack.scmtools.tfs.TFSTool',
         b'rbpowerpack.scmtools.tfs_git.TFSGitTool']).delete()
        self.check_enable()
        self.assertIsNotNone(get_object_or_none(Tool, name=b'Team Foundation Server', class_name=b'rbpowerpack.scmtools.tfs.TFSTool'))
        self.assertIsNotNone(get_object_or_none(Tool, name=b'Team Foundation Server (git)', class_name=b'rbpowerpack.scmtools.tfs_git.TFSGitTool'))

    def test_disable(self):
        """Testing TFSFeature.disable"""
        self.check_disable()