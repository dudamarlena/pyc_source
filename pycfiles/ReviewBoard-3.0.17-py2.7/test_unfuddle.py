# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_unfuddle.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the Unfuddle hosting service."""
from __future__ import unicode_literals
from django.utils.six.moves.urllib.error import HTTPError
from reviewboard.hostingsvcs.errors import RepositoryError
from reviewboard.hostingsvcs.testing import HostingServiceTestCase
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError

class UnfuddleTests(HostingServiceTestCase):
    """Unit tests for the Unfuddle hosting service."""
    service_name = b'unfuddle'
    fixtures = [b'test_scmtools']
    default_account_data = {b'password': encrypt_password(HostingServiceTestCase.default_password)}
    default_repository_extra_data = {b'unfuddle_account_domain': b'mydomain', 
       b'unfuddle_project_id': 1, 
       b'unfuddle_repo_id': 2, 
       b'unfuddle_repo_name': b'myrepo'}

    def test_service_support(self):
        """Testing Unfuddle service support capabilities"""
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)

    def test_get_repository_fields_with_git(self):
        """Testing Unfuddle.get_repository_fields for Git"""
        self.assertEqual(self.get_repository_fields(b'Git', fields={b'unfuddle_account_domain': b'mydomain', 
           b'unfuddle_project_id': 1, 
           b'unfuddle_repo_name': b'myrepo'}), {b'path': b'git@mydomain.unfuddle.com:mydomain/myrepo.git', 
           b'mirror_path': b'https://mydomain.unfuddle.com/git/mydomain_myrepo/'})

    def test_get_repository_fields_with_subversion(self):
        """Testing Unfuddle.get_repository_fields for Subversion"""
        self.assertEqual(self.get_repository_fields(b'Subversion', fields={b'unfuddle_account_domain': b'mydomain', 
           b'unfuddle_project_id': 1, 
           b'unfuddle_repo_name': b'myrepo'}), {b'path': b'https://mydomain.unfuddle.com/svn/mydomain_myrepo', 
           b'mirror_path': b'http://mydomain.unfuddle.com/svn/mydomain_myrepo'})

    def test_authorize(self):
        """Testing Unfuddle.authorize"""
        hosting_account = self.create_hosting_account(data={})
        with self.setup_http_test(payload=b'{}', hosting_account=hosting_account, expected_http_calls=1) as (ctx):
            self.assertFalse(ctx.service.is_authorized())
            ctx.service.authorize(username=b'myuser', password=b'abc123', unfuddle_account_domain=b'mydomain')
        ctx.assertHTTPCall(0, url=b'https://mydomain.unfuddle.com/api/v1/account/', username=b'myuser', password=b'abc123', headers={b'Accept': b'application/json'})
        self.assertIn(b'password', hosting_account.data)
        self.assertNotEqual(hosting_account.data[b'password'], b'abc123')
        self.assertEqual(decrypt_password(hosting_account.data[b'password']), b'abc123')
        self.assertTrue(ctx.service.is_authorized())

    def test_check_repository(self):
        """Testing Unfuddle.check_repository"""
        payload = self.dump_json([
         {b'id': 2, 
            b'abbreviation': b'myrepo', 
            b'system': b'git'}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            ctx.service.check_repository(unfuddle_account_domain=b'mydomain', unfuddle_repo_name=b'myrepo', tool_name=b'Git')
        ctx.assertHTTPCall(0, url=b'https://mydomain.unfuddle.com/api/v1/repositories/', headers={b'Accept': b'application/json'})

    def test_check_repository_with_wrong_repo_type(self):
        """Testing Unfuddle.check_repository with wrong repo type"""
        payload = self.dump_json([
         {b'id': 2, 
            b'abbreviation': b'myrepo', 
            b'system': b'svn'}])
        expected_message = b'A repository with this name was not found'
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            with self.assertRaisesMessage(RepositoryError, expected_message):
                ctx.service.check_repository(unfuddle_account_domain=b'mydomain', unfuddle_repo_name=b'myrepo', tool_name=b'Git')
        ctx.assertHTTPCall(0, url=b'https://mydomain.unfuddle.com/api/v1/repositories/', headers={b'Accept': b'application/json'})

    def test_get_file_with_svn_and_base_commit_id(self):
        """Testing Unfuddle.get_file with Subversion and base commit ID"""
        self._test_get_file(tool_name=b'Subversion', revision=b'123', base_commit_id=b'456', expected_revision=b'456')

    def test_get_file_with_svn_and_revision(self):
        """Testing Unfuddle.get_file with Subversion and revision"""
        self._test_get_file(tool_name=b'Subversion', revision=b'123', base_commit_id=None, expected_revision=b'123')
        return

    def test_get_file_with_git_and_base_commit_id(self):
        """Testing Unfuddle.get_file with Git and revision with base commit ID
        """
        self._test_get_file(tool_name=b'Git', revision=b'123', base_commit_id=b'456', expected_revision=b'456')

    def test_get_file_with_git_and_revision(self):
        """Testing Unfuddle.get_file with Git and revision without base commit
        ID
        """
        self._test_get_file(tool_name=b'Git', revision=b'123', base_commit_id=None, expected_revision=None, expected_error=True)
        return

    def test_get_file_exists_with_svn_and_base_commit_id(self):
        """Testing Unfuddle.get_file_exists with Subversion and base commit ID
        """
        self._test_get_file_exists(tool_name=b'Subversion', revision=b'123', base_commit_id=b'456', expected_revision=b'456', expected_found=True)

    def test_get_file_exists_with_svn_and_revision(self):
        """Testing Unfuddle.get_file_exists with Subversion and revision"""
        self._test_get_file_exists(tool_name=b'Subversion', revision=b'123', base_commit_id=None, expected_revision=b'123', expected_found=True)
        return

    def test_get_file_exists_with_svn_and_revision_not_found(self):
        """Testing Unfuddle.get_file_exists with Subversion and revision not
        found
        """
        self._test_get_file_exists(tool_name=b'Subversion', revision=b'123', base_commit_id=None, expected_revision=b'123', expected_found=False)
        return

    def test_get_file_exists_with_git_and_base_commit_id(self):
        """Testing Unfuddle.get_file_exists with Git and revision with base
        commit ID
        """
        self._test_get_file_exists(tool_name=b'Git', revision=b'123', base_commit_id=b'456', expected_revision=b'456', expected_found=True)

    def test_get_file_exists_with_git_and_revision_no_base_commit_id(self):
        """Testing Unfuddle.get_file_exists with Git and revision without
        base commit ID
        """
        self._test_get_file_exists(tool_name=b'Git', revision=b'123', base_commit_id=None, expected_revision=None, expected_found=False, expected_error=True)
        return

    def test_get_file_exists_with_git_and_revision_not_found(self):
        """Testing Unfuddle.get_file_exists with Git and revision not found"""
        self._test_get_file_exists(tool_name=b'Git', revision=b'123', base_commit_id=b'456', expected_revision=b'456', expected_found=False)

    def _test_get_file(self, tool_name, revision, base_commit_id, expected_revision, expected_error=False):
        """Common function for testing file fetching.

        Args:
            tool_name (unicode):
                The registered name of the SCMTool.

            revision (unicode):
                The revision to fetch.

            base_commit_id (unicode):
                The ID the commit is based on.

            expected_revision (unicode):
                The expected revision to find in the URL.

            expected_error (bool, optional):
                Whether this test expects the file existence check to return
                an error.
        """
        if expected_error:
            expected_http_calls = 0
        else:
            expected_http_calls = 1
        with self.setup_http_test(expected_http_calls=expected_http_calls, payload=b'My data') as (ctx):
            repository = ctx.create_repository(tool_name=tool_name)
            get_file_kwargs = {b'repository': repository, 
               b'path': b'/path', 
               b'revision': revision, 
               b'base_commit_id': base_commit_id}
            if expected_error:
                with self.assertRaises(FileNotFoundError):
                    ctx.service.get_file(**get_file_kwargs)
                result = None
            else:
                result = ctx.service.get_file(**get_file_kwargs)
        if not expected_error:
            ctx.assertHTTPCall(0, url=b'https://mydomain.unfuddle.com/api/v1/repositories/2/download/?path=/path&commit=%s' % expected_revision, headers={b'Accept': b'application/json'})
            self.assertIsInstance(result, bytes)
            self.assertEqual(result, b'My data')
        return

    def _test_get_file_exists(self, tool_name, revision, base_commit_id, expected_revision, expected_found=True, expected_error=False):
        """Common function for testing file existence checks.

        Args:
            tool_name (unicode):
                The registered name of the SCMTool.

            revision (unicode):
                The revision to fetch.

            base_commit_id (unicode):
                The ID the commit is based on.

            expected_revision (unicode):
                The expected revision to find in the URL.

            expected_found (bool, optional):
                Whether this test expects the check to indicate the file
                exists.

            expected_error (bool, optional):
                Whether this test expects the file existence check to return
                an error.
        """
        if expected_found:
            payload = b'{}'
            status_code = None
        else:
            payload = None
            status_code = 404
        if expected_error:
            expected_http_calls = 0
        else:
            expected_http_calls = 1
        with self.setup_http_test(expected_http_calls=expected_http_calls, payload=payload, status_code=status_code) as (ctx):
            repository = ctx.create_repository(tool_name=tool_name)
            result = ctx.service.get_file_exists(repository=repository, path=b'/path', revision=revision, base_commit_id=base_commit_id)
        if expected_error:
            self.assertEqual(len(ctx.http_calls), 0)
            self.assertFalse(result)
        else:
            ctx.assertHTTPCall(0, url=b'https://mydomain.unfuddle.com/api/v1/repositories/2/history/?path=/path&commit=%s&count=0' % expected_revision, headers={b'Accept': b'application/json'})
            if expected_found:
                self.assertTrue(result)
            else:
                self.assertTrue(ctx.http_calls[0].raised(HTTPError))
                self.assertFalse(result)
        return