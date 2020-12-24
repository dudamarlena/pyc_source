# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/tests/test_github_enterprise.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import json
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import get_hosting_service, register_hosting_service, unregister_hosting_service
from reviewboard.scmtools.models import Repository
from rbpowerpack.hostingsvcs.githubenterprise import GitHubEnterprise
from rbpowerpack.hostingsvcs.tests.testcases import ServiceTests

class GitHubEnterpriseTests(ServiceTests):
    """Unit tests for the GitHubEnterprise hosting service."""
    service_name = b'github-enterprise'

    def __init__(self, *args, **kwargs):
        self.service_name = b'github'
        super(GitHubEnterpriseTests, self).__init__(*args, **kwargs)
        self.service_class = None
        self.service_name = GitHubEnterpriseTests.service_name
        return

    def setUp(self):
        register_hosting_service(self.service_name, GitHubEnterprise)
        self.assertNotEqual(self.service_name, None)
        self.service_class = get_hosting_service(self.service_name)
        super(GitHubEnterpriseTests, self).setUp()
        return

    def tearDown(self):
        super(GitHubEnterpriseTests, self).tearDown()
        unregister_hosting_service(self.service_name)

    def test_service_support(self):
        """Testing the GitHubEnterprise service support capabilities"""
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)

    def test_public_field_values(self):
        """Testing the GitHubEnterprise public plan repository field values"""
        fields = self._get_repository_fields(b'Git', plan=b'public', with_url=True, fields={b'github_enterprise_public_repo_name': b'myrepo', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(fields[b'path'], b'git@example.com:myuser/myrepo.git')
        self.assertEqual(fields[b'mirror_path'], b'')

    def test_public_repo_api_url(self):
        """Testing the GitHubEnterprise public repository API URL"""
        url = self._get_repo_api_url(b'public', {b'github_enterprise_public_repo_name': b'testrepo'})
        self.assertEqual(url, b'https://example.com/api/v3/repos/myuser/testrepo')

    def test_public_bug_tracker_field(self):
        """Testing the GitHubEnterprise public repository bug tracker field value"""
        self.assertTrue(self.service_class.get_bug_tracker_requires_username(b'public'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'public', {b'github_enterprise_public_repo_name': b'myrepo', 
           b'hosting_url': b'https://example.com', 
           b'hosting_account_username': b'myuser'}), b'https://example.com/myuser/myrepo/issues#issue/%s')

    def test_public_org_field_values(self):
        """Testing the GitHubEnterprise public-org plan repository field values"""
        fields = self._get_repository_fields(b'Git', plan=b'public-org', with_url=True, fields={b'github_enterprise_public_org_repo_name': b'myrepo', 
           b'github_enterprise_public_org_name': b'myorg', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(fields[b'path'], b'git@example.com:myorg/myrepo.git')
        self.assertEqual(fields[b'mirror_path'], b'')

    def test_public_org_repo_api_url(self):
        """Testing the GitHubEnterprise public-org repository API URL"""
        url = self._get_repo_api_url(b'public-org', {b'github_enterprise_public_org_name': b'myorg', 
           b'github_enterprise_public_org_repo_name': b'testrepo', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(url, b'https://example.com/api/v3/repos/myorg/testrepo')

    def test_public_org_bug_tracker_field(self):
        """Testing the GitHubEnterprise public-org repository bug tracker field value"""
        self.assertFalse(self.service_class.get_bug_tracker_requires_username(b'public-org'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'public-org', {b'github_enterprise_public_org_name': b'myorg', 
           b'github_enterprise_public_org_repo_name': b'myrepo', 
           b'hosting_url': b'https://example.com'}), b'https://example.com/myorg/myrepo/issues#issue/%s')

    def test_private_field_values(self):
        """Testing the GitHubEnterprise private plan repository field values"""
        fields = self._get_repository_fields(b'Git', plan=b'private', with_url=True, fields={b'github_enterprise_private_repo_name': b'myrepo', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(fields[b'path'], b'git@example.com:myuser/myrepo.git')
        self.assertEqual(fields[b'mirror_path'], b'')

    def test_private_repo_api_url(self):
        """Testing the GitHubEnterprise private repository API URL"""
        url = self._get_repo_api_url(b'private', {b'github_enterprise_private_repo_name': b'testrepo', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(url, b'https://example.com/api/v3/repos/myuser/testrepo')

    def test_private_bug_tracker_field(self):
        """Testing the GitHubEnterprise private repository bug tracker field value"""
        self.assertTrue(self.service_class.get_bug_tracker_requires_username(b'private'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'private', {b'github_enterprise_private_repo_name': b'myrepo', 
           b'hosting_account_username': b'myuser', 
           b'hosting_url': b'https://example.com'}), b'https://example.com/myuser/myrepo/issues#issue/%s')

    def test_private_org_field_values(self):
        """Testing the GitHubEnterprise private-org plan repository field values"""
        fields = self._get_repository_fields(b'Git', plan=b'private-org', with_url=True, fields={b'github_enterprise_private_org_repo_name': b'myrepo', 
           b'github_enterprise_private_org_name': b'myorg', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(fields[b'path'], b'git@example.com:myorg/myrepo.git')
        self.assertEqual(fields[b'mirror_path'], b'')

    def test_private_org_repo_api_url(self):
        """Testing the GitHubEnterprise private-org repository API URL"""
        url = self._get_repo_api_url(b'private-org', {b'github_enterprise_private_org_name': b'myorg', 
           b'github_enterprise_private_org_repo_name': b'testrepo', 
           b'hosting_url': b'https://example.com'})
        self.assertEqual(url, b'https://example.com/api/v3/repos/myorg/testrepo')

    def test_private_org_bug_tracker_field(self):
        """Testing the GitHubEnterprise private-org repository bug tracker field value"""
        self.assertFalse(self.service_class.get_bug_tracker_requires_username(b'private-org'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'private-org', {b'github_enterprise_private_org_name': b'myorg', 
           b'github_enterprise_private_org_repo_name': b'myrepo', 
           b'hosting_url': b'https://example.com'}), b'https://example.com/myorg/myrepo/issues#issue/%s')

    def test_authorization(self):
        """Testing that GitHubEnterprise account authorization sends expected data"""
        http_post_data = {}

        def _http_post(self, *args, **kwargs):
            http_post_data[b'args'] = args
            http_post_data[b'kwargs'] = kwargs
            return (
             json.dumps({b'id': 1, 
                b'url': b'https://example.com/api/v3/authorizations/1', 
                b'scopes': [
                          b'user', b'repo'], 
                b'token': b'abc123', 
                b'note': b'', 
                b'note_url': b'', 
                b'updated_at': b'2012-05-04T03:30:00Z', 
                b'created_at': b'2012-05-04T03:30:00Z'}), {})

        self._override_http_method(b'post', _http_post)
        account = HostingServiceAccount(service_name=self.service_name, username=b'myuser', hosting_url=b'https://example.com')
        service = account.service
        self.assertFalse(account.is_authorized)
        service.authorize(b'myuser', b'mypass', b'https://example.com')
        self.assertTrue(account.is_authorized)
        self.assertEqual(http_post_data[b'kwargs'][b'url'], b'https://example.com/api/v3/authorizations')
        self.assertEqual(http_post_data[b'kwargs'][b'username'], b'myuser')
        self.assertEqual(http_post_data[b'kwargs'][b'password'], b'mypass')

    def _get_repo_api_url(self, plan, fields):
        account = self._get_hosting_account(True)
        service = account.service
        self.assertNotEqual(service, None)
        repository = Repository(hosting_account=account)
        repository.extra_data[b'repository_plan'] = plan
        repository.extra_data[b'hosting_url'] = b'https://example.com'
        form = self._get_form(plan, fields)
        form.save(repository)
        return service._get_repo_api_url(repository)

    def _override_http_method(self, name, func):
        from reviewboard.hostingsvcs.github import GitHubClient
        setattr(GitHubClient, b'http_%s' % name, func)