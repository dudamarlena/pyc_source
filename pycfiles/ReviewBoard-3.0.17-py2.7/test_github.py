# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_github.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the GitHub hosting service."""
from __future__ import unicode_literals
import hashlib, hmac, logging, uuid
from django.core.exceptions import ObjectDoesNotExist
from djblets.testing.decorators import add_fixtures
from reviewboard.scmtools.core import Branch, Commit
from reviewboard.hostingsvcs.errors import RepositoryError
from reviewboard.hostingsvcs.repository import RemoteRepository
from reviewboard.hostingsvcs.testing import HostingServiceTestCase
from reviewboard.reviews.models import ReviewRequest
from reviewboard.scmtools.errors import SCMError
from reviewboard.site.models import LocalSite
from reviewboard.site.urlresolvers import local_site_reverse

class GitHubTestCase(HostingServiceTestCase):
    """Base class for GitHub test suites."""
    service_name = b'github'
    default_account_data = {b'authorization': {b'token': b'abc123'}}
    default_repository_extra_data = {b'repository_plan': b'public', 
       b'github_public_repo_name': b'myrepo'}


class GitHubTests(GitHubTestCase):
    """Unit tests for the GitHub hosting service."""

    def test_service_support(self):
        """Testing GitHub service support capabilities"""
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)
        self.assertFalse(self.service_class.supports_ssh_key_association)

    def test_get_repository_fields_with_public_plan(self):
        """Testing GitHub.get_repository_fields with the public plan"""
        self.assertEqual(self.get_repository_fields(b'Git', plan=b'public', fields={b'github_public_repo_name': b'myrepo'}), {b'path': b'git://github.com/myuser/myrepo.git', 
           b'mirror_path': b'git@github.com:myuser/myrepo.git'})

    def test_get_repository_fields_with_public_org_plan(self):
        """Testing GitHub.get_repository_fields with the public-org plan"""
        self.assertEqual(self.get_repository_fields(b'Git', plan=b'public-org', fields={b'github_public_org_repo_name': b'myrepo', 
           b'github_public_org_name': b'myorg'}), {b'path': b'git://github.com/myorg/myrepo.git', 
           b'mirror_path': b'git@github.com:myorg/myrepo.git'})

    def test_get_repository_fields_with_private_plan(self):
        """Testing GitHub.get_repository_fields with the private plan"""
        self.assertEqual(self.get_repository_fields(b'Git', plan=b'private', fields={b'github_private_repo_name': b'myrepo'}), {b'path': b'git@github.com:myuser/myrepo.git', 
           b'mirror_path': b''})

    def test_get_repository_fields_with_private_org_plan(self):
        """Testing GitHub.get_repository_fields with the private-org plan"""
        self.assertEqual(self.get_repository_fields(b'Git', plan=b'private-org', fields={b'github_private_org_repo_name': b'myrepo', 
           b'github_private_org_name': b'myorg'}), {b'path': b'git@github.com:myorg/myrepo.git', 
           b'mirror_path': b''})

    def test_get_repo_api_url_with_public_plan(self):
        """Testing GitHub._get_repo_api_url with the public plan"""
        url = self._get_repo_api_url(b'public', {b'github_public_repo_name': b'testrepo'})
        self.assertEqual(url, b'https://api.github.com/repos/myuser/testrepo')

    def test_get_repo_api_url_with_public_org_plan(self):
        """Testing GitHub._get_repo_api_url with the public-org plan"""
        url = self._get_repo_api_url(b'public-org', {b'github_public_org_name': b'myorg', 
           b'github_public_org_repo_name': b'testrepo'})
        self.assertEqual(url, b'https://api.github.com/repos/myorg/testrepo')

    def test_get_repo_api_url_with_private_plan(self):
        """Testing GitHub._get_repo_api_url with the private plan"""
        url = self._get_repo_api_url(b'private', {b'github_private_repo_name': b'testrepo'})
        self.assertEqual(url, b'https://api.github.com/repos/myuser/testrepo')

    def test_get_repo_api_url_with_private_org_plan(self):
        """Testing GitHub._get_repo_api_url with the private-org plan"""
        url = self._get_repo_api_url(b'private-org', {b'github_private_org_name': b'myorg', 
           b'github_private_org_repo_name': b'testrepo'})
        self.assertEqual(url, b'https://api.github.com/repos/myorg/testrepo')

    def test_get_bug_tracker_field_with_public_plan(self):
        """Testing GitHub.get_bug_tracker_field with the public plan"""
        self.assertTrue(self.service_class.get_bug_tracker_requires_username(b'public'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'public', {b'github_public_repo_name': b'myrepo', 
           b'hosting_account_username': b'myuser'}), b'http://github.com/myuser/myrepo/issues#issue/%s')

    def test_get_bug_tracker_field_with_public_org_plan(self):
        """Testing GitHub.get_bug_tracker_field with the public-org plan"""
        self.assertFalse(self.service_class.get_bug_tracker_requires_username(b'public-org'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'public-org', {b'github_public_org_name': b'myorg', 
           b'github_public_org_repo_name': b'myrepo'}), b'http://github.com/myorg/myrepo/issues#issue/%s')

    def test_get_bug_tracker_field_with_private_plan(self):
        """Testing GitHub.get_bug_tracker_field with the private plan"""
        self.assertTrue(self.service_class.get_bug_tracker_requires_username(b'private'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'private', {b'github_private_repo_name': b'myrepo', 
           b'hosting_account_username': b'myuser'}), b'http://github.com/myuser/myrepo/issues#issue/%s')

    def test_get_bug_tracker_field_with_private_org_plan(self):
        """Testing GitHub.get_bug_tracker_field with the private-org plan"""
        self.assertFalse(self.service_class.get_bug_tracker_requires_username(b'private-org'))
        self.assertEqual(self.service_class.get_bug_tracker_field(b'private-org', {b'github_private_org_name': b'myorg', 
           b'github_private_org_repo_name': b'myrepo'}), b'http://github.com/myorg/myrepo/issues#issue/%s')

    def test_check_repository_public(self):
        """Testing GitHub.check_repository with public repository"""
        self._test_check_repository(plan=b'public', github_public_repo_name=b'myrepo')

    def test_check_repository_private(self):
        """Testing GitHub.check_repository with private repository"""
        self._test_check_repository(plan=b'private', github_private_repo_name=b'myrepo')

    def test_check_repository_public_org(self):
        """Testing GitHub.check_repository with public org repository"""
        self._test_check_repository(plan=b'public-org', github_public_org_name=b'myorg', github_public_org_repo_name=b'myrepo', expected_owner=b'myorg')

    def test_check_repository_private_org(self):
        """Testing GitHub.check_repository with private org repository"""
        self._test_check_repository(plan=b'private-org', github_private_org_name=b'myorg', github_private_org_repo_name=b'myrepo', expected_owner=b'myorg')

    def test_check_repository_public_not_found(self):
        """Testing GitHub.check_repository with not found error and public
        repository
        """
        self._test_check_repository_error(plan=b'public', github_public_repo_name=b'myrepo', http_status=404, payload=b'{"message": "Not Found"}', expected_url=b'https://api.github.com/repos/myuser/myrepo', expected_error=b'A repository with this name was not found, or your user may not own it.')

    def test_check_repository_private_not_found(self):
        """Testing GitHub.check_repository with not found error and private
        repository
        """
        self._test_check_repository_error(plan=b'private', github_private_repo_name=b'myrepo', http_status=404, payload=b'{"message": "Not Found"}', expected_url=b'https://api.github.com/repos/myuser/myrepo', expected_error=b'A repository with this name was not found, or your user may not own it.')

    def test_check_repository_public_org_not_found(self):
        """Testing GitHub.check_repository with not found error and
        public organization repository
        """
        self._test_check_repository_error(plan=b'public-org', github_public_org_name=b'myorg', github_public_org_repo_name=b'myrepo', http_status=404, payload=b'{"message": "Not Found"}', expected_url=b'https://api.github.com/repos/myorg/myrepo', expected_error=b'A repository with this organization or name was not found.')

    def test_check_repository_private_org_not_found(self):
        """Testing GitHub.check_repository with not found error and
        private organization repository
        """
        self._test_check_repository_error(plan=b'private-org', github_private_org_name=b'myorg', github_private_org_repo_name=b'myrepo', http_status=404, payload=b'{"message": "Not Found"}', expected_url=b'https://api.github.com/repos/myorg/myrepo', expected_error=b'A repository with this organization or name was not found, or your user may not have access to it.')

    def test_check_repository_public_plan_private_repo(self):
        """Testing GitHub.check_repository with public plan and
        private repository
        """
        self._test_check_repository_error(plan=b'public', github_public_repo_name=b'myrepo', http_status=200, payload=b'{"private": true}', expected_url=b'https://api.github.com/repos/myuser/myrepo', expected_error=b'This is a private repository, but you have selected a public plan.')

    def test_check_repository_private_plan_public_repo(self):
        """Testing GitHub.check_repository with private plan and
        public repository
        """
        self._test_check_repository_error(plan=b'private', github_private_repo_name=b'myrepo', http_status=200, payload=b'{"private": false}', expected_url=b'https://api.github.com/repos/myuser/myrepo', expected_error=b'This is a public repository, but you have selected a private plan.')

    def test_check_repository_public_org_plan_private_repo(self):
        """Testing GitHub.check_repository with public organization plan and
        private repository
        """
        self._test_check_repository_error(plan=b'public-org', github_public_org_name=b'myorg', github_public_org_repo_name=b'myrepo', http_status=200, payload=b'{"private": true}', expected_url=b'https://api.github.com/repos/myorg/myrepo', expected_error=b'This is a private repository, but you have selected a public plan.')

    def test_check_repository_private_org_plan_public_repo(self):
        """Testing GitHub.check_repository with private organization plan and
        public repository
        """
        self._test_check_repository_error(plan=b'private-org', github_private_org_name=b'myorg', github_private_org_repo_name=b'myrepo', http_status=200, payload=b'{"private": false}', expected_url=b'https://api.github.com/repos/myorg/myrepo', expected_error=b'This is a public repository, but you have selected a private plan.')

    def test_authorization(self):
        """Testing GitHub.authorize"""
        payload = self.dump_json({b'id': 1, 
           b'url': b'https://api.github.com/authorizations/1', 
           b'scopes': [
                     b'user', b'repo'], 
           b'token': b'abc123', 
           b'note': b'', 
           b'note_url': b'', 
           b'updated_at': b'2012-05-04T03:30:00Z', 
           b'created_at': b'2012-05-04T03:30:00Z'})
        hosting_account = self.create_hosting_account(data={})
        self.assertFalse(hosting_account.is_authorized)
        self.spy_on(uuid.uuid4, call_fake=lambda : uuid.UUID(b'2a707f8c6fc14dd590e545ebe1e9b2f6'))
        with self.setup_http_test(payload=payload, hosting_account=hosting_account, expected_http_calls=1) as (ctx):
            with self.settings(GITHUB_CLIENT_ID=None, GITHUB_CLIENT_SECRET=None):
                ctx.service.authorize(username=b'myuser', password=b'mypass')
        self.assertTrue(hosting_account.is_authorized)
        ctx.assertHTTPCall(0, url=b'https://api.github.com/authorizations', method=b'POST', username=b'myuser', password=b'mypass', body=b'{"note": "Access for Review Board (example.com/ - 2a707f8)", "note_url": "http://example.com/", "scopes": ["user", "repo"]}', headers={b'Content-Length': b'123'})
        return

    def test_authorization_with_client_info(self):
        """Testing GitHub.authorize with registered client ID/secret"""
        payload = self.dump_json({b'id': 1, 
           b'url': b'https://api.github.com/authorizations/1', 
           b'scopes': [
                     b'user', b'repo'], 
           b'token': b'abc123', 
           b'note': b'', 
           b'note_url': b'', 
           b'updated_at': b'2012-05-04T03:30:00Z', 
           b'created_at': b'2012-05-04T03:30:00Z'})
        hosting_account = self.create_hosting_account(data={})
        self.assertFalse(hosting_account.is_authorized)
        self.spy_on(uuid.uuid4, call_fake=lambda : uuid.UUID(b'2a707f8c6fc14dd590e545ebe1e9b2f6'))
        with self.setup_http_test(payload=payload, hosting_account=hosting_account, expected_http_calls=1) as (ctx):
            with self.settings(GITHUB_CLIENT_ID=b'abc123', GITHUB_CLIENT_SECRET=b'def456'):
                ctx.service.authorize(username=b'myuser', password=b'mypass')
        self.assertTrue(hosting_account.is_authorized)
        ctx.assertHTTPCall(0, url=b'https://api.github.com/authorizations', method=b'POST', username=b'myuser', password=b'mypass', body=b'{"client_id": "abc123", "client_secret": "def456", "note": "Access for Review Board (example.com/ - 2a707f8)", "note_url": "http://example.com/", "scopes": ["user", "repo"]}', headers={b'Content-Length': b'173'})

    def test_get_branches(self):
        """Testing GitHub.get_branches"""
        payload = self.dump_json([
         {b'ref': b'refs/heads/master', 
            b'object': {b'sha': b'859d4e148ce3ce60bbda6622cdbe5c2c2f8d9817'}},
         {b'ref': b'refs/heads/release-1.7.x', 
            b'object': {b'sha': b'92463764015ef463b4b6d1a1825fee7aeec8cb15'}},
         {b'ref': b'refs/heads/some-component/fix', 
            b'object': {b'sha': b'764015ef492c8cb1546363b45fee7ab6d1a182ee'}},
         {b'ref': b'refs/tags/release-1.7.11', 
            b'object': {b'sha': b'f5a35f1d8a8dcefb336a8e3211334f1f50ea7792'}}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository()
            branches = ctx.service.get_branches(repository)
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/myuser/myrepo/git/refs/heads', username=b'myuser', password=b'abc123')
        self.assertEqual(branches, [
         Branch(id=b'master', commit=b'859d4e148ce3ce60bbda6622cdbe5c2c2f8d9817', default=True),
         Branch(id=b'release-1.7.x', commit=b'92463764015ef463b4b6d1a1825fee7aeec8cb15', default=False),
         Branch(id=b'some-component/fix', commit=b'764015ef492c8cb1546363b45fee7ab6d1a182ee', default=False)])

    def test_get_commits(self):
        """Testing GitHub.get_commits"""
        payload = self.dump_json([
         {b'commit': {b'author': {b'name': b'Christian Hammond'}, b'committer': {b'date': b'2013-06-25T23:31:22Z'}, b'message': b'Fixed the bug number for the blacktriangledown bug.'}, 
            b'sha': b'859d4e148ce3ce60bbda6622cdbe5c2c2f8d9817', 
            b'parents': [{b'sha': b'92463764015ef463b4b6d1a1825fee7aeec8cb15'}]},
         {b'commit': {b'author': {b'name': b'Christian Hammond'}, b'committer': {b'date': b'2013-06-25T23:30:59Z'}, b'message': b"Merge branch 'release-1.7.x'"}, 
            b'sha': b'92463764015ef463b4b6d1a1825fee7aeec8cb15', 
            b'parents': [{b'sha': b'f5a35f1d8a8dcefb336a8e3211334f1f50ea7792'}, {b'sha': b'6c5f3465da5ed03dca8128bb3dd03121bd2cddb2'}]},
         {b'commit': {b'author': {b'name': b'David Trowbridge'}, b'committer': {b'date': b'2013-06-25T22:41:09Z'}, b'message': b'Add DIFF_PARSE_ERROR to the ValidateDiffResource.create error list.'}, 
            b'sha': b'f5a35f1d8a8dcefb336a8e3211334f1f50ea7792', 
            b'parents': []}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            repository = ctx.create_repository()
            commits = ctx.service.get_commits(repository=repository, start=b'859d4e148ce3ce60bbda6622cdbe5c2c2f8d9817')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/myuser/myrepo/commits?sha=859d4e148ce3ce60bbda6622cdbe5c2c2f8d9817', username=b'myuser', password=b'abc123')
        self.assertEqual(commits, [
         Commit(author_name=b'Christian Hammond', date=b'2013-06-25T23:31:22Z', id=b'859d4e148ce3ce60bbda6622cdbe5c2c2f8d9817', message=b'Fixed the bug number for the blacktriangledown bug.', parent=b'92463764015ef463b4b6d1a1825fee7aeec8cb15'),
         Commit(author_name=b'Christian Hammond', date=b'2013-06-25T23:30:59Z', id=b'92463764015ef463b4b6d1a1825fee7aeec8cb15', message=b"Merge branch 'release-1.7.x'", parent=b'f5a35f1d8a8dcefb336a8e3211334f1f50ea7792'),
         Commit(author_name=b'David Trowbridge', date=b'2013-06-25T22:41:09Z', id=b'f5a35f1d8a8dcefb336a8e3211334f1f50ea7792', message=b'Add DIFF_PARSE_ERROR to the ValidateDiffResource.create error list.', parent=b'')])
        for commit in commits:
            self.assertIsNone(commit.diff)

    def test_get_change(self):
        """Testing GitHub.get_change"""
        commit_sha = b'1c44b461cebe5874a857c51a4a13a849a4d1e52d'
        parent_sha = b'44568f7d33647d286691517e6325fea5c7a21d5e'
        tree_sha = b'56e25e58380daf9b4dfe35677ae6043fe1743922'
        paths = {b'/repos/myuser/myrepo/commits': {b'payload': self.dump_json([
                                                        {b'commit': {b'author': {b'name': b'David Trowbridge'}, b'committer': {b'date': b'2013-06-25T23:31:22Z'}, b'message': b'Move .clearfix to defs.less'}, 
                                                           b'sha': commit_sha, 
                                                           b'parents': [{b'sha': parent_sha}]}])}, 
           b'/repos/myuser/myrepo/compare/%s...%s' % (parent_sha, commit_sha): {b'payload': self.dump_json({b'base_commit': {b'commit': {b'tree': {b'sha': tree_sha}}}, b'files': [
                                                                                                      {b'sha': b'4344b3ad41b171ea606e88e9665c34cca602affb', 
                                                                                                         b'filename': b'reviewboard/static/rb/css/defs.less', 
                                                                                                         b'status': b'modified', 
                                                                                                         b'patch': b'@@ -182,4 +182,6 @@\n }\n \n+.foo {\n+}\n \n table {'},
                                                                                                      {b'sha': b'8e3129277b018b169cb8d13771433fbcd165a17c', 
                                                                                                         b'filename': b'reviewboard/static/rb/css/reviews.less', 
                                                                                                         b'status': b'modified', 
                                                                                                         b'patch': b'@@ -1311,6 +1311,4 @@\n }\n \n-.bar {\n-}\n \n h1 {'},
                                                                                                      {b'sha': b'17ba0791499db908433b80f37c5fbc89b870084b', 
                                                                                                         b'filename': b'new_filename', 
                                                                                                         b'previous_filename': b'old_filename', 
                                                                                                         b'status': b'renamed', 
                                                                                                         b'patch': b'@@ -1,1 +1,1 @@\n- foo\n+ bar'}]})}, 
           b'/repos/myuser/myrepo/git/trees/%s' % tree_sha: {b'payload': self.dump_json({b'tree': [
                                                                                  {b'path': b'reviewboard/static/rb/css/defs.less', 
                                                                                     b'sha': b'830a40c3197223c6a0abb3355ea48891a1857bfd'},
                                                                                  {b'path': b'reviewboard/static/rb/css/reviews.less', 
                                                                                     b'sha': b'535cd2c4211038d1bb8ab6beaed504e0db9d7e62'},
                                                                                  {b'path': b'old_filename', 
                                                                                     b'sha': b'356a192b7913b04c54574d18c28d46e6395428ab'}]})}}
        with self.setup_http_test(self.make_handler_for_paths(paths), expected_http_calls=3) as (ctx):
            repository = ctx.create_repository()
            change = ctx.service.get_change(repository=repository, revision=commit_sha)
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/myuser/myrepo/commits?sha=1c44b461cebe5874a857c51a4a13a849a4d1e52d', username=b'myuser', password=b'abc123')
        ctx.assertHTTPCall(1, url=b'https://api.github.com/repos/myuser/myrepo/compare/44568f7d33647d286691517e6325fea5c7a21d5e...1c44b461cebe5874a857c51a4a13a849a4d1e52d', username=b'myuser', password=b'abc123')
        ctx.assertHTTPCall(2, url=b'https://api.github.com/repos/myuser/myrepo/git/trees/56e25e58380daf9b4dfe35677ae6043fe1743922?recursive=1', username=b'myuser', password=b'abc123')
        self.assertEqual(change, Commit(author_name=b'David Trowbridge', date=b'2013-06-25T23:31:22Z', id=b'1c44b461cebe5874a857c51a4a13a849a4d1e52d', message=b'Move .clearfix to defs.less', parent=b'44568f7d33647d286691517e6325fea5c7a21d5e'))
        self.assertEqual(change.diff, b'diff --git a/reviewboard/static/rb/css/defs.less b/reviewboard/static/rb/css/defs.less\nindex 830a40c3197223c6a0abb3355ea48891a1857bfd..4344b3ad41b171ea606e88e9665c34cca602affb 100644\n--- a/reviewboard/static/rb/css/defs.less\n+++ b/reviewboard/static/rb/css/defs.less\n@@ -182,4 +182,6 @@\n }\n \n+.foo {\n+}\n \n table {\ndiff --git a/reviewboard/static/rb/css/reviews.less b/reviewboard/static/rb/css/reviews.less\nindex 535cd2c4211038d1bb8ab6beaed504e0db9d7e62..8e3129277b018b169cb8d13771433fbcd165a17c 100644\n--- a/reviewboard/static/rb/css/reviews.less\n+++ b/reviewboard/static/rb/css/reviews.less\n@@ -1311,6 +1311,4 @@\n }\n \n-.bar {\n-}\n \n h1 {\ndiff --git a/new_filename b/new_filename\nrename from old_filename\nrename to new_filename\nindex 356a192b7913b04c54574d18c28d46e6395428ab..17ba0791499db908433b80f37c5fbc89b870084b\n--- a/old_filename\n+++ b/new_filename\n@@ -1,1 +1,1 @@\n- foo\n+ bar\n')

    def test_get_change_with_not_found(self):
        """Testing GitHub.get_change with commit not found"""
        with self.setup_http_test(status_code=404, payload=b'{"message": "Not Found"}', expected_http_calls=1) as (ctx):
            with self.assertRaisesMessage(SCMError, b'Not Found'):
                repository = ctx.create_repository()
                ctx.service.get_change(repository=repository, revision=b'1c44b461cebe5874a857c51a4a13a849a4d1e52d')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/myuser/myrepo/commits?sha=1c44b461cebe5874a857c51a4a13a849a4d1e52d', username=b'myuser', password=b'abc123')

    def test_get_remote_repositories_with_owner(self):
        """Testing GitHub.get_remote_repositories with requesting
        authenticated user's repositories
        """
        base_url = b'https://api.github.com/user/repos'
        paths = {b'/user/repos': {b'payload': self.dump_json([
                                       {b'id': 1, 
                                          b'owner': {b'login': b'myuser'}, 
                                          b'name': b'myrepo', 
                                          b'clone_url': b'myrepo_path', 
                                          b'mirror_url': b'myrepo_mirror', 
                                          b'private': b'false'}]), 
                            b'headers': {b'Link': b'<%s?page=2>; rel="next"' % base_url}}, 
           b'/user/repos?page=2': {b'payload': self.dump_json([
                                              {b'id': 2, 
                                                 b'owner': {b'login': b'myuser'}, 
                                                 b'name': b'myrepo2', 
                                                 b'clone_url': b'myrepo_path2', 
                                                 b'mirror_url': b'myrepo_mirror2', 
                                                 b'private': b'true'}]), 
                                   b'headers': {b'Link': b'<%s?page=1>; rel="prev"' % base_url}}}
        with self.setup_http_test(self.make_handler_for_paths(paths), expected_http_calls=1) as (ctx):
            paginator = ctx.service.get_remote_repositories(b'myuser')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/user/repos', username=b'myuser', password=b'abc123')
        self.assertEqual(len(paginator.page_data), 1)
        self.assertFalse(paginator.has_prev)
        self.assertTrue(paginator.has_next)
        repo = paginator.page_data[0]
        self.assertIsInstance(repo, RemoteRepository)
        self.assertEqual(repo.id, b'myuser/myrepo')
        self.assertEqual(repo.owner, b'myuser')
        self.assertEqual(repo.name, b'myrepo')
        self.assertEqual(repo.scm_type, b'Git')
        self.assertEqual(repo.path, b'myrepo_path')
        self.assertEqual(repo.mirror_path, b'myrepo_mirror')
        paginator.next()
        ctx.assertHTTPCall(1, url=b'https://api.github.com/user/repos?page=2', username=b'myuser', password=b'abc123')
        self.assertEqual(len(paginator.page_data), 1)
        self.assertTrue(paginator.has_prev)
        self.assertFalse(paginator.has_next)
        repo = paginator.page_data[0]
        self.assertIsInstance(repo, RemoteRepository)
        self.assertEqual(repo.id, b'myuser/myrepo2')
        self.assertEqual(repo.owner, b'myuser')
        self.assertEqual(repo.name, b'myrepo2')
        self.assertEqual(repo.scm_type, b'Git')
        self.assertEqual(repo.path, b'myrepo_path2')
        self.assertEqual(repo.mirror_path, b'myrepo_mirror2')

    def test_get_remote_repositories_with_other_user(self):
        """Testing GitHub.get_remote_repositories with requesting user's
        repositories
        """
        repos1 = self.dump_json([
         {b'id': 1, 
            b'owner': {b'login': b'other'}, 
            b'name': b'myrepo', 
            b'clone_url': b'myrepo_path', 
            b'mirror_url': b'myrepo_mirror', 
            b'private': b'false'}])
        headers = {b'Link': b'<https://api.github.com/users/other/repos?page=2>; rel="next"'}
        with self.setup_http_test(payload=repos1, headers=headers, expected_http_calls=1) as (ctx):
            paginator = ctx.service.get_remote_repositories(b'other')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/users/other/repos', username=b'myuser', password=b'abc123')
        self.assertEqual(len(paginator.page_data), 1)
        public_repo = paginator.page_data[0]
        self.assertIsInstance(public_repo, RemoteRepository)
        self.assertEqual(public_repo.id, b'other/myrepo')
        self.assertEqual(public_repo.owner, b'other')
        self.assertEqual(public_repo.name, b'myrepo')
        self.assertEqual(public_repo.scm_type, b'Git')
        self.assertEqual(public_repo.path, b'myrepo_path')
        self.assertEqual(public_repo.mirror_path, b'myrepo_mirror')

    def test_get_remote_repositories_with_org(self):
        """Testing GitHub.get_remote_repositories with requesting
        organization's repositories
        """
        payload = self.dump_json([
         {b'id': 1, 
            b'owner': {b'login': b'myorg'}, 
            b'name': b'myrepo', 
            b'clone_url': b'myrepo_path', 
            b'mirror_url': b'myrepo_mirror', 
            b'private': b'false'},
         {b'id': 2, 
            b'owner': {b'login': b'myuser'}, 
            b'name': b'myrepo2', 
            b'clone_url': b'myrepo_path2', 
            b'mirror_url': b'myrepo_mirror2', 
            b'private': b'true'}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            paginator = ctx.service.get_remote_repositories(b'myorg', b'organization')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/orgs/myorg/repos', username=b'myuser', password=b'abc123')
        self.assertEqual(len(paginator.page_data), 2)
        public_repo, private_repo = paginator.page_data
        self.assertIsInstance(public_repo, RemoteRepository)
        self.assertEqual(public_repo.id, b'myorg/myrepo')
        self.assertEqual(public_repo.owner, b'myorg')
        self.assertEqual(public_repo.name, b'myrepo')
        self.assertEqual(public_repo.scm_type, b'Git')
        self.assertEqual(public_repo.path, b'myrepo_path')
        self.assertEqual(public_repo.mirror_path, b'myrepo_mirror')
        self.assertIsInstance(private_repo, RemoteRepository)
        self.assertEqual(private_repo.id, b'myuser/myrepo2')
        self.assertEqual(private_repo.owner, b'myuser')
        self.assertEqual(private_repo.name, b'myrepo2')
        self.assertEqual(private_repo.scm_type, b'Git')
        self.assertEqual(private_repo.path, b'myrepo_path2')
        self.assertEqual(private_repo.mirror_path, b'myrepo_mirror2')

    def test_get_remote_repositories_with_defaults(self):
        """Testing GitHub.get_remote_repositories with default values"""
        with self.setup_http_test(payload=b'{}', expected_http_calls=1) as (ctx):
            ctx.service.get_remote_repositories()
        ctx.assertHTTPCall(0, url=b'https://api.github.com/user/repos', username=b'myuser', password=b'abc123')

    def test_get_remote_repositories_with_filter(self):
        """Testing GitHub.get_remote_repositories with ?filter-type="""
        with self.setup_http_test(payload=b'[]', expected_http_calls=1) as (ctx):
            ctx.service.get_remote_repositories(b'myuser', filter_type=b'private')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/user/repos?type=private', username=b'myuser', password=b'abc123')

    def test_get_remote_repository(self):
        """Testing GitHub.get_remote_repository"""
        payload = self.dump_json({b'id': 1, 
           b'owner': {b'login': b'myuser'}, 
           b'name': b'myrepo', 
           b'clone_url': b'myrepo_path', 
           b'mirror_url': b'myrepo_mirror', 
           b'private': b'false'})
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            remote_repository = ctx.service.get_remote_repository(b'myuser/myrepo')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/myuser/myrepo', username=b'myuser', password=b'abc123')
        self.assertIsInstance(remote_repository, RemoteRepository)
        self.assertEqual(remote_repository.id, b'myuser/myrepo')
        self.assertEqual(remote_repository.owner, b'myuser')
        self.assertEqual(remote_repository.name, b'myrepo')
        self.assertEqual(remote_repository.scm_type, b'Git')
        self.assertEqual(remote_repository.path, b'myrepo_path')
        self.assertEqual(remote_repository.mirror_path, b'myrepo_mirror')

    def test_get_remote_repository_invalid(self):
        """Testing GitHub.get_remote_repository with invalid repository ID"""
        with self.setup_http_test(status_code=404, payload=b'{"message": "Not Found"}', expected_http_calls=1) as (ctx):
            with self.assertRaises(ObjectDoesNotExist):
                ctx.service.get_remote_repository(b'myuser/invalid')
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/myuser/invalid', username=b'myuser', password=b'abc123')

    def _test_check_repository(self, expected_owner=b'myuser', **kwargs):
        """Test checking for a repository.

        Args:
            expected_owner (unicode):
                The expected owner of the repository.

            **kwargs (dict):
                Keyword arguments to pass to
                :py:meth:`check_repository()
                <reviewboard.hostingsvcs.gitlab.GitLab.check_repository>`.
        """
        with self.setup_http_test(payload=b'{}', expected_http_calls=1) as (ctx):
            ctx.service.check_repository(**kwargs)
        ctx.assertHTTPCall(0, url=b'https://api.github.com/repos/%s/myrepo' % expected_owner, username=b'myuser', password=b'abc123')

    def _test_check_repository_error(self, http_status, payload, expected_url, expected_error, **kwargs):
        """Test error conditions when checking for a repository.

        Args:
            http_status (int):
                The HTTP status to simulate returning.

            payload (bytes):
                The payload to return, if ``http_status`` is 200.

            expected_url (unicode):
                The expected URL accessed (minus any query strings).

            expected_error (unicode):
                The expected error message from a raised exception.

            **kwargs (dict):
                Keyword arguments to pass to
                :py:meth:`check_repository()
                <reviewboard.hostingsvcs.gitlab.GitLab.check_repository>`.
        """
        if http_status != 200:
            payload = b'{"message": "not Found"}'
        with self.setup_http_test(status_code=http_status, payload=payload, expected_http_calls=1) as (ctx):
            with self.assertRaisesMessage(RepositoryError, expected_error):
                ctx.service.check_repository(**kwargs)
        ctx.assertHTTPCall(0, url=expected_url, username=b'myuser', password=b'abc123')

    def _get_repo_api_url(self, plan, fields):
        """Return the base API URL for a repository.

        Args:
            plan (unicode):
                The name of the plan.

            fields (dict):
                Fields containing repository information.

        Returns:
            unicode:
            The API URL for the repository.
        """
        account = self.create_hosting_account()
        repository = self.create_repository(hosting_account=account, extra_data={b'repository_plan': plan})
        form = self.get_form(plan, fields)
        form.save(repository)
        return account.service._get_repo_api_url(repository)


class CloseSubmittedHookTests(GitHubTestCase):
    """Unit tests for the GitHub close-submitted webhook."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_close_submitted_hook(self):
        """Testing GitHub close_submitted hook with event=push"""
        self._test_post_commit_hook()

    @add_fixtures([b'test_site'])
    def test_close_submitted_hook_with_local_site(self):
        """Testing GitHub close_submitted hook with event=push and using a
        Local Site
        """
        self._test_post_commit_hook(LocalSite.objects.get(name=self.local_site_name))

    @add_fixtures([b'test_site'])
    def test_close_submitted_hook_with_unpublished_review_request(self):
        """Testing GitHub close_submitted hook with event=push and an
        un-published review request
        """
        self._test_post_commit_hook(publish=False)

    def test_close_submitted_hook_ping(self):
        """Testing GitHub close_submitted hook with event=ping"""
        account = self.create_hosting_account()
        repository = self.create_repository(hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), secret=repository.get_or_create_hooks_uuid(), event=b'ping')
        self.assertEqual(response.status_code, 200)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)

    def test_close_submitted_hook_with_invalid_repo(self):
        """Testing GitHub close_submitted hook with event=push and invalid
        repository
        """
        repository = self.create_repository()
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), secret=repository.get_or_create_hooks_uuid())
        self.assertEqual(response.status_code, 404)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)

    def test_close_submitted_hook_with_invalid_site(self):
        """Testing GitHub close_submitted hook with event=push and invalid
        Local Site
        """
        account = self.create_hosting_account()
        repository = self.create_repository(hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', local_site_name=b'badsite', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), secret=repository.get_or_create_hooks_uuid())
        self.assertEqual(response.status_code, 404)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)

    def test_close_submitted_hook_with_invalid_service_id(self):
        """Testing GitHub close_submitted hook with event=push and invalid
        hosting service ID
        """
        account = self.create_hosting_account()
        account.service_name = b'bitbucket'
        account.save()
        repository = self.create_repository(hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), secret=repository.get_or_create_hooks_uuid())
        self.assertEqual(response.status_code, 404)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)

    def test_close_submitted_hook_with_invalid_event(self):
        """Testing GitHub close_submitted hook with invalid event"""
        account = self.create_hosting_account()
        repository = self.create_repository(hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), secret=repository.get_or_create_hooks_uuid(), event=b'foo')
        self.assertEqual(response.status_code, 400)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)

    def test_close_submitted_hook_with_invalid_signature(self):
        """Testing GitHub close_submitted hook with invalid signature"""
        account = self.create_hosting_account()
        repository = self.create_repository(hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url, secret=b'bad-secret')
        self.assertEqual(response.status_code, 400)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)

    def test_close_submitted_hook_with_invalid_review_requests(self):
        """Testing GitHub close_submitted hook with event=push and invalid
        review requests
        """
        self.spy_on(logging.error)
        account = self.create_hosting_account()
        repository = self.create_repository(hosting_account=account)
        review_request = self.create_review_request(repository=repository, publish=True)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=b'/r/9999/', secret=repository.get_or_create_hooks_uuid())
        self.assertEqual(response.status_code, 200)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        self.assertEqual(review_request.changedescs.count(), 0)
        self.assertTrue(logging.error.called_with(b'close_all_review_requests: Review request #%s does not exist.', 9999))

    def _test_post_commit_hook(self, local_site=None, publish=True):
        """Testing posting to a commit hook.

        This will simulate pushing a commit and posting the resulting webhook
        payload from GitHub to the handler for the hook.

        Args:
            local_site (reviewboard.site.models.LocalSite, optional):
                The Local Site owning the review request.

            publish (bool, optional):
                Whether to test with a published review request.
        """
        account = self.create_hosting_account(local_site=local_site)
        repository = self.create_repository(hosting_account=account, local_site=local_site)
        review_request = self.create_review_request(repository=repository, local_site=local_site, publish=publish)
        self.assertEqual(review_request.status, review_request.PENDING_REVIEW)
        url = local_site_reverse(b'github-hooks-close-submitted', local_site=local_site, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': b'github'})
        response = self._post_commit_hook_payload(post_url=url, review_request_url=review_request.get_absolute_url(), secret=repository.get_or_create_hooks_uuid())
        self.assertEqual(response.status_code, 200)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertTrue(review_request.public)
        self.assertEqual(review_request.status, review_request.SUBMITTED)
        self.assertEqual(review_request.changedescs.count(), 1)
        changedesc = review_request.changedescs.get()
        self.assertEqual(changedesc.text, b'Pushed to master (1c44b46)')

    def _post_commit_hook_payload(self, post_url, review_request_url, secret, event=b'push'):
        """Post a payload for a hook for testing.

        Args:
            post_url (unicode):
                The URL to post to.

            review_request_url (unicode):
                The URL of the review request being represented in the
                payload.

            secret (unicode):
                The HMAC secret for the message.

            event (unicode, optional):
                The webhook event.

        Results:
            django.core.handlers.request.wsgi.WSGIRequest:
            The post request.
        """
        payload = self.dump_json({b'ref': b'refs/heads/master', 
           b'commits': [
                      {b'id': b'1c44b461cebe5874a857c51a4a13a849a4d1e52d', 
                         b'message': b'This is my fancy commit\n\nReviewed at http://example.com%s' % review_request_url}]})
        m = hmac.new(bytes(secret), payload, hashlib.sha1)
        return self.client.post(post_url, payload, content_type=b'application/json', HTTP_X_GITHUB_EVENT=event, HTTP_X_HUB_SIGNATURE=b'sha1=%s' % m.hexdigest())