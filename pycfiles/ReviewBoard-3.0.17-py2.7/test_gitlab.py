# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_gitlab.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the GitLab hosting service."""
from __future__ import unicode_literals
from reviewboard.hostingsvcs.errors import RepositoryError
from reviewboard.hostingsvcs.gitlab import GitLabAPIVersionError
from reviewboard.hostingsvcs.testing import HostingServiceTestCase
from reviewboard.scmtools.core import Branch, Commit
from reviewboard.scmtools.crypto_utils import encrypt_password

class GitLabTests(HostingServiceTestCase):
    """Unit tests for the GitLab hosting service."""
    service_name = b'gitlab'
    default_use_hosting_url = True
    default_account_data = {b'private_token': encrypt_password(b'abc123')}
    default_repository_extra_data = {b'gitlab_project_id': 123456}

    def test_service_support(self):
        """Testing GitLab service support capabilities"""
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)
        self.assertFalse(self.service_class.supports_ssh_key_association)

    def test_get_repository_fields_with_personal_plan(self):
        """Testing GitLab.get_repository_fields with plan=personal"""
        self.assertEqual(self.get_repository_fields(b'Git', plan=b'personal', fields={b'hosting_url': b'https://example.com', 
           b'gitlab_personal_repo_name': b'myrepo'}), {b'path': b'git@example.com:myuser/myrepo.git', 
           b'mirror_path': b'https://example.com/myuser/myrepo.git'})

    def test_get_repository_fields_with_group_plan(self):
        """Testing GitLab.get_repository_fields with plan=group"""
        self.assertEqual(self.get_repository_fields(b'Git', plan=b'group', fields={b'hosting_url': b'https://example.com', 
           b'gitlab_group_repo_name': b'myrepo', 
           b'gitlab_group_name': b'mygroup'}), {b'path': b'git@example.com:mygroup/myrepo.git', 
           b'mirror_path': b'https://example.com/mygroup/myrepo.git'})

    def test_get_bug_tracker_field_with_personal_plan(self):
        """Testing GitLab.get_bug_tracker_field with plan=personal"""
        self.assertTrue(self.service_class.get_bug_tracker_requires_username(b'personal'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'personal', {b'hosting_url': b'https://example.com', 
           b'gitlab_personal_repo_name': b'myrepo', 
           b'hosting_account_username': b'myuser'}), b'https://example.com/myuser/myrepo/issues/%s')

    def test_get_bug_tracker_field_with_group_plan(self):
        """Testing GitLab.get_bug_tracker_field with plan=group"""
        self.assertFalse(self.service_class.get_bug_tracker_requires_username(b'group'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'group', {b'hosting_url': b'https://example.com', 
           b'gitlab_group_name': b'mygroup', 
           b'gitlab_group_repo_name': b'myrepo'}), b'https://example.com/mygroup/myrepo/issues/%s')

    def test_check_repository_personal_v3(self):
        """Testing GitLab.check_repository with personal repository (API v3)"""
        ctx = self._test_check_repository_v3(plan=b'personal', gitlab_personal_repo_name=b'myrepo', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v3/projects?per_page=100', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_personal_v4(self):
        """Testing GitLab.check_repository with personal repository (API v4)"""
        ctx = self._test_check_repository_v4(plan=b'personal', gitlab_personal_repo_name=b'myrepo', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects/myuser%2Fmyrepo', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_group_v3(self):
        """Testing GitLab.check_repository with group repository (API v3)"""
        ctx = self._test_check_repository_v3(plan=b'group', gitlab_group_name=b'mygroup', gitlab_group_repo_name=b'myrepo', expected_owner=b'mygroup', expected_http_calls=2)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v3/groups?per_page=100', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        ctx.assertHTTPCall(1, url=b'https://example.com/api/v3/groups/1', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_group_v4(self):
        """Testing GitLab.check_repository with group repository (API v4)"""
        ctx = self._test_check_repository_v4(plan=b'group', gitlab_group_name=b'mygroup', gitlab_group_repo_name=b'myrepo', expected_owner=b'mygroup', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects/mygroup%2Fmyrepo', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_personal_not_found_v4(self):
        """Testing GitLab.check_repository with not found error and personal
        repository (API v4)
        """
        ctx = self._test_check_repository_error_v4(plan=b'personal', gitlab_personal_repo_name=b'myrepo', expected_error=b'A repository with this name was not found, or your user may not own it.', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects/myuser%2Fmyrepo', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_group_repo_not_found_v4(self):
        """Testing GitLab.check_repository with not found error and
        group repository (API v4)
        """
        ctx = self._test_check_repository_error_v4(plan=b'group', gitlab_group_name=b'mygroup', gitlab_group_repo_name=b'badrepo', expected_error=b'A repository with this name was not found, or your user may not own it.', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects/mygroup%2Fbadrepo', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_personal_not_found_v3(self):
        """Testing GitLab.check_repository with not found error and personal
        repository (API v3)
        """
        ctx = self._test_check_repository_error_v3(plan=b'personal', gitlab_personal_repo_name=b'myrepo', expected_error=b'A repository with this name was not found, or your user may not own it.', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v3/projects?per_page=100', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_group_repo_not_found_v3(self):
        """Testing GitLab.check_repository with not found error and
        group repository (API v3)
        """
        ctx = self._test_check_repository_error_v3(plan=b'group', gitlab_group_name=b'mygroup', gitlab_group_repo_name=b'badrepo', expected_error=b'A repository with this name was not found on this group, or your user may not have access to it.', expected_http_calls=2)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v3/groups?per_page=100', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        ctx.assertHTTPCall(1, url=b'https://example.com/api/v3/groups/1', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_check_repository_group_not_found_v3(self):
        """Testing GitLab.check_repository with an incorrect group name (API
        v3)
        """
        ctx = self._test_check_repository_error_v3(plan=b'group', gitlab_group_name=b'badgroup', gitlab_group_repo_name=b'myrepo', expected_error=b'A group with this name was not found, or your user may not have access to it.', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v3/groups?per_page=100', username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        return

    def test_authorize_v4(self):
        """Testing GitLab.authorize (API v4)"""
        ctx = self._test_check_authorize(payload=b'{}', expected_http_calls=1)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects?per_page=1', username=None, password=None, headers={b'PRIVATE-TOKEN': b'foobarbaz'})
        return

    def test_authorize_v3(self):
        """Testing GitLab.authorize (API v3)"""
        paths = {b'/api/v4/projects': {b'status_code': 404}, 
           b'/api/v3/projects': {b'payload': b'{}'}}
        ctx = self._test_check_authorize(self.make_handler_for_paths(paths), expected_http_calls=2)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects?per_page=1', username=None, password=None, headers={b'PRIVATE-TOKEN': b'foobarbaz'})
        ctx.assertHTTPCall(1, url=b'https://example.com/api/v3/projects?per_page=1', username=None, password=None, headers={b'PRIVATE-TOKEN': b'foobarbaz'})
        return

    def test_authorize_with_api_version_not_found(self):
        """Testing GitLab.authorize (API version not found)"""
        hosting_account = self.create_hosting_account(data={})
        self.assertFalse(hosting_account.is_authorized)
        message = b'Could not determine the GitLab API version for https://example.com due to an unexpected error (Unexpected path "/api/v4/projects"). Check to make sure the URL can be resolved from this server and that any SSL certificates are valid and trusted.'
        with self.setup_http_test(self.make_handler_for_paths({}), hosting_account=hosting_account) as (ctx):
            with self.assertRaisesMessage(GitLabAPIVersionError, message):
                ctx.service.authorize(b'myuser', credentials={b'username': b'myuser', 
                   b'private_token': b'foobarbaz'}, hosting_url=b'https://example.com')
        self.assertFalse(hosting_account.is_authorized)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects?per_page=1', username=None, password=None, headers={b'PRIVATE-TOKEN': b'foobarbaz'})
        ctx.assertHTTPCall(1, url=b'https://example.com/api/v3/projects?per_page=1', username=None, password=None, headers={b'PRIVATE-TOKEN': b'foobarbaz'})
        return

    def test_get_branches_v4(self):
        """Testing GitLab.get_branches (API v4)"""
        self._test_get_branches(api_version=b'4')

    def test_get_branches_v3(self):
        """Testing GitLab.get_branches (API v3)"""
        self._test_get_branches(api_version=b'3')

    def test_get_commits_v4(self):
        """Testing GitLab.get_commits (API v4)"""
        self._test_get_commits(api_version=b'4')

    def test_get_commits_v3(self):
        """Testing GitLab.get_commits (API v3)"""
        self._test_get_commits(api_version=b'3')

    def test_get_change_v4(self):
        """Testing GitLab.get_change (API v4)"""
        self._test_get_change(api_version=b'4')

    def test_get_change_v3(self):
        """Testing GitLab.get_change (API v3)"""
        self._test_get_change(api_version=b'3')

    def test_get_file_v4(self):
        """Testing GitLab.get_file (API v4)"""
        self._test_get_file(api_version=b'4', expected_url=b'https://example.com/api/v4/projects/123456/repository/blobs/676502b42383c746ed899a2f4b50b4370feeea94/raw')

    def test_get_file_with_base_commit_v3(self):
        """Testing GitLab.get_file with base commit ID (API v3)"""
        self._test_get_file(api_version=b'3', base_commit_id=b'ed899a2f4b50b4370feeea94676502b42383c746', expected_url=b'https://example.com/api/v3/projects/123456/repository/blobs/ed899a2f4b50b4370feeea94676502b42383c746?filepath=path/to/file.txt')

    def test_get_file_without_base_commit_v3(self):
        """Testing GitLab.get_file without base commit ID (API v3)"""
        self._test_get_file(api_version=b'3', expected_url=b'https://example.com/api/v3/projects/123456/repository/raw_blobs/676502b42383c746ed899a2f4b50b4370feeea94')

    def test_get_file_exists_with_exists_v4(self):
        """Testing GitLab.get_file_exists with exists (API v4)"""
        self._test_get_file_exists(api_version=b'4', should_exist=True, expected_url=b'https://example.com/api/v4/projects/123456/repository/blobs/676502b42383c746ed899a2f4b50b4370feeea94/raw')

    def test_get_file_exists_with_not_exists_v4(self):
        """Testing GitLab.get_file_exists with not exists (API v4)"""
        self._test_get_file_exists(api_version=b'4', should_exist=False, expected_url=b'https://example.com/api/v4/projects/123456/repository/blobs/676502b42383c746ed899a2f4b50b4370feeea94/raw')

    def test_get_file_exists_with_base_commit_and_exists_v3(self):
        """Testing GitLab.get_file_exists with base commit ID and exists
        (API v3)
        """
        self._test_get_file_exists(api_version=b'3', should_exist=True, base_commit_id=b'ed899a2f4b50b4370feeea94676502b42383c746', expected_url=b'https://example.com/api/v3/projects/123456/repository/blobs/ed899a2f4b50b4370feeea94676502b42383c746?filepath=path/to/file.txt')

    def test_get_file_exists_without_base_commit_and_exists_v3(self):
        """Testing GitLab.get_file_exists without base commit ID and with
        exists
        (API v3)
        """
        self._test_get_file_exists(api_version=b'3', should_exist=True, expected_url=b'https://example.com/api/v3/projects/123456/repository/raw_blobs/676502b42383c746ed899a2f4b50b4370feeea94')

    def test_get_file_exists_with_not_exists_v3(self):
        """Testing GitLab.get_file_exists with not exists (API v3)"""
        self._test_get_file_exists(api_version=b'3', should_exist=False, expected_url=b'https://example.com/api/v3/projects/123456/repository/raw_blobs/676502b42383c746ed899a2f4b50b4370feeea94')

    def _test_check_authorize(self, *args, **kwargs):
        """Test authorizing a new account.

        Args:
            *args (tuple):
                Positional arguments for the HTTP test.

            **kwargs (dict):
                Keyword arguments for the HTTP test.

        Returns:
            reviewboard.hostingsvcs.testing.testcases.HttpTestContext:
            The context used for this test.
        """
        hosting_account = self.create_hosting_account(data={})
        self.assertFalse(hosting_account.is_authorized)
        with self.setup_http_test(hosting_account=hosting_account, *args, **kwargs) as (ctx):
            ctx.service.authorize(b'myuser', credentials={b'username': b'myuser', 
               b'private_token': b'foobarbaz'}, hosting_url=b'https://example.com')
        self.assertTrue(hosting_account.is_authorized)
        return ctx

    def _test_check_repository_v4(self, expected_owner=b'myuser', **kwargs):
        """Test checking for a repository using API v4.

        Args:
            expected_owner (unicode):
                The expected user/group name owning the repository.

            **kwargs (dict):
                Keyword arguments to pass to
                :py:meth:`check_repository()
                <reviewboard.hostingsvcs.gitlab.GitLab.check_repository>`.

        Returns:
            reviewboard.hostingsvcs.testing.testcases.HttpTestContext:
            The context used for this test.
        """
        with self.setup_http_test(payload=b'{"id": 12345}') as (ctx):
            self._set_api_version(ctx.service, b'4')
            ctx.service.check_repository(**kwargs)
        return ctx

    def _test_check_repository_v3(self, expected_owner=b'myuser', **kwargs):
        """Test checking for a repository using API v3.

        Args:
            expected_owner (unicode):
                The expected user/group name owning the repository.

            **kwargs (dict):
                Keyword arguments to pass to
                :py:meth:`check_repository()
                <reviewboard.hostingsvcs.gitlab.GitLab.check_repository>`.

        Returns:
            reviewboard.hostingsvcs.testing.testcases.HttpTestContext:
            The context used for this test.
        """
        paths = {b'/api/v3/projects': {b'payload': self.dump_json([
                                            {b'id': 1, 
                                               b'path': b'myrepo', 
                                               b'namespace': {b'path': expected_owner}}])}, 
           b'/api/v3/groups': {b'payload': self.dump_json([
                                          {b'id': 1, 
                                             b'name': b'mygroup'}])}, 
           b'/api/v3/groups/1': {b'payload': self.dump_json({b'projects': [
                                                          {b'id': 1, 
                                                             b'name': b'myrepo'}]})}}
        with self.setup_http_test(self.make_handler_for_paths(paths)) as (ctx):
            self._set_api_version(ctx.service, b'3')
            ctx.service.check_repository(**kwargs)
        return ctx

    def _test_check_repository_error_v4(self, expected_error, expected_http_calls, **kwargs):
        """Test error conditions when checking for a repository using API v4.

        Args:
            expected_error (unicode):
                The expected error message from a raised exception.

            expected_http_calls (int):
                The number of expected HTTP calls.

            **kwargs (dict):
                Keyword arguments to pass to
                :py:meth:`check_repository()
                <reviewboard.hostingsvcs.gitlab.GitLab.check_repository>`.

        Returns:
            reviewboard.hostingsvcs.testing.testcases.HttpTestContext:
            The context used for this test.
        """
        with self.setup_http_test(expected_http_calls=expected_http_calls, status_code=404) as (ctx):
            with self.assertRaisesMessage(RepositoryError, expected_error):
                self._set_api_version(ctx.service, b'4')
                ctx.service.check_repository(**kwargs)
        return ctx

    def _test_check_repository_error_v3(self, expected_error, expected_http_calls, **kwargs):
        """Test error conditions when checking for a repository using API v3.

        Args:
            expected_error (unicode):
                The expected error message from a raised exception.

            expected_http_calls (int):
                The number of expected HTTP calls.

            **kwargs (dict):
                Keyword arguments to pass to
                :py:meth:`check_repository()
                <reviewboard.hostingsvcs.gitlab.GitLab.check_repository>`.

        Returns:
            reviewboard.hostingsvcs.testing.testcases.HttpTestContext:
            The context used for this test.
        """
        paths = {b'/api/v3/groups': {b'payload': self.dump_json([
                                          {b'id': 1, 
                                             b'name': b'mygroup'}])}, 
           b'/api/v3/projects': {b'payload': self.dump_json([])}, 
           b'/api/v3/groups/1': {b'payload': self.dump_json({b'projects': [
                                                          {b'id': 1, 
                                                             b'name': b'myrepo'}]})}}
        with self.setup_http_test(self.make_handler_for_paths(paths), expected_http_calls=expected_http_calls) as (ctx):
            self._set_api_version(ctx.service, b'3')
            with self.assertRaisesMessage(RepositoryError, expected_error):
                ctx.service.check_repository(**kwargs)
        return ctx

    def test_check_repository_with_api_version_not_found(self):
        """Testing GitLab.check_repository (API version not found)"""
        hosting_account = self.create_hosting_account(data={})
        self.assertFalse(hosting_account.is_authorized)
        message = b'Could not determine the GitLab API version for https://example.com due to an unexpected error (Unexpected path "/api/v4/projects"). Check to make sure the URL can be resolved from this server and that any SSL certificates are valid and trusted.'
        with self.setup_http_test(self.make_handler_for_paths({}), hosting_account=hosting_account) as (ctx):
            with self.assertRaisesMessage(GitLabAPIVersionError, message):
                ctx.service.check_repository(plan=b'group', gitlab_group_name=b'mygroup', gitlab_group_repo_name=b'myrepo')
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v4/projects?per_page=1', username=None, password=None, headers={})
        ctx.assertHTTPCall(1, url=b'https://example.com/api/v3/projects?per_page=1', username=None, password=None, headers={})
        return

    def _test_get_file(self, api_version, expected_url, base_commit_id=None):
        """Common test for file retrieval.

        Args:
            api_version (unicode):
                The API version to test against.

            expected_url (unicode):
                The expected URL to fetch for the request.

            base_commit_id (unicode, optional):
                An optional base commit ID to specify during file retrieval.
        """
        with self.setup_http_test(payload=b'test data', expected_http_calls=1) as (ctx):
            self._set_api_version(ctx.service, api_version)
            repository = ctx.create_repository()
            data = ctx.service.get_file(repository=repository, path=b'path/to/file.txt', revision=b'676502b42383c746ed899a2f4b50b4370feeea94', base_commit_id=base_commit_id)
        self.assertIsInstance(data, bytes)
        self.assertEqual(data, b'test data')
        ctx.assertHTTPCall(0, url=expected_url, username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        return

    def _test_get_file_exists(self, api_version, should_exist, expected_url, base_commit_id=None):
        """Common test for file existence checks.

        Args:
            api_version (unicode):
                The API version to test against.

            should_exist (bool):
                Whether this should simulate that the file exists.

            expected_url (unicode):
                The expected URL to fetch for the request.

            base_commit_id (unicode, optional):
                An optional base commit ID to specify during file existence
                checks.
        """
        if should_exist:
            test_kwargs = {b'payload': b'test data'}
        else:
            test_kwargs = {b'status_code': 400}
        with self.setup_http_test(expected_http_calls=1, **test_kwargs) as (ctx):
            self._set_api_version(ctx.service, api_version)
            repository = ctx.create_repository()
            result = ctx.service.get_file_exists(repository=repository, path=b'path/to/file.txt', revision=b'676502b42383c746ed899a2f4b50b4370feeea94', base_commit_id=base_commit_id)
        self.assertEqual(result, should_exist)
        ctx.assertHTTPCall(0, url=expected_url, username=None, password=None, headers={b'PRIVATE-TOKEN': b'abc123'})
        return

    def _test_get_branches(self, api_version):
        """Common test for fetching branches.

        Args:
            api_version (unicode):
                The API version to test against.
        """
        payload = self.dump_json([
         {b'name': b'master', 
            b'commit': {b'id': b'ed899a2f4b50b4370feeea94676502b42383c746'}},
         {b'name': b'branch1', 
            b'commit': {b'id': b'6104942438c14ec7bd21c6cd5bd995272b3faff6'}},
         {b'name': b'branch2', 
            b'commit': {b'id': b'21b3bcabcff2ab3dc3c9caa172f783aad602c0b0'}},
         {b'branch-name': b'branch3', 
            b'commit': {b'id': b'd5a3ff139356ce33e37e73add446f16869741b50'}}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            self._set_api_version(ctx.service, api_version)
            repository = ctx.create_repository()
            branches = ctx.service.get_branches(repository)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v%s/projects/123456/repository/branches' % api_version, username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        self.assertEqual(branches, [
         Branch(id=b'master', commit=b'ed899a2f4b50b4370feeea94676502b42383c746', default=True),
         Branch(id=b'branch1', commit=b'6104942438c14ec7bd21c6cd5bd995272b3faff6', default=False),
         Branch(id=b'branch2', commit=b'21b3bcabcff2ab3dc3c9caa172f783aad602c0b0', default=False)])
        return

    def _test_get_commits(self, api_version):
        """Common test for fetching lists of commits.

        Args:
            api_version (unicode):
                The API version to test against.
        """
        payload = self.dump_json([
         {b'id': b'ed899a2f4b50b4370feeea94676502b42383c746', 
            b'author_name': b'Chester Li', 
            b'created_at': b'2015-03-10T11:50:22+03:00', 
            b'message': b'Replace sanitize with escape once'},
         {b'id': b'6104942438c14ec7bd21c6cd5bd995272b3faff6', 
            b'author_name': b'Chester Li', 
            b'created_at': b'2015-03-10T09:06:12+03:00', 
            b'message': b'Sanitize for network graph'},
         {b'id': b'21b3bcabcff2ab3dc3c9caa172f783aad602c0b0', 
            b'author_name': b'East Coast', 
            b'created_at': b'2015-03-04T15:31:18.000-04:00', 
            b'message': b'Add a timer to test file'}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            self._set_api_version(ctx.service, api_version)
            repository = ctx.create_repository()
            commits = ctx.service.get_commits(repository=repository, start=b'ed899a2f4b50b4370feeea94676502b42383c746')
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v%s/projects/123456/repository/commits?per_page=21&ref_name=ed899a2f4b50b4370feeea94676502b42383c746' % api_version, username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        self.assertEqual(commits, [
         Commit(author_name=b'Chester Li', date=b'2015-03-10T11:50:22+03:00', id=b'ed899a2f4b50b4370feeea94676502b42383c746', message=b'Replace sanitize with escape once', parent=b'6104942438c14ec7bd21c6cd5bd995272b3faff6'),
         Commit(author_name=b'Chester Li', date=b'2015-03-10T09:06:12+03:00', id=b'6104942438c14ec7bd21c6cd5bd995272b3faff6', message=b'Sanitize for network graph', parent=b'21b3bcabcff2ab3dc3c9caa172f783aad602c0b0'),
         Commit(author_name=b'East Coast', date=b'2015-03-04T15:31:18.000-04:00', id=b'21b3bcabcff2ab3dc3c9caa172f783aad602c0b0', message=b'Add a timer to test file', parent=b'')])
        for commit in commits:
            self.assertIsNone(commit.diff)

        return

    def _test_get_change(self, api_version):
        """Common test for fetching individual commits.

        Args:
            api_version (unicode):
                The API version to test against.
        """
        commit_sha = b'ed899a2f4b50b4370feeea94676502b42383c746'
        diff_rsp = b'---\nf1 | 1 +\nf2 | 1 +\n2 files changed, 2 insertions(+), 0 deletions(-)\n\ndiff --git a/f1 b/f1\nindex 11ac561..3ea0691 100644\n--- a/f1\n+++ b/f1\n@@ -1 +1,2 @@\n this is f1\n+add one line to f1\ndiff --git a/f2 b/f2\nindex c837441..9302ecd 100644\n--- a/f2\n+++ b/f2\n@@ -1 +1,2 @@\n this is f2\n+add one line to f2 with Unicode❶\n'
        paths = {b'/api/v%s/projects/123456/repository/commits/%s' % (api_version, commit_sha): {b'payload': self.dump_json({b'author_name': b'Chester Li', 
                                                                                                        b'id': commit_sha, 
                                                                                                        b'created_at': b'2015-03-10T11:50:22+03:00', 
                                                                                                        b'message': b'Replace sanitize with escape once', 
                                                                                                        b'parent_ids': [
                                                                                                                      b'ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba']})}, 
           b'/api/v%s/projects/123456' % api_version: {b'payload': self.dump_json({b'path_with_namespace': b'myuser/myproject'})}, 
           b'/myuser/myproject/commit/%s.diff' % commit_sha: {b'payload': diff_rsp}}
        with self.setup_http_test(self.make_handler_for_paths(paths), expected_http_calls=3) as (ctx):
            self._set_api_version(ctx.service, api_version)
            repository = ctx.create_repository()
            commit = ctx.service.get_change(repository=repository, revision=commit_sha)
        ctx.assertHTTPCall(0, url=b'https://example.com/api/v%s/projects/123456/repository/commits/%s' % (
         api_version, commit_sha), username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        ctx.assertHTTPCall(1, url=b'https://example.com/api/v%s/projects/123456?private_token=abc123' % api_version, username=None, password=None, headers={b'Accept': b'application/json', 
           b'PRIVATE-TOKEN': b'abc123'})
        ctx.assertHTTPCall(2, url=b'https://example.com/myuser/myproject/commit/%s.diff?private_token=abc123' % commit_sha, username=None, password=None, headers={b'Accept': b'text/plain'})
        self.assertEqual(commit, Commit(author_name=b'Chester Li', date=b'2015-03-10T11:50:22+03:00', id=commit_sha, message=b'Replace sanitize with escape once', parent=b'ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba'))
        self.assertEqual(commit.diff, diff_rsp)
        return

    def _set_api_version(self, service, api_version):
        """Set the API version for a test.

        Args:
            service (reviewboard.hostingsvcs.gitlab.GitLab):
                The GitLab hosting service instance.

            api_version (unicode):
                The API version for the test.
        """
        self.spy_on(service._get_api_version, call_fake=lambda self, hosting_url: api_version)