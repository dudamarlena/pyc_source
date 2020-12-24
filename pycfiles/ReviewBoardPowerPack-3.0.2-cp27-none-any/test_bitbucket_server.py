# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/tests/test_bitbucket_server.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import get_hosting_service, register_hosting_service, unregister_hosting_service
from reviewboard.scmtools.crypto_utils import decrypt_password
from reviewboard.scmtools.models import Repository
from rbpowerpack.hostingsvcs.bitbucket_server import BitbucketServer
from rbpowerpack.hostingsvcs.tests.testcases import ServiceTests

class BitbucketServerTests(ServiceTests):
    """Unit tests for the BitbucketServer hosting service."""
    service_name = b'bitbucket-server'

    def setUp(self):
        register_hosting_service(self.service_name, BitbucketServer)
        self.service_class = get_hosting_service(self.service_name)
        super(BitbucketServerTests, self).setUp()

    def tearDown(self):
        super(BitbucketServerTests, self).tearDown()
        unregister_hosting_service(self.service_name)

    def test_service_support(self):
        """Testing BitbucketServer service support capabilities"""
        self.assertFalse(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)
        self.assertFalse(self.service_class.supports_post_commit)

    def test_authorize(self):
        """Testing BitbucketServer.authorize"""
        account = HostingServiceAccount(service_name=self.service_name, hosting_url=b'https://localhost:7990/', username=b'myuser')
        self.spy_on(account.service._api_get, call_original=False)
        self.assertFalse(account.is_authorized)
        account.service.authorize(b'myuser', b'mypass', b'https://localhost:7990/')
        self.assertTrue(account.is_authorized)
        self.assertTrue(account.service._api_get.called_with(b'https://localhost:7990/rest/api/1.0/application-properties'))
        self.assertIn(b'password', account.data)
        self.assertEqual(decrypt_password(account.data[b'password']), b'mypass')

    def test_project_field_values(self):
        """Testing BitbucketServer project repository form values"""
        fields = self._get_repository_fields(b'Git', plan=b'project', with_url=True, fields={b'bitbucket_server_project_key': b'Project Name', 
           b'bitbucket_server_project_repo_name': b'Repo Name'})
        self.assertEqual(fields[b'path'], b'https://example.com/scm/project-name/repo-name.git')
        self.assertNotIn(b'mirror_path', fields)

    def test_personal_field_values(self):
        """Testing BitbucketServer personal repository form values"""
        fields = self._get_repository_fields(b'Git', plan=b'personal', with_url=True, fields={b'bitbucket_server_personal_repo_owner': b'User Name', 
           b'bitbucket_server_personal_repo_name': b'Repo Name'})
        self.assertEqual(fields[b'path'], b'https://example.com/scm/~user-name/repo-name.git')
        self.assertNotIn(b'mirror_path', fields)

    def test_project_api_paths(self):
        """Testing BitbucketServer project repository raw file path"""
        account = self._get_hosting_account(True)
        service = account.service
        self.assertNotEqual(service, None)
        plan = b'project'
        form = self._get_form(plan, fields={b'bitbucket_server_project_key': b'Project Name', 
           b'bitbucket_server_project_repo_name': b'Repo Name'})
        repository = Repository(hosting_account=account)
        repository.extra_data[b'repository_plan'] = plan
        repository.extra_data[b'hosting_url'] = b'https://example.com'
        form.save(repository)
        self.spy_on(service._api_get, call_original=False)
        service.get_file(repository, b'x/y/z.py', b'123456780', base_commit_id=b'1234567890')
        self.assertEqual(service._api_get.last_call.args, ('https://example.com/projects/project-name/repos/repo-name/raw/x/y/z.py?at=1234567890', ))
        return

    def test_personal_api_paths(self):
        """Testing BitbucketServer personal repository raw file path"""
        account = self._get_hosting_account(True)
        service = account.service
        self.assertNotEqual(service, None)
        plan = b'personal'
        form = self._get_form(plan, fields={b'bitbucket_server_personal_repo_owner': b'User Name', 
           b'bitbucket_server_personal_repo_name': b'Repo Name'})
        repository = Repository(hosting_account=account)
        repository.extra_data[b'repository_plan'] = plan
        repository.extra_data[b'hosting_url'] = b'https://example.com'
        form.save(repository)
        self.spy_on(service._api_get, call_original=False)
        service.get_file(repository, b'x/y/z.py', b'123456780', base_commit_id=b'1234567890')
        self.assertEqual(service._api_get.last_call.args, ('https://example.com/users/user-name/repos/repo-name/raw/x/y/z.py?at=1234567890', ))
        return