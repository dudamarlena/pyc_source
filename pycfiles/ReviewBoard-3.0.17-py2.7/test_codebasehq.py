# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_codebasehq.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the Codebase HQ hosting service."""
from __future__ import unicode_literals
from django.utils import six
from reviewboard.hostingsvcs.errors import RepositoryError
from reviewboard.hostingsvcs.testing import HostingServiceTestCase
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError

class CodebaseHQTests(HostingServiceTestCase):
    """Unit tests for the Codebase HQ hosting service."""
    service_name = b'codebasehq'
    fixtures = [b'test_scmtools']
    default_account_data = {b'domain': b'mydomain', 
       b'api_key': encrypt_password(b'abc123'), 
       b'password': encrypt_password(HostingServiceTestCase.default_password)}
    default_repository_extra_data = {b'codebasehq_project_name': b'myproj', 
       b'codebasehq_repo_name': b'myrepo'}

    def test_service_support(self):
        """Testing CodebaseHQ service support capabilities"""
        self.assertFalse(self.service_class.supports_post_commit)
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)

    def test_get_repository_fields_for_git(self):
        """Testing CodebaseHQ.get_repository_fields for Git"""
        self.assertEqual(self.get_repository_fields(b'Git', fields={b'codebasehq_project_name': b'myproj', 
           b'codebasehq_repo_name': b'myrepo'}), {b'path': b'git@codebasehq.com:mydomain/myproj/myrepo.git'})

    def test_get_repository_fields_for_mercurial(self):
        """Testing CodebaseHQ.get_repository_fields for Mercurial"""
        self.assertEqual(self.get_repository_fields(b'Mercurial', fields={b'codebasehq_project_name': b'myproj', 
           b'codebasehq_repo_name': b'myrepo'}), {b'path': b'https://mydomain.codebasehq.com/projects/myproj/repositories/myrepo/'})

    def test_get_repository_fields_for_subversion(self):
        """Testing CodebaseHQ.get_repository_fields for Subversion"""
        self.assertEqual(self.get_repository_fields(b'Subversion', fields={b'codebasehq_project_name': b'myproj', 
           b'codebasehq_repo_name': b'myrepo'}), {b'path': b'https://mydomain.codebasehq.com/myproj/myrepo.svn'})

    def test_get_bug_tracker_field(self):
        """Testing CodebaseHQ.get_bug_tracker_field"""
        self.assertEqual(self.service_class.get_bug_tracker_field(None, {b'codebasehq_project_name': b'myproj', 
           b'domain': b'mydomain'}), b'https://mydomain.codebasehq.com/projects/myproj/tickets/%s')
        return

    def test_check_repository_git(self):
        """Testing CodebaseHQ.check_repository for Git"""
        self._test_check_repository(codebase_scm_type=b'git', tool_name=b'Git')

    def test_check_repository_mercurial(self):
        """Testing CodebaseHQ.check_repository for Mercurial"""
        self._test_check_repository(codebase_scm_type=b'hg', tool_name=b'Mercurial')

    def test_check_repository_subversion(self):
        """Testing CodebaseHQ.check_repository for Subversion"""
        self._test_check_repository(codebase_scm_type=b'svn', tool_name=b'Subversion')

    def test_check_repository_with_mismatching_type(self):
        """Testing CodebaseHQ.check_repository with mismatching repository type
        """
        self._test_check_repository(codebase_scm_type=b'svn', tool_name=b'Mercurial', expect_success=False, expected_name_for_error=b'Subversion')

    def test_authorize(self):
        """Testing CodebaseHQ.authorize"""
        hosting_account = self.create_hosting_account(data={})
        with self.setup_http_test(payload=b'{}', hosting_account=hosting_account, expected_http_calls=1) as (ctx):
            self.assertFalse(ctx.service.is_authorized())
            ctx.service.authorize(username=b'myuser', password=b'mypass', credentials={b'domain': b'mydomain', 
               b'api_key': b'abc123'})
        ctx.assertHTTPCall(0, url=b'https://api3.codebasehq.com/users/myuser/public_keys', username=b'mydomain/myuser', password=b'abc123', headers={b'Accept': b'application/xml'})
        self.assertEqual(set(six.iterkeys(hosting_account.data)), {
         b'api_key', b'domain', b'password'})
        self.assertEqual(decrypt_password(hosting_account.data[b'api_key']), b'abc123')
        self.assertEqual(hosting_account.data[b'domain'], b'mydomain')
        self.assertEqual(decrypt_password(hosting_account.data[b'password']), b'mypass')
        self.assertTrue(ctx.service.is_authorized())

    def test_get_file_with_mercurial(self):
        """Testing CodebaseHQ.get_file with Mercurial"""
        self._test_get_file(tool_name=b'Mercurial')

    def test_get_file_with_mercurial_not_found(self):
        """Testing CodebaseHQ.get_file with Mercurial with file not found"""
        self._test_get_file(tool_name=b'Mercurial', file_exists=False)

    def test_get_file_with_git(self):
        """Testing CodebaseHQ.get_file with Git"""
        self._test_get_file(tool_name=b'Git', expect_git_blob_url=True)

    def test_get_file_with_git_not_found(self):
        """Testing CodebaseHQ.get_file with Git with file not found"""
        self._test_get_file(tool_name=b'Git', expect_git_blob_url=True, file_exists=False)

    def test_get_file_with_subversion(self):
        """Testing CodebaseHQ.get_file with Subversion"""
        self._test_get_file(tool_name=b'Subversion')

    def test_get_file_with_subversion_not_found(self):
        """Testing CodebaseHQ.get_file with Subversion with file not found"""
        self._test_get_file(tool_name=b'Subversion', file_exists=False)

    def test_get_file_exists_with_mercurial(self):
        """Testing CodebaseHQ.get_file_exists with Mercurial"""
        self._test_get_file_exists(tool_name=b'Mercurial')

    def test_get_file_exists_with_mercurial_not_found(self):
        """Testing CodebaseHQ.get_file_exists with Mercurial with file not
        found
        """
        self._test_get_file_exists(tool_name=b'Mercurial', file_exists=False)

    def test_get_file_exists_with_git(self):
        """Testing CodebaseHQ.get_file_exists with Git"""
        self._test_get_file_exists(tool_name=b'Git', expect_git_blob_url=True)

    def test_get_file_exists_with_git_not_found(self):
        """Testing CodebaseHQ.get_file_exists with Git with file not found"""
        self._test_get_file_exists(tool_name=b'Git', expect_git_blob_url=True, file_exists=False)

    def test_get_file_exists_with_subversion(self):
        """Testing CodebaseHQ.get_file_exists with Subversion"""
        self._test_get_file_exists(tool_name=b'Subversion')

    def test_get_file_exists_with_subversion_not_found(self):
        """Testing CodebaseHQ.get_file_exists with Subversion with file not
        found
        """
        self._test_get_file_exists(tool_name=b'Subversion', file_exists=False)

    def _test_check_repository(self, codebase_scm_type, tool_name, expect_success=True, expected_name_for_error=None):
        """Test repository checks.

        Args:
            codebase_scm_type (unicode):
                The name of the SCM type in the CodebaseHQ API to return in
                payloads.

            tool_name (unicode):
                The name of the SCM Tool to test with.

            expect_success (bool, optional):
                Whether to simulate a truthy response.

            expected_name_for_error (unicode, optional):
                The name of the SCM Tool to expect in the error response,
                if ``expect_success`` is ``False``.
        """
        payload = (b'<?xml version="1.0" encoding="UTF-8"?>\n<repository>\n <scm>%s</scm>\n</repository>\n' % codebase_scm_type).encode(b'utf-8')
        check_repository_kwargs = {b'codebasehq_project_name': b'myproj', 
           b'codebasehq_repo_name': b'myrepo', 
           b'tool_name': tool_name}
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            if expect_success:
                ctx.service.check_repository(**check_repository_kwargs)
            else:
                message = b"The repository type doesn't match what you selected. Did you mean %s?" % expected_name_for_error
                with self.assertRaisesMessage(RepositoryError, message):
                    ctx.service.check_repository(**check_repository_kwargs)
        ctx.assertHTTPCall(0, url=b'https://api3.codebasehq.com/myproj/myrepo', username=b'mydomain/myuser', password=b'abc123', headers={b'Accept': b'application/xml'})

    def _test_get_file(self, tool_name, expect_git_blob_url=False, file_exists=True):
        """Test file fetching.

        Args:
            tool_name (unicode):
                The name of the SCM Tool to test with.

            expect_git_blob_url (bool, optional):
                Whether to expect a URL referencing a Git blob.

            file_exists (bool, optional):
                Whether to simulate a truthy response.
        """
        if expect_git_blob_url:
            expected_url = b'https://api3.codebasehq.com/myproj/myrepo/blob/123'
        else:
            expected_url = b'https://api3.codebasehq.com/myproj/myrepo/blob/123/myfile'
        if file_exists:
            payload = b'My data\n'
            status_code = None
        else:
            payload = b''
            status_code = 404
        with self.setup_http_test(payload=payload, status_code=status_code, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository(tool_name=tool_name)
            get_file_kwargs = {b'repository': repository, 
               b'path': b'myfile', 
               b'revision': b'123'}
            if file_exists:
                result = ctx.service.get_file(**get_file_kwargs)
                self.assertIsInstance(result, bytes)
                self.assertEqual(result, b'My data\n')
            else:
                with self.assertRaises(FileNotFoundError):
                    ctx.service.get_file(**get_file_kwargs)
        ctx.assertHTTPCall(0, url=expected_url, username=b'mydomain/myuser', password=b'abc123', headers={b'Accept': b'application/xml'})
        return

    def _test_get_file_exists(self, tool_name, expect_git_blob_url=False, file_exists=True):
        """Test file existence checks.

        Args:
            tool_name (unicode):
                The name of the SCM Tool to test with.

            expect_git_blob_url (bool, optional):
                Whether to expect a URL referencing a Git blob.

            file_exists (bool, optional):
                Whether to simulate a truthy response.
        """
        if file_exists:
            payload = b'{"scm": "git"}'
            status_code = None
        else:
            payload = None
            status_code = 404
        with self.setup_http_test(payload=payload, status_code=status_code, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository(tool_name=tool_name)
            result = ctx.service.get_file_exists(repository=repository, path=b'myfile', revision=b'123')
            self.assertEqual(result, file_exists)
        if expect_git_blob_url:
            expected_url = b'https://api3.codebasehq.com/myproj/myrepo/blob/123'
        else:
            expected_url = b'https://api3.codebasehq.com/myproj/myrepo/blob/123/myfile'
        ctx.assertHTTPCall(0, url=expected_url, username=b'mydomain/myuser', password=b'abc123', body=None, headers={b'Accept': b'application/xml'})
        return