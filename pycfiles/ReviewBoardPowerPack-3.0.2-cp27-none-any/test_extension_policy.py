# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/tests/test_extension_policy.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from datetime import datetime, timedelta
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase
from django.contrib.auth.models import User
from rbpowerpack.extension import PowerPackExtension
from rbpowerpack.extension.policy import FeaturePolicy

class DisabledFeaturePolicy(FeaturePolicy):

    def is_aws_codecommit_enabled(self, user, repository):
        return False

    def is_bitbucket_server_enabled(self, user, repository):
        return False

    def is_github_enterprise_enabled(self, user, repository):
        return False

    def is_pdf_enabled(self, user, review_request):
        return False

    def is_reporting_enabled(self, user, local_site_name):
        return False

    def is_visual_studio_team_services_enabled(self, user, repository):
        return False


class ExtensionPolicyTestCase(LicensedExtensionTestCase):
    """Test template for rbpowerpack.extension.policy.ExtensionPolicy"""
    __test__ = False
    extension_class = PowerPackExtension
    settings_key = None
    is_enabled_method_name = None

    def setUp(self):
        """Set up the test cases."""
        super(ExtensionPolicyTestCase, self).setUp()
        self.user = User.objects.create(username=b'doc')

    def shortDescription(self):
        """Return a short description for the currently-running test.

        Returns:
            unicode:
            The string to use when printing the test name.
        """
        desc = super(ExtensionPolicyTestCase, self).shortDescription()
        desc = desc.replace(b'<METHOD_NAME>', self.is_enabled_method_name)
        return desc

    def test_enabled_valid_no_user_cap(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with enabled and no user cap
        """
        self.install_license_data(users=0)
        self.extension.settings[self.settings_key] = True
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertTrue(is_enabled_method(self.user, None))
        return

    def test_enabled_valid_licensed_user(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with enabled and licensed
        user
        """
        self.extension.settings[self.settings_key] = True
        self.license_settings.add_licensed_users([self.user])
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertTrue(is_enabled_method(self.user, None))
        return

    def test_enabled_unlicensed_user(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with enabled and unlicensed
        user
        """
        self.extension.settings[self.settings_key] = True
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertFalse(is_enabled_method(self.user, None))
        return

    def test_enabled_no_license(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with no license"""
        self.extension.settings[self.settings_key] = True
        self.install_license(None)
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertFalse(is_enabled_method(self.user, None))
        return

    def test_enabled_unlicensed(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with unlicensed state"""
        self.extension.settings[self.settings_key] = True
        self.install_unlicensed()
        self.license_settings.add_licensed_users([self.user])
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertTrue(is_enabled_method(self.user, None))
        return

    def test_enabled_license_expired(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with expired license"""
        self.extension.settings[self.settings_key] = True
        self.install_license_data(expiration=datetime.utcnow() - timedelta(minutes=1), grace_period=0, users=0)
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertFalse(is_enabled_method(self.user, None))
        return

    def test_enabled_setting_disabled(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with setting disabled"""
        self.install_license_data(users=0)
        self.extension.settings[self.settings_key] = False
        self.extension.reload_features()
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertFalse(is_enabled_method(self.user, None))
        return

    def test_enabled_feature_policy_disabled(self):
        """Testing ExtensionPolicy.<METHOD_NAME> with feature policy disabled
        """
        self.install_license_data(users=0)
        self.extension.settings[self.settings_key] = True
        self.extension.reload_features()
        self.extension.policy.feature_policy = DisabledFeaturePolicy(self.extension)
        is_enabled_method = getattr(self.extension.policy, self.is_enabled_method_name)
        self.assertFalse(is_enabled_method(self.user, None))
        return


class AWSCodeCommitExtensionPolicyTests(ExtensionPolicyTestCase):
    """Unit tests for ExtensionPolicy.is_aws_codecommit_enabled."""
    __test__ = True
    settings_key = b'aws_codecommit_enabled'
    is_enabled_method_name = b'is_aws_codecommit_enabled'


class BitbucketServerExtensionPolicyTests(ExtensionPolicyTestCase):
    """Unit tests for ExtensionPolicy.is_bitbucket_server_enabled."""
    __test__ = True
    settings_key = b'bitbucket_server_enabled'
    is_enabled_method_name = b'is_bitbucket_server_enabled'


class GitHubEnterpriseExtensionPolicyTests(ExtensionPolicyTestCase):
    """Unit tests for ExtensionPolicy.is_github_enterprise_enabled."""
    __test__ = True
    settings_key = b'github_enterprise_enabled'
    is_enabled_method_name = b'is_github_enterprise_enabled'


class PDFExtensionPolicyTests(ExtensionPolicyTestCase):
    """Unit tests for ExtensionPolicy.is_pdf_enabled."""
    __test__ = True
    settings_key = b'pdf_review_enabled'
    is_enabled_method_name = b'is_pdf_enabled'


class ReportingExtensionPolicyTests(ExtensionPolicyTestCase):
    """Unit tests for ExtensionPolicy.is_reporting_enabled."""
    __test__ = True
    settings_key = b'reports_enabled'
    is_enabled_method_name = b'is_reporting_enabled'


class VisualStudioTeamServicesExtensionPolicyTests(ExtensionPolicyTestCase):
    """Unit tests for ExtensionPolicy.is_visual_studio_online_enabled."""
    __test__ = True
    settings_key = b'visual_studio_online_enabled'
    is_enabled_method_name = b'is_visual_studio_team_services_enabled'