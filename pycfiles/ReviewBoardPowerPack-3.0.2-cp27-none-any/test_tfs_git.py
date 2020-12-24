# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/scmtools/tests/test_tfs_git.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import base64, json
from django.utils import six
from django.utils.six.moves.urllib.request import OpenerDirector, build_opener, urlopen
from kgb import SpyAgency
from reviewboard.scmtools.errors import SCMError
from reviewboard.scmtools.models import Tool, Repository
from reviewboard.scmtools.tests import SCMTestCase
from rbpowerpack.scmtools.tfs_git import TFSGitTool
from rbpowerpack.testing.testcases import PowerPackExtensionTestCase

class EmptyResponse200(object):
    code = 200
    headers = {}

    def read(self):
        return b'{  "count": 0,  "value": []}'


class Response404(object):
    code = 404
    headers = {}

    def read(self):
        return b''


class TFSGitTests(SpyAgency, PowerPackExtensionTestCase, SCMTestCase):
    """Unit tests for TFS-Git."""

    def setUp(self):
        super(TFSGitTests, self).setUp()
        self.collection_path = b'http://tfs:8080/tfs/DefaultCollection/'
        self.api_path = b'%s_apis/' % self.collection_path
        self.path = b'%s_git/' % self.collection_path
        self.tool = Tool.objects.get(name=b'Team Foundation Server (git)')
        self.repository = Repository(name=b'TFS-Git', path=self.path, tool=self.tool)

    def test_api_path_lookup_with_ntlm_auth(self):
        """Testing TFSGitTool API path lookup with NTLM auth"""

        class Opener(OpenerDirector):

            def open(s, url):
                found_paths.append(url)
                if url == expected_api_path:
                    return EmptyResponse200()
                else:
                    return Response404()

        expected_api_path = b'%sgit/repositories?api-version=1.0' % self.api_path
        found_paths = []
        opener = Opener()
        self.spy_on(build_opener, call_fake=lambda *args: opener)
        self.spy_on(opener.open)
        repo = Repository.objects.create(name=b'Test', path=b'http://tfs:8080/tfs/DefaultCollection/MyProject/_git/MyRepo', tool=Tool.objects.get(name=b'Team Foundation Server (git)'))
        repo.username = b'my-user'
        repo.password = b'my-pass'
        self.assertFalse(opener.open.called)
        tool = repo.get_scmtool()
        self.assertIsNone(tool.client.path)
        self.assertFalse(opener.open.called)
        tool.client._find_api_path()
        self.assertEqual(tool.client.path, self.collection_path)
        self.assertTrue(opener.open.called)
        self.assertEqual(found_paths, [
         b'http://tfs:8080/tfs/DefaultCollection/MyProject/_apis/git/repositories?api-version=1.0',
         b'http://tfs:8080/tfs/DefaultCollection/_apis/git/repositories?api-version=1.0'])
        self.assertEqual(tool.client.password_manager.find_user_password(None, expected_api_path), ('my-user',
                                                                                                    'my-pass'))
        return

    def test_api_path_lookup_with_basic_auth(self):
        """Testing TFSGitTool API path lookup with HTTP Basic Auth"""

        def _urlopen(request, *args, **kwargs):
            self.assertEqual(request.get_header(b'Authorization'), b'Basic %s' % tool.client.basic_credentials)
            url = request.get_full_url()
            found_paths.append(url)
            if url == expected_api_path:
                return EmptyResponse200()
            else:
                return Response404()

        expected_api_path = b'%sgit/repositories?api-version=1.0' % self.api_path
        found_paths = []
        self.spy_on(urlopen, call_fake=_urlopen)
        repo = Repository.objects.create(name=b'Test', path=b'http://tfs:8080/tfs/DefaultCollection/MyProject/_git/MyRepo', tool=Tool.objects.get(name=b'Team Foundation Server (git)'))
        repo.username = b'my-user'
        repo.password = b'my-pass'
        repo.extra_data[b'tfs_use_basic_auth'] = True
        self.assertFalse(urlopen.spy.called)
        tool = repo.get_scmtool()
        self.assertTrue(tool.client.use_basic_auth)
        self.assertEqual(tool.client.basic_credentials, base64.b64encode(b'my-user:my-pass'))
        self.assertIsNone(tool.client.password_manager)
        self.assertIsNone(tool.client.path)
        self.assertFalse(urlopen.spy.called)
        tool.client._find_api_path()
        self.assertEqual(tool.client.path, self.collection_path)
        self.assertTrue(urlopen.spy.called)
        self.assertEqual(found_paths, [
         b'http://tfs:8080/tfs/DefaultCollection/MyProject/_apis/git/repositories?api-version=1.0',
         b'http://tfs:8080/tfs/DefaultCollection/_apis/git/repositories?api-version=1.0'])

    def test_api_path_lookup_with_stored_extra_data(self):
        """Testing TFSGitTool API path lookup with path stored in
        repository.extra_data
        """
        opener = OpenerDirector()
        self.spy_on(build_opener, call_fake=lambda *args: opener)
        self.spy_on(opener.open)
        repo = Repository.objects.create(name=b'Test', path=b'http://tfs:8080/tfs/DefaultCollection/MyProject/_git/MyRepo', tool=Tool.objects.get(name=b'Team Foundation Server (git)'))
        repo.username = b'my-user'
        repo.password = b'my-pass'
        repo.extra_data[b'tfs_api_path'] = b'http://example.com/'
        tool = repo.get_scmtool()
        self.assertEqual(tool.client.path, b'http://example.com/')
        self.assertFalse(opener.open.called)
        self.assertEqual(tool.client.password_manager.find_user_password(None, b'http://example.com/'), ('my-user',
                                                                                                         'my-pass'))
        return

    def test_check_repository_disabled(self):
        """Testing TFSGitTool.check_repository with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'Team Foundation Server (git) repositories cannot be used while Power Pack is disabled.', lambda : tool.check_repository(self.path, b'username', b'password'))

    def test_file_exists_disabled(self):
        """Testing TFSGitTool.file_exists with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS-Git" cannot be used while Power Pack is disabled.', lambda : tool.file_exists(b'my_file.txt', b'abc123', base_commit_id=None))

    def test_get_file_disabled(self):
        """Testing TFSGitTool.get_file with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS-Git" cannot be used while Power Pack is disabled.', lambda : tool.get_file(b'my_file.txt', b'abc123', base_commit_id=None))

    def test_get_branches(self):
        """Testing TFSGitTool.get_branches"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, b'%sgit/repositories/abc123/refs/heads?api-version=1.0' % self.api_path)

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        return json.dumps({b'count': 2, 
                           b'value': [
                                    {b'objectId': b'sha-1', 
                                       b'name': b'refs/heads/branch1'},
                                    {b'objectId': b'sha-2', 
                                       b'name': b'refs/heads/master'}]})

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        tool.client.repo_id = b'abc123'
        tool.client.path = self.collection_path
        branches = tool.get_branches()
        self.assertEqual(len(branches), 2)
        branch = branches[0]
        self.assertEqual(branch.id, b'branch1')
        self.assertEqual(branch.commit, b'sha-1')
        self.assertFalse(branch.default)
        branch = branches[1]
        self.assertEqual(branch.id, b'master')
        self.assertEqual(branch.commit, b'sha-2')
        self.assertTrue(branch.default)

    def test_get_branches_disabled(self):
        """Testing TFSGitTool.get_branches with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS-Git" cannot be used while Power Pack is disabled.', lambda : tool.get_branches())

    def test_get_commits(self):
        """Testing TFSGitTool.get_commits"""
        commits = self._get_commits(result=[
         {b'commitId': b'sha-2', 
            b'author': {b'name': b'Author 2'}, 
            b'committer': {b'date': b'2016-11-07T23:14:37.05Z'}, 
            b'comment': b'Commit 2'},
         {b'commitId': b'sha-1', 
            b'author': {b'name': b'Author 1'}, 
            b'committer': {b'date': b'2016-10-26T19:23:15.43Z'}, 
            b'comment': b'Commit 1'}])
        self.assertEqual(len(commits), 2)
        commit = commits[0]
        self.assertEqual(commit.id, b'sha-2')
        self.assertEqual(commit.author_name, b'Author 2')
        self.assertEqual(commit.message, b'Commit 2')
        self.assertEqual(commit.parent, b'sha-1')
        commit = commits[1]
        self.assertEqual(commit.id, b'sha-1')
        self.assertEqual(commit.author_name, b'Author 1')
        self.assertEqual(commit.message, b'Commit 1')
        self.assertEqual(commit.parent, b'')

    def test_get_commits_with_branch_name(self):
        """Testing TFSGitTool.get_commits with branch name"""
        commits = self._get_commits(branch=b'my-branch', result=[
         {b'commitId': b'sha-1', 
            b'author': {b'name': b'Author 1'}, 
            b'committer': {b'date': b'2016-11-07T23:14:37.05Z'}, 
            b'comment': b'Commit 1'}])
        self.assertEqual(len(commits), 1)
        commit = commits[0]
        self.assertEqual(commit.id, b'sha-1')
        self.assertEqual(commit.author_name, b'Author 1')
        self.assertEqual(commit.message, b'Commit 1')
        self.assertEqual(commit.parent, b'')

    def test_get_commits_with_start(self):
        """Testing TFSGitTool.get_commits with start commit"""
        commits = self._get_commits(start=b'sha-1', result=[
         {b'commitId': b'sha-1', 
            b'author': {b'name': b'Author 1'}, 
            b'committer': {b'date': b'2016-11-07T23:14:37.05Z'}, 
            b'comment': b'Commit 1'}])
        self.assertEqual(len(commits), 1)
        commit = commits[0]
        self.assertEqual(commit.id, b'sha-1')
        self.assertEqual(commit.author_name, b'Author 1')
        self.assertEqual(commit.message, b'Commit 1')
        self.assertEqual(commit.parent, b'')

    def test_get_commits_with_branch_and_start(self):
        """Testing TFSGitTool.get_commits with branch name and start commit"""
        commits = self._get_commits(branch=b'my-branch', start=b'sha-1', result=[
         {b'commitId': b'sha-1', 
            b'author': {b'name': b'Author 1'}, 
            b'committer': {b'date': b'2016-11-07T23:14:37.05Z'}, 
            b'comment': b'Commit 1'}])
        self.assertEqual(len(commits), 1)
        commit = commits[0]
        self.assertEqual(commit.id, b'sha-1')
        self.assertEqual(commit.author_name, b'Author 1')
        self.assertEqual(commit.message, b'Commit 1')
        self.assertEqual(commit.parent, b'')

    def test_get_commits_with_parent_on_last_item_on_page(self):
        """Testing TFSGitTool.get_commits with fetching parent SHA on last
        item on a page of results
        """
        results = [ {b'commitId': b'sha-%s' % i, b'author': {b'name': b'Author %s' % i}, b'committer': {b'date': b'2016-11-07T23:14:37.05Z'}, b'comment': b'Commit %s' % i} for i in range(1, TFSGitTool.COMMITS_PER_PAGE + 2)
                  ]
        commits = self._get_commits(result=results)
        self.assertEqual(len(commits), 20)
        commit = commits[(-1)]
        self.assertEqual(commit.id, b'sha-20')
        self.assertEqual(commit.author_name, b'Author 20')
        self.assertEqual(commit.message, b'Commit 20')
        self.assertEqual(commit.parent, b'sha-21')

    def test_get_change(self):
        """Testing TFSGitTool.get_change"""

        class Opener(OpenerDirector):

            def open(s, url):
                assert url.startswith(self.api_path)
                key = url[len(self.api_path):].split(b'?', 1)[0]
                try:
                    handler = url_handlers[key]
                except KeyError:
                    self.fail(b'Unexpected URL encountered in get_change() test: %s' % url)

                payload = handler(url)

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        if isinstance(payload, (bytes, six.text_type)):
                            return payload
                        else:
                            return json.dumps(payload)

                return Response()

        def _handle_commits_url(url):
            return {b'value': [
                        {b'commitId': b'c07f317c4127d8667a4bd6c08d48e716b1d47da1', 
                           b'author': {b'name': b'Author 2'}, 
                           b'committer': {b'date': b'2016-11-07T23:14:37.05Z'}, 
                           b'comment': b'Commit 2'},
                        {b'commitId': b'd32758130e6c8cb46c00868bd4314b98f0c55468', 
                           b'author': {b'name': b'Author 1'}, 
                           b'committer': {b'date': b'2016-10-26T19:23:15.43Z'}, 
                           b'comment': b'Commit 1'}]}

        def _handle_diff_commits_url(url):
            self.assertURLsEqual(url, b'%sgit/repositories/abc123/diffs/commits?api-version=1.0&baseVersionType=commit&targetVersionType=commit&baseVersion=d32758130e6c8cb46c00868bd4314b98f0c55468&targetVersion=c07f317c4127d8667a4bd6c08d48e716b1d47da1&$top=1000' % self.api_path)
            return {b'changes': [
                          {b'changeType': b'edit', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file1', 
                                       b'originalObjectId': b'6ebadc6dabb93f88bcded2f9a7be2ebf00f6cad6', 
                                       b'objectId': b'b156588983d4df593b46ca51386b591451a69707'}},
                          {b'changeType': b'add', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file2', 
                                       b'objectId': b'fb002728ff7a285be696a0f86bbe9834b11833f7'}},
                          {b'changeType': b'delete', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file3', 
                                       b'originalObjectId': b'5a838949cd57780d0f369eaf37dbbf2d8a5d08a6'}},
                          {b'changeType': b'rename', 
                             b'sourceServerItem': b'/file4', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file5', 
                                       b'originalObjectId': b'34dd46008fc647a637b838db77dbeacd50657062', 
                                       b'objectId': b'34dd46008fc647a637b838db77dbeacd50657062'}},
                          {b'changeType': b'delete, sourceRename', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file4', 
                                       b'originalObjectId': b'34dd46008fc647a637b838db77dbeacd50657062', 
                                       b'objectId': b''}},
                          {b'changeType': b'delete, sourceRename', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file6', 
                                       b'originalObjectId': b'a4f0e954765f60e332fe58e4bdfa3f6553d7d249', 
                                       b'objectId': b''}},
                          {b'changeType': b'edit, rename', 
                             b'sourceServerItem': b'/file6', 
                             b'item': {b'gitObjectType': b'blob', 
                                       b'path': b'/file7', 
                                       b'originalObjectId': b'a4f0e954765f60e332fe58e4bdfa3f6553d7d249', 
                                       b'objectId': b'b8f78f121c20b84fdd43699bd9ba9050a659500e'}}]}

        def _handle_orig_file1_blob_url(url):
            return b'This is file 1 (original)\n'

        def _handle_new_file1_blob_url(url):
            return b'This is file 1 (modified)\n'

        def _handle_file2_blob_url(url):
            return b'This is file 2\n'

        def _handle_file3_blob_url(url):
            return b'This is file 3\n'

        def _handle_file6_blob_url(url):
            return b'This is file 6\n'

        def _handle_file7_blob_url(url):
            return b'This is file 7\n'

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        repo_base = b'git/repositories/abc123/'
        url_handlers = {repo_base + b'commits': _handle_commits_url, 
           repo_base + b'diffs/commits': _handle_diff_commits_url, 
           repo_base + b'blobs/6ebadc6dabb93f88bcded2f9a7be2ebf00f6cad6': _handle_orig_file1_blob_url, 
           repo_base + b'blobs/b156588983d4df593b46ca51386b591451a69707': _handle_new_file1_blob_url, 
           repo_base + b'blobs/fb002728ff7a285be696a0f86bbe9834b11833f7': _handle_file2_blob_url, 
           repo_base + b'blobs/5a838949cd57780d0f369eaf37dbbf2d8a5d08a6': _handle_file3_blob_url, 
           repo_base + b'blobs/a4f0e954765f60e332fe58e4bdfa3f6553d7d249': _handle_file6_blob_url, 
           repo_base + b'blobs/b8f78f121c20b84fdd43699bd9ba9050a659500e': _handle_file7_blob_url}
        self.repository.extra_data.update({b'repo_id': b'abc123', 
           b'tfs_api_path': self.collection_path})
        tool = self.repository.get_scmtool()
        commit = tool.get_change(b'c07f317c4127d8667a4bd6c08d48e716b1d47da1')
        self.assertEqual(commit.id, b'c07f317c4127d8667a4bd6c08d48e716b1d47da1')
        self.assertEqual(commit.author_name, b'Author 2')
        self.assertEqual(commit.message, b'Commit 2')
        self.assertEqual(commit.parent, b'd32758130e6c8cb46c00868bd4314b98f0c55468')
        self.assertEqual(commit.diff, b'diff --git a/file1 b/file1\nindex 6ebadc6dabb93f88bcded2f9a7be2ebf00f6cad6..b156588983d4df593b46ca51386b591451a69707\n--- file1\n+++ file1\n@@ -1 +1 @@\n-This is file 1 (original)\n+This is file 1 (modified)\ndiff --git a/file2 b/file2\nindex 000000000000000000000000000000000000000..fb002728ff7a285be696a0f86bbe9834b11833f7\n--- /dev/null\n+++ file2\n@@ -0,0 +1 @@\n+This is file 2\ndiff --git a/file3 b/file3\ndeleted file mode 100644\nindex 5a838949cd57780d0f369eaf37dbbf2d8a5d08a6..000000000000000000000000000000000000000\n--- file3\n+++ /dev/null\n@@ -1 +0,0 @@\n-This is file 3\ndiff --git a/file4 b/file5\nrename from file4\nrename to file5\ndiff --git a/file6 b/file7\nrename from file6\nrename to file7\nindex a4f0e954765f60e332fe58e4bdfa3f6553d7d249..b8f78f121c20b84fdd43699bd9ba9050a659500e\n--- file6\n+++ file7\n@@ -1 +1 @@\n-This is file 6\n+This is file 7\n')

    def test_get_change_disabled(self):
        """Testing TFSGitTool.get_change with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS-Git" cannot be used while Power Pack is disabled.', lambda : tool.get_change(1))

    def test_get_commits_disabled(self):
        """Testing TFSGitTool.get_commits with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS-Git" cannot be used while Power Pack is disabled.', lambda : tool.get_commits())

    def _get_commits(self, result, branch=None, start=None):

        class Opener(OpenerDirector):

            def open(s, url):
                query_args = []
                if start:
                    query_args.append(b'commit=%s' % start)
                elif branch:
                    query_args.append(b'branch=%s' % branch)
                self.assertURLsEqual(url, b'%sgit/repositories/abc123/commits?api-version=1.0&top=21&%s' % (
                 self.api_path, (b'&').join(query_args)))

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        return json.dumps({b'count': len(result), 
                           b'value': result})

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        self.repository.extra_data.update({b'repo_id': b'abc123', 
           b'tfs_api_path': self.collection_path})
        tool = self.repository.get_scmtool()
        return tool.get_commits(branch=branch, start=start)