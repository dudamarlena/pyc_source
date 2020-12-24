# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/tests/test_git.py
# Compiled at: 2020-04-14 20:27:46
"""Unit tests for GitClient."""
from __future__ import unicode_literals
import os
from hashlib import md5
import six
from kgb import SpyAgency
from nose import SkipTest
from rbtools.clients import RepositoryInfo
from rbtools.clients.errors import CreateCommitError, MergeError, PushError, TooManyRevisionsError
from rbtools.clients.git import GitClient
from rbtools.clients.tests import FOO1, FOO2, FOO3, FOO4, SCMClientTests
from rbtools.utils.console import edit_text
from rbtools.utils.filesystem import is_exe_in_path, load_config
from rbtools.utils.process import execute

class GitClientTests(SpyAgency, SCMClientTests):
    """Unit tests for GitClient."""
    TESTSERVER = b'http://127.0.0.1:8080'
    AUTHOR = type(str(b'Author'), (
     object,), {b'fullname': b'name', 
       b'email': b'email'})

    def _run_git(self, command):
        return execute([b'git'] + command, env=None, cwd=self.clone_dir, split_lines=False, ignore_errors=False, extra_ignore_errors=())

    def _git_add_file_commit(self, filename, data, msg):
        """Add a file to a git repository.

        Args:
            filename (unicode):
                The filename to write to.

            data (unicode):
                The content of the file to write.

            msg (unicode):
                The commit message to use.
        """
        with open(filename, b'wb') as (f):
            f.write(data)
        self._run_git([b'add', filename])
        self._run_git([b'commit', b'-m', msg])

    def _git_get_head(self):
        return self._run_git([b'rev-parse', b'HEAD']).strip()

    def setUp(self):
        if not is_exe_in_path(b'git'):
            raise SkipTest(b'git not found in path')
        super(GitClientTests, self).setUp()
        self.set_user_home(os.path.join(self.testdata_dir, b'homedir'))
        self.git_dir = os.path.join(self.testdata_dir, b'git-repo')
        self.clone_dir = self.chdir_tmp()
        self._run_git([b'clone', self.git_dir, self.clone_dir])
        self.client = GitClient(options=self.options)
        self.options.parent_branch = None
        self.options.tracking = None
        return

    def test_get_repository_info_simple(self):
        """Testing GitClient get_repository_info, simple case"""
        ri = self.client.get_repository_info()
        self.assertTrue(isinstance(ri, RepositoryInfo))
        self.assertEqual(ri.base_path, b'')
        self.assertEqual(ri.path.rstrip(b'/.git'), self.git_dir)
        self.assertTrue(ri.supports_parent_diffs)
        self.assertFalse(ri.supports_changesets)

    def test_scan_for_server_simple(self):
        """Testing GitClient scan_for_server, simple case"""
        ri = self.client.get_repository_info()
        server = self.client.scan_for_server(ri)
        self.assertTrue(server is None)
        return

    def test_scan_for_server_reviewboardrc(self):
        """Testing GitClient scan_for_server, .reviewboardrc case"""
        with self.reviewboardrc({b'REVIEWBOARD_URL': self.TESTSERVER}):
            self.client.config = load_config()
            ri = self.client.get_repository_info()
            server = self.client.scan_for_server(ri)
            self.assertEqual(server, self.TESTSERVER)

    def test_scan_for_server_property(self):
        """Testing GitClient scan_for_server using repo property"""
        self._run_git([b'config', b'reviewboard.url', self.TESTSERVER])
        ri = self.client.get_repository_info()
        self.assertEqual(self.client.scan_for_server(ri), self.TESTSERVER)

    def test_diff_simple(self):
        """Testing GitClient simple diff case"""
        self.client.get_repository_info()
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO1, b'delete and modify stuff')
        commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_too_many_revisions(self):
        """Testing GitClient parse_revision_spec with too many revisions"""
        self.assertRaises(TooManyRevisionsError, self.client.parse_revision_spec, [
         1, 2, 3])

    def test_diff_simple_multiple(self):
        """Testing GitClient simple diff with multiple commits case"""
        self.client.get_repository_info()
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        self._git_add_file_commit(b'foo.txt', FOO2, b'commit 1')
        self._git_add_file_commit(b'foo.txt', FOO3, b'commit 1')
        commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'c9a31264f773406edff57a8ed10d9acc')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_exclude(self):
        """Testing GitClient simple diff with file exclusion"""
        self.client.get_repository_info()
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        self._git_add_file_commit(b'exclude.txt', FOO2, b'commit 2')
        commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[b'exclude.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_exclude_in_subdir(self):
        """Testing GitClient simple diff with file exclusion in a subdir"""
        base_commit_id = self._git_get_head()
        os.mkdir(b'subdir')
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        self._git_add_file_commit(b'subdir/exclude.txt', FOO2, b'commit 2')
        os.chdir(b'subdir')
        self.client.get_repository_info()
        commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[
         b'exclude.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_exclude_root_pattern_in_subdir(self):
        """Testing GitClient diff with file exclusion in the repo root"""
        base_commit_id = self._git_get_head()
        os.mkdir(b'subdir')
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        self._git_add_file_commit(b'exclude.txt', FOO2, b'commit 2')
        os.chdir(b'subdir')
        self.client.get_repository_info()
        commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[
         os.path.sep + b'exclude.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_branch_diverge(self):
        """Testing GitClient diff with divergent branches"""
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        self._run_git([b'checkout', b'-b', b'mybranch', b'--track',
         b'origin/master'])
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'commit 2')
        commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'cfb79a46f7a35b07e21765608a7852f7')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        self._run_git([b'checkout', b'master'])
        self.client.get_repository_info()
        commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_tracking_no_origin(self):
        """Testing GitClient diff with a tracking branch, but no origin
        remote"""
        self._run_git([b'remote', b'add', b'quux', self.git_dir])
        self._run_git([b'fetch', b'quux'])
        self._run_git([b'checkout', b'-b', b'mybranch', b'--track', b'quux/master'])
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO1, b'delete and modify stuff')
        commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_local_tracking(self):
        """Testing GitClient diff with a local tracking branch"""
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        self._run_git([b'checkout', b'-b', b'mybranch', b'--track', b'master'])
        self._git_add_file_commit(b'foo.txt', FOO2, b'commit 2')
        commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'cfb79a46f7a35b07e21765608a7852f7')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_tracking_override(self):
        """Testing GitClient diff with option override for tracking branch"""
        self.options.tracking = b'origin/master'
        self._run_git([b'remote', b'add', b'bad', self.git_dir])
        self._run_git([b'fetch', b'bad'])
        self._run_git([b'checkout', b'-b', b'mybranch', b'--track', b'bad/master'])
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO1, b'commit 1')
        commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'69d4616cf985f6b10571036db744e2d8')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_diff_slash_tracking(self):
        """Testing GitClient diff with tracking branch that has slash in its
        name"""
        self._run_git([b'fetch', b'origin'])
        self._run_git([b'checkout', b'-b', b'my/branch', b'--track',
         b'origin/not-master'])
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'commit 2')
        commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'parent_diff' in result)
        self.assertTrue(b'base_commit_id' in result)
        self.assertTrue(b'commit_id' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'd2015ff5fd0297fd7f1210612f87b6b3')
        self.assertEqual(result[b'parent_diff'], None)
        self.assertEqual(result[b'base_commit_id'], base_commit_id)
        self.assertEqual(result[b'commit_id'], commit_id)
        return

    def test_parse_revision_spec_no_args(self):
        """Testing GitClient.parse_revision_spec with no specified revisions"""
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_parse_revision_spec_no_args_parent(self):
        """Testing GitClient.parse_revision_spec with no specified revisions
        and a parent diff"""
        parent_base_commit_id = self._git_get_head()
        self._run_git([b'fetch', b'origin'])
        self._run_git([b'checkout', b'-b', b'parent-branch', b'--track',
         b'origin/not-master'])
        parent_base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        base_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'topic-branch'])
        self._git_add_file_commit(b'foo.txt', FOO3, b'Commit 3')
        tip_commit_id = self._git_get_head()
        self.options.parent_branch = b'parent-branch'
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' in revisions)
        self.assertEqual(revisions[b'parent_base'], parent_base_commit_id)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_parse_revision_spec_one_arg(self):
        """Testing GitClient.parse_revision_spec with one specified revision"""
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([tip_commit_id])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_parse_revision_spec_one_arg_parent(self):
        """Testing GitClient.parse_revision_spec with one specified revision
        and a parent diff"""
        parent_base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO3, b'Commit 3')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([tip_commit_id])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' in revisions)
        self.assertEqual(revisions[b'parent_base'], parent_base_commit_id)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_parse_revision_spec_two_args(self):
        """Testing GitClient.parse_revision_spec with two specified
        revisions"""
        base_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'topic-branch'])
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([b'master', b'topic-branch'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_parse_revision_spec_one_arg_two_revs(self):
        """Testing GitClient.parse_revision_spec with diff-since syntax"""
        base_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'topic-branch'])
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([b'master..topic-branch'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_parse_revision_spec_one_arg_since_merge(self):
        """Testing GitClient.parse_revision_spec with diff-since-merge
        syntax"""
        base_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'topic-branch'])
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([b'master...topic-branch'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], base_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_diff_finding_parent(self):
        """Testing GitClient.parse_revision_spec with target branch off a
        tracking branch not aligned with the remote"""
        self.client.get_repository_info()
        self._git_add_file_commit(b'foo.txt', FOO1, b'on master')
        self._run_git([b'checkout', b'not-master'])
        parent_base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'on not-master')
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'topic-branch'])
        self._git_add_file_commit(b'foo.txt', FOO3, b'commit 2')
        self._git_add_file_commit(b'foo.txt', FOO4, b'commit 3')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([
         b'topic-branch', b'^not-master'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)
        self.assertEqual(revisions[b'parent_base'], parent_base_commit_id)

    def test_diff_finding_parent_case_one(self):
        """Testing GitClient.parse_revision_spec with target branch off a
        tracking branch aligned with the remote"""
        self.client.get_repository_info()
        self._run_git([b'fetch', b'origin'])
        self._run_git([b'checkout', b'-b', b'not-master',
         b'--track', b'origin/not-master'])
        self.options.tracking = b'origin/not-master'
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo.txt', FOO3, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertFalse(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_diff_finding_parent_case_two(self):
        """Testing GitClient.parse_revision_spec with target branch off
        a tracking branch with changes since the remote"""
        self.client.get_repository_info()
        self._run_git([b'fetch', b'origin'])
        self._run_git([b'checkout', b'-b', b'not-master',
         b'--track', b'origin/not-master'])
        parent_base_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'on not-master')
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo.txt', FOO3, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([b'feature-branch',
         b'^not-master'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)
        self.assertEqual(revisions[b'parent_base'], parent_base_commit_id)

    def test_diff_finding_parent_case_three(self):
        """Testing GitClient.parse_revision_spec with target branch off a
        branch not properly tracking the remote"""
        self.client.get_repository_info()
        self._run_git([b'branch', b'--no-track', b'not-master',
         b'origin/not-master'])
        self._run_git([b'checkout', b'not-master'])
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo.txt', FOO3, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([b'feature-branch',
         b'^not-master'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 2)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertFalse(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_diff_finding_parent_case_four(self):
        """Testing GitClient.parse_revision_spec with a target branch that
        merged a tracking branch off another tracking branch"""
        self.client.get_repository_info()
        self._run_git([b'checkout', b'master'])
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo.txt', FOO1, b'on feature-branch')
        self._run_git([b'merge', b'origin/not-master'])
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'commit_id' in revisions)
        self.assertFalse(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)
        self.assertEqual(revisions[b'commit_id'], tip_commit_id)

    def test_diff_finding_parent_case_five(self):
        """Testing GitClient.parse_revision_spec with a target branch posted
        off a tracking branch that merged another tracking branch"""
        self.client.get_repository_info()
        self._git_add_file_commit(b'foo.txt', FOO2, b'on master')
        self._run_git([b'checkout', b'-b', b'not-master',
         b'--track', b'origin/not-master'])
        self.options.tracking = b'origin/not-master'
        self._run_git([b'merge', b'origin/master'])
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo.txt', FOO4, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'commit_id' in revisions)
        self.assertFalse(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)
        self.assertEqual(revisions[b'commit_id'], tip_commit_id)

    def test_diff_finding_parent_case_six(self):
        """Testing GitClient.parse_revision_spec with a target branch posted
        off a remote branch without any tracking branches"""
        self.client.get_repository_info()
        self._run_git([b'checkout', b'-b', b'feature-branch',
         b'origin/not-master'])
        parent_commit_id = self._git_get_head()
        self._git_add_file_commit(b'foo.txt', FOO2, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec([])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'commit_id' in revisions)
        self.assertFalse(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)
        self.assertEqual(revisions[b'commit_id'], tip_commit_id)

    def test_diff_finding_parent_case_seven(self):
        """Testing GitClient.parse_revision_spec with a target branch posted
        off a remote branch that is aligned to the same commit as another
        remote branch"""
        self.client.get_repository_info()
        self.git_dir = os.getcwd()
        self.clone_dir = self.chdir_tmp()
        self._run_git([b'clone', self.git_dir, self.clone_dir])
        self.client.get_repository_info()
        self._run_git([b'checkout', b'-b', b'remote-branch1'])
        self._git_add_file_commit(b'foo1.txt', FOO1, b'on remote-branch1')
        self._run_git([b'push', b'origin', b'remote-branch1'])
        self._run_git([b'checkout', b'-b', b'remote-branch2'])
        self._git_add_file_commit(b'foo2.txt', FOO1, b'on remote-branch2')
        self._run_git([b'push', b'origin', b'remote-branch2'])
        self._run_git([b'checkout', b'master'])
        self._run_git([b'merge', b'remote-branch1'])
        self._run_git([b'merge', b'remote-branch2'])
        self._git_add_file_commit(b'foo3.txt', FOO1, b'on master')
        parent_commit_id = self._git_get_head()
        self._run_git([b'push', b'origin', b'master:remote-branch1'])
        self._run_git([b'push', b'origin', b'master:remote-branch2'])
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo4.txt', FOO1, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([b'feature-branch',
         b'^master'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 2)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertFalse(b'parent_base' in revisions)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_diff_finding_parent_case_eight(self):
        """Testing GitClient.parse_revision_spec with a target branch not
        up-to-date with a remote branch"""
        self.client.get_repository_info()
        self.git_dir = os.getcwd()
        self.clone_dir = self.chdir_tmp()
        self._run_git([b'clone', self.git_dir, self.clone_dir])
        self.client.get_repository_info()
        self._run_git([b'checkout', b'master'])
        self._git_add_file_commit(b'foo.txt', FOO1, b'on master')
        parent_base_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'remote-branch1'])
        self._git_add_file_commit(b'foo1.txt', FOO1, b'on remote-branch1')
        self._run_git([b'push', b'origin', b'remote-branch1'])
        self._run_git([b'checkout', b'master'])
        self._git_add_file_commit(b'foo2.txt', FOO1, b'on master')
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo3.txt', FOO1, b'on feature-branch')
        self.client.get_repository_info()
        tip_commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([b'feature-branch',
         b'^master'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' in revisions)
        self.assertEqual(revisions[b'parent_base'], parent_base_commit_id)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_diff_finding_parent_case_nine(self):
        """Testing GitClient.parse_revision_spec with a target branch that has
        branches from different remotes in its path"""
        self.client.get_repository_info()
        self._run_git([b'checkout', b'not-master'])
        orig_clone = os.getcwd()
        self.clone_dir = self.chdir_tmp()
        self._run_git([b'clone', self.git_dir, self.clone_dir])
        self.client.get_repository_info()
        self._run_git([b'remote', b'add', b'not-origin', orig_clone])
        self._run_git([b'fetch', b'not-origin'])
        parent_base_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'master'])
        self._run_git([b'merge', b'not-origin/master'])
        self._git_add_file_commit(b'foo1.txt', FOO1, b'on master')
        self._run_git([b'push', b'not-origin', b'master:master'])
        self._git_add_file_commit(b'foo2.txt', FOO1, b'on master')
        parent_commit_id = self._git_get_head()
        self._run_git([b'checkout', b'-b', b'feature-branch'])
        self._git_add_file_commit(b'foo3.txt', FOO1, b'on feature-branch')
        tip_commit_id = self._git_get_head()
        revisions = self.client.parse_revision_spec([b'feature-branch',
         b'^master'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertEqual(len(revisions), 3)
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' in revisions)
        self.assertEqual(revisions[b'parent_base'], parent_base_commit_id)
        self.assertEqual(revisions[b'base'], parent_commit_id)
        self.assertEqual(revisions[b'tip'], tip_commit_id)

    def test_get_raw_commit_message(self):
        """Testing GitClient.get_raw_commit_message"""
        self._git_add_file_commit(b'foo.txt', FOO2, b'Commit 2')
        self.client.get_repository_info()
        revisions = self.client.parse_revision_spec()
        self.assertEqual(self.client.get_raw_commit_message(revisions), b'Commit 2')

    def test_push_upstream_pull_exception(self):
        """Testing GitClient.push_upstream with an invalid remote branch"""
        with self.assertRaisesRegexp(PushError, b'Could not determine remote for branch "non-existent-branch".'):
            self.client.push_upstream(b'non-existent-branch')

    def test_push_upstream_no_push_exception(self):
        """Testing GitClient.push_upstream with 'git push' disabled"""
        self._run_git([b'remote', b'set-url', b'--push', b'origin', b'bad-url'])
        with self.assertRaisesRegexp(PushError, b'Could not push branch "master" to upstream\\.'):
            self.client.push_upstream(b'master')

    def test_merge_invalid_destination(self):
        """Testing GitClient.merge with an invalid destination branch"""
        try:
            self.client.merge(b'master', b'non-existent-branch', b'commit message', self.AUTHOR)
        except MergeError as e:
            self.assertTrue(six.text_type(e).startswith(b'Could not checkout to branch "non-existent-branch"'))
        else:
            self.fail(b'Expected MergeError')

    def test_merge_invalid_target(self):
        """Testing GitClient.merge with an invalid target branch"""
        try:
            self.client.merge(b'non-existent-branch', b'master', b'commit message', self.AUTHOR)
        except MergeError as e:
            self.assertTrue(six.text_type(e).startswith(b'Could not merge branch "non-existent-branch"'))
        else:
            self.fail(b'Expected MergeError')

    def test_merge_with_squash(self):
        """Testing GitClient.merge with squash set to True"""
        self.spy_on(execute)
        self.client.get_repository_info()
        self.git_dir = os.getcwd()
        self.clone_dir = self.chdir_tmp()
        self._run_git([b'clone', self.git_dir, self.clone_dir])
        self.client.get_repository_info()
        self._run_git([b'checkout', b'-b', b'new-branch'])
        self._git_add_file_commit(b'foo1.txt', FOO1, b'on new-branch')
        self._run_git([b'push', b'origin', b'new-branch'])
        self.client.merge(b'new-branch', b'master', b'message', self.AUTHOR, True)
        self.assertEqual(execute.spy.calls[(-2)].args[0], [
         b'git', b'merge', b'new-branch', b'--squash',
         b'--no-commit'])

    def test_merge_without_squash(self):
        """Testing GitClient.merge with squash set to False"""
        self.spy_on(execute)
        self.client.get_repository_info()
        self.git_dir = os.getcwd()
        self.clone_dir = self.chdir_tmp()
        self._run_git([b'clone', self.git_dir, self.clone_dir])
        self.client.get_repository_info()
        self._run_git([b'checkout', b'-b', b'new-branch'])
        self._git_add_file_commit(b'foo1.txt', FOO1, b'on new-branch')
        self._run_git([b'push', b'origin', b'new-branch'])
        self.client.merge(b'new-branch', b'master', b'message', self.AUTHOR, False)
        self.assertEqual(execute.spy.calls[(-2)].args[0], [
         b'git', b'merge', b'new-branch', b'--no-ff',
         b'--no-commit'])

    def test_create_commit_with_run_editor_true(self):
        """Testing GitClient.create_commit with run_editor set to True"""
        self.spy_on(execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'Test commit message.', author=self.AUTHOR, run_editor=True, files=[
         b'foo.txt'])
        self.assertTrue(execute.last_called_with([
         b'git', b'commit', b'-m', b'TEST COMMIT MESSAGE.',
         b'--author', b'name <email>']))

    def test_create_commit_with_run_editor_false(self):
        """Testing GitClient.create_commit with run_editor set to False"""
        self.spy_on(execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'Test commit message.', author=self.AUTHOR, run_editor=False, files=[
         b'foo.txt'])
        self.assertTrue(execute.last_called_with([
         b'git', b'commit', b'-m', b'Test commit message.',
         b'--author', b'name <email>']))

    def test_create_commit_with_all_files_true(self):
        """Testing GitClient.create_commit with all_files set to True"""
        self.spy_on(execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'message', author=self.AUTHOR, run_editor=False, files=[], all_files=True)
        self.assertTrue(execute.calls[0].called_with([
         b'git', b'add', b'--all', b':/']))
        self.assertTrue(execute.last_called_with([
         b'git', b'commit', b'-m', b'message',
         b'--author', b'name <email>']))

    def test_create_commit_with_all_files_false(self):
        """Testing GitClient.create_commit with all_files set to False"""
        self.spy_on(execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'message', author=self.AUTHOR, run_editor=False, files=[
         b'foo.txt'], all_files=False)
        self.assertTrue(execute.calls[0].called_with([
         b'git', b'add', b'foo.txt']))
        self.assertTrue(execute.last_called_with([
         b'git', b'commit', b'-m', b'message',
         b'--author', b'name <email>']))

    def test_create_commit_with_empty_commit_message(self):
        """Testing GitClient.create_commit with empty commit message"""
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        message = b"A commit message wasn't provided. The patched files are in your tree and are staged for commit, but haven't been committed. Run `git commit` to commit them."
        with self.assertRaisesMessage(CreateCommitError, message):
            self.client.create_commit(message=b'', author=self.AUTHOR, run_editor=True, files=[
             b'foo.txt'])

    def test_create_commit_without_author(self):
        """Testing GitClient.create_commit without author information"""
        self.spy_on(execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'Test commit message.', author=None, run_editor=True, files=[
         b'foo.txt'])
        self.assertTrue(execute.last_called_with([
         b'git', b'commit', b'-m', b'TEST COMMIT MESSAGE.']))
        return

    def test_delete_branch_with_merged_only(self):
        """Testing GitClient.delete_branch with merged_only set to True"""
        self.spy_on(execute)
        self._run_git([b'branch', b'new-branch'])
        self.client.delete_branch(b'new-branch', True)
        self.assertTrue(execute.spy.called)
        self.assertEqual(execute.spy.last_call.args[0], [
         b'git', b'branch', b'-d', b'new-branch'])

    def test_delete_branch_without_merged_only(self):
        """Testing GitClient.delete_branch with merged_only set to False"""
        self.spy_on(execute)
        self._run_git([b'branch', b'new-branch'])
        self.client.delete_branch(b'new-branch', False)
        self.assertTrue(execute.spy.called)
        self.assertEqual(execute.spy.last_call.args[0], [
         b'git', b'branch', b'-D', b'new-branch'])