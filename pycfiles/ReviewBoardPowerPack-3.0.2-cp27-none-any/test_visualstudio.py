# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/tests/test_visualstudio.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import get_hosting_service, register_hosting_service
from reviewboard.scmtools.crypto_utils import decrypt_password
from reviewboard.scmtools.models import Repository, Tool
from rbpowerpack.hostingsvcs.tests.testcases import ServiceTests
from rbpowerpack.hostingsvcs.visualstudio import VisualStudioTeamServices
from rbpowerpack.scmtools.tfs import TFSTool
from rbpowerpack.testing.testcases import PowerPackExtensionTestCase

class VisualStudioTeamServicesTests(PowerPackExtensionTestCase, ServiceTests):
    """Unit tests for the VisualStudioTeamServices hosting service."""
    service_name = b'visual-studio-online'

    def setUp(self):
        register_hosting_service(self.service_name, VisualStudioTeamServices)
        self.assertIsNotNone(self.service_name)
        self.service_class = get_hosting_service(self.service_name)
        super(VisualStudioTeamServicesTests, self).setUp()

    def test_service_support(self):
        """Testing the VisualStudioTeamServices service support capabilities"""
        self.assertFalse(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)
        self.assertTrue(self.service_class.supports_post_commit)

    def test_tfs_public_field_values(self):
        """Testing the VisualStudioTeamServices TFS repository field values"""
        fields = self._get_repository_fields(b'Team Foundation Server', fields={b'vso_account_name': b'myaccount'})
        self.assertEqual(fields[b'path'], b'https://myaccount.visualstudio.com/defaultcollection')
        self.assertNotIn(b'mirror_path', fields)

    def test_tfs_git_public_field_values(self):
        """Testing the VisualStudioTeamServices TFS-Git repository field values
        """
        fields = self._get_repository_fields(b'Team Foundation Server (git)', fields={b'vso_account_name': b'myaccount', 
           b'vso_project_name': b'MyProject', 
           b'vso_repository_name': b'MyRepo'})
        self.assertEqual(fields[b'path'], b'https://myaccount.visualstudio.com/DefaultCollection/MyProject/_git/MyRepo')
        self.assertNotIn(b'mirror_path', fields)

    def test_tfs_git_api_path(self):
        """Testing the VisualStudioTeamServices computed API path for TFS-Git
        """
        account = self._get_hosting_account(True)
        service = account.service
        self.assertIsNotNone(service)
        tool = Tool.objects.get(name=b'Team Foundation Server (git)')
        repository = Repository(hosting_account=account, tool=tool)
        form = self._get_form(None, {b'vso_account_name': b'myaccount', 
           b'vso_project_name': b'MyProject', 
           b'vso_repository_name': b'MyRepo'})
        form.save(repository)
        api_path = repository.extra_data[b'tfs_api_path']
        self.assertEqual(api_path, b'https://myaccount.visualstudio.com/DefaultCollection/')
        return

    def test_authorize(self):
        """Testing VisualStudioTeamServices.authorize"""
        self.spy_on(TFSTool.check_repository, call_original=False)
        account = HostingServiceAccount(service_name=self.service_name, username=b'myuser')
        service = account.service
        self.assertFalse(account.is_authorized)
        service.authorize(b'myuser', b'mypass', vso_account_name=b'myaccount')
        self.assertTrue(account.is_authorized)
        self.assertEqual(TFSTool.check_repository.last_call.kwargs, {b'path': b'https://myaccount.visualstudio.com/defaultcollection', 
           b'username': b'myuser', 
           b'password': b'mypass', 
           b'local_site_name': None, 
           b'use_basic_auth': True, 
           b'tfs_api_path': b'https://myaccount.visualstudio.com/DefaultCollection/'})
        self.assertIn(b'password', account.data)
        self.assertEqual(decrypt_password(account.data[b'password']), b'mypass')
        return