# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/tests/test_mercurial.py
# Compiled at: 2020-04-14 20:27:46
"""Unit tests for MercurialClient."""
from __future__ import unicode_literals
import os, re, shutil, tempfile, time
from hashlib import md5
from random import randint
from textwrap import dedent
from kgb import SpyAgency
from nose import SkipTest
from six.moves import range
from rbtools.clients import RepositoryInfo
from rbtools.clients.errors import CreateCommitError, MergeError
from rbtools.clients.mercurial import MercurialClient, MercurialRefType
from rbtools.clients.tests import FOO, FOO1, FOO2, FOO3, FOO4, FOO5, FOO6, SCMClientTests
from rbtools.utils.encoding import force_unicode
from rbtools.utils.filesystem import is_exe_in_path, load_config, make_tempdir
from rbtools.utils.process import execute

class MercurialTestBase(SCMClientTests):
    """Base class for all Mercurial unit tests."""

    def run_hg(self, command, **kwargs):
        """Run a Mercurial command.

        Args:
            command (list of unicode):
                The command and arguments to pass to :program:`hg`.

            **kwargs (dict):
                Additional keyword arguments to pass to
                :py:func:`~rbtools.utils.process.execute`.

        Returns:
            object:
            The result of :py:func:`~rbtools.utils.process.execute`.
        """
        return execute(([
         b'hg'] + command), env={b'HGPLAIN': b'1'}, split_lines=False, results_unicode=False, **kwargs)

    def hg_add_file_commit(self, filename=b'test.txt', data=b'Test', msg=b'Test commit', branch=None, bookmark=None, tag=None):
        """Add a file to the repository and commit it.

        This can also optionally construct a branch for the commit.

        Args:
            filename (unicode, optional):
                The name of the file to write.

            data (bytes, optional):
                The data to write to the file.

            msg (unicode, optional):
                The commit message.

            branch (unicode, optional):
                The optional branch to create.

            bookmark (unicode, optional):
                The optional bookmark to create.

            tag (unicode, optional):
                The optional tag to create.
        """
        if branch:
            self.run_hg([b'branch', branch])
        if bookmark:
            self.run_hg([b'bookmark', bookmark])
        with open(filename, b'wb') as (f):
            f.write(data)
        self.run_hg([b'commit', b'-A', b'-m', msg, filename])
        if tag:
            self.run_hg([b'tag', tag])


class MercurialClientTests(SpyAgency, MercurialTestBase):
    """Unit tests for MercurialClient."""
    TESTSERVER = b'http://127.0.0.1:8080'
    CLONE_HGRC = dedent(b'\n        [ui]\n        username = test user <user at example.com>\n\n        [paths]\n        default = %(hg_dir)s\n        cloned = %(clone_dir)s\n\n        [reviewboard]\n        url = %(test_server)s\n\n        [diff]\n        git = true\n    ').rstrip()
    AUTHOR = type(str(b'Author'), (
     object,), {b'fullname': b'name', 
       b'email': b'email'})

    def setUp(self):
        super(MercurialClientTests, self).setUp()
        if not is_exe_in_path(b'hg'):
            raise SkipTest(b'hg not found in path')
        self.hg_dir = os.path.join(self.testdata_dir, b'hg-repo')
        self.clone_dir = self.chdir_tmp()
        self.clone_hgrc_path = os.path.join(self.clone_dir, b'.hg', b'hgrc')
        self.run_hg([b'clone', b'--stream', self.hg_dir, self.clone_dir])
        self.client = MercurialClient(options=self.options)
        with open(self.clone_hgrc_path, b'w') as (fp):
            fp.write(self.CLONE_HGRC % {b'hg_dir': self.hg_dir, 
               b'clone_dir': self.clone_dir, 
               b'test_server': self.TESTSERVER})
        self.options.parent_branch = None
        return

    def test_get_repository_info(self):
        """Testing MercurialClient.get_repository_info"""
        ri = self.client.get_repository_info()
        self.assertIsInstance(ri, RepositoryInfo)
        self.assertEqual(ri.base_path, b'')
        hgpath = ri.path
        if os.path.basename(hgpath) == b'.hg':
            hgpath = os.path.dirname(hgpath)
        self.assertEqual(self.hg_dir, hgpath)
        self.assertTrue(ri.supports_parent_diffs)
        self.assertFalse(ri.supports_changesets)

    def test_scan_for_server(self):
        """Testing MercurialClient.scan_for_server"""
        os.rename(self.clone_hgrc_path, os.path.join(self.clone_dir, b'._disabled_hgrc'))
        self.client.hgrc = {}
        self.client._load_hgrc()
        ri = self.client.get_repository_info()
        self.assertIsNone(self.client.scan_for_server(ri))

    def test_scan_for_server_when_present_in_hgrc(self):
        """Testing MercurialClient.scan_for_server when present in hgrc"""
        ri = self.client.get_repository_info()
        self.assertEqual(self.client.scan_for_server(ri), self.TESTSERVER)

    def test_scan_for_server_reviewboardrc(self):
        """Testing MercurialClient.scan_for_server when in .reviewboardrc"""
        with self.reviewboardrc({b'REVIEWBOARD_URL': self.TESTSERVER}):
            self.client.config = load_config()
            ri = self.client.get_repository_info()
            self.assertEqual(self.client.scan_for_server(ri), self.TESTSERVER)

    def test_diff(self):
        """Testing MercurialClient.diff"""
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'delete and modify stuff')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'68c2bdccf52a4f0baddd0ac9f2ecb7d2')

    def test_diff_with_multiple(self):
        """Testing MercurialClient.diff with multiple commits"""
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'9c8796936646be5c7349973b0fceacbd')

    def test_diff_with_exclude_patterns(self):
        """Testing MercurialClient.diff with exclude_patterns"""
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'exclude.txt', data=FOO2, msg=b'commit 2')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[b'exclude.txt'])
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'68c2bdccf52a4f0baddd0ac9f2ecb7d2')

    def test_diff_with_exclude_patterns_no_matches(self):
        """Testing MercurialClient.diff with exclude_patterns and no matched
        files
        """
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'empty.txt', data=b'', msg=b'commit 2')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[b'empty.txt'])
        self.assertIsInstance(revisions, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'68c2bdccf52a4f0baddd0ac9f2ecb7d2')

    def test_diff_with_diverged_branch(self):
        """Testing MercurialClient.diff with diverged branch"""
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.run_hg([b'branch', b'diverged'])
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'6b12723baab97f346aa938005bc4da4d')
        self.run_hg([b'update', b'-C', b'default'])
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'68c2bdccf52a4f0baddd0ac9f2ecb7d2')

    def test_diff_with_parent_diff(self):
        """Testing MercurialClient.diff with parent diffs"""
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3')
        revisions = self.client.parse_revision_spec([b'2', b'3'])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'parent_diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'7a897f68a9dc034fc1e42fe7a33bb808')
        self.assertEqual(md5(result[b'parent_diff']).hexdigest(), b'5cacbd79800a9145f982dcc0908b6068')

    def test_diff_with_parent_diff_and_diverged_branch(self):
        """Testing MercurialClient.diff with parent diffs and diverged branch
        """
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.run_hg([b'branch', b'diverged'])
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3')
        revisions = self.client.parse_revision_spec([b'2', b'3'])
        result = self.client.diff(revisions)
        self.assertIn(b'parent_diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'7a897f68a9dc034fc1e42fe7a33bb808')
        self.assertEqual(md5(result[b'parent_diff']).hexdigest(), b'5cacbd79800a9145f982dcc0908b6068')

    def test_diff_with_parent_diff_using_option(self):
        """Testing MercurialClient.diff with parent diffs using --parent"""
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3')
        self.options.parent_branch = b'2'
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'parent_diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'7a897f68a9dc034fc1e42fe7a33bb808')
        self.assertEqual(md5(result[b'parent_diff']).hexdigest(), b'5cacbd79800a9145f982dcc0908b6068')

    def test_parse_revision_spec_with_no_args(self):
        """Testing MercurialClient.parse_revision_spec with no arguments"""
        base = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        tip = self._hg_get_tip()
        revisions = self.client.parse_revision_spec([])
        self.assertIsInstance(revisions, dict)
        self.assertIn(b'base', revisions)
        self.assertIn(b'tip', revisions)
        self.assertNotIn(b'parent_base', revisions)
        self.assertEqual(revisions[b'base'], base)
        self.assertEqual(revisions[b'tip'], tip)

    def test_parse_revision_spec_with_one_arg_periods(self):
        """Testing MercurialClient.parse_revision_spec with r1..r2 syntax"""
        base = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        tip = self._hg_get_tip()
        revisions = self.client.parse_revision_spec([b'0..1'])
        self.assertIsInstance(revisions, dict)
        self.assertIn(b'base', revisions)
        self.assertIn(b'tip', revisions)
        self.assertNotIn(b'parent_base', revisions)
        self.assertEqual(revisions[b'base'], base)
        self.assertEqual(revisions[b'tip'], tip)

    def test_parse_revision_spec_with_one_arg_colons(self):
        """Testing MercurialClient.parse_revision_spec with r1::r2 syntax"""
        base = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        tip = self._hg_get_tip()
        revisions = self.client.parse_revision_spec([b'0..1'])
        self.assertIsInstance(revisions, dict)
        self.assertIn(b'base', revisions)
        self.assertIn(b'tip', revisions)
        self.assertNotIn(b'parent_base', revisions)
        self.assertEqual(revisions[b'base'], base)
        self.assertEqual(revisions[b'tip'], tip)

    def test_parse_revision_spec_with_one_arg(self):
        """Testing MercurialClient.parse_revision_spec with one revision"""
        base = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        tip = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        revisions = self.client.parse_revision_spec([b'1'])
        self.assertIsInstance(revisions, dict)
        self.assertIn(b'base', revisions)
        self.assertIn(b'tip', revisions)
        self.assertNotIn(b'parent_base', revisions)
        self.assertEqual(revisions[b'base'], base)
        self.assertEqual(revisions[b'tip'], tip)

    def test_parse_revision_spec_with_two_args(self):
        """Testing MercurialClient.parse_revision_spec with two revisions"""
        base = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        tip = self._hg_get_tip()
        revisions = self.client.parse_revision_spec([b'0', b'2'])
        self.assertIsInstance(revisions, dict)
        self.assertIn(b'base', revisions)
        self.assertIn(b'tip', revisions)
        self.assertNotIn(b'parent_base', revisions)
        self.assertEqual(revisions[b'base'], base)
        self.assertEqual(revisions[b'tip'], tip)

    def test_parse_revision_spec_with_parent_base(self):
        """Testing MercurialClient.parse_revision_spec with parent base"""
        start_base = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        commit1 = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2')
        commit2 = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3')
        commit3 = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO4, msg=b'commit 4')
        commit4 = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO5, msg=b'commit 5')
        self.assertEqual(self.client.parse_revision_spec([b'1', b'2']), {b'base': commit1, 
           b'tip': commit2, 
           b'parent_base': start_base})
        self.assertEqual(self.client.parse_revision_spec([b'4']), {b'base': commit3, 
           b'tip': commit4, 
           b'parent_base': start_base, 
           b'commit_id': commit4})
        self.assertEqual(self.client.parse_revision_spec([b'2', b'4']), {b'base': commit2, 
           b'tip': commit4, 
           b'parent_base': start_base})

    def test_get_hg_ref_type(self):
        """Testing MercurialClient.get_hg_ref_type"""
        self.hg_add_file_commit(branch=b'test-branch', bookmark=b'test-bookmark', tag=b'test-tag')
        tip = self._hg_get_tip()
        self.assertEqual(self.client.get_hg_ref_type(b'test-branch'), MercurialRefType.BRANCH)
        self.assertEqual(self.client.get_hg_ref_type(b'test-bookmark'), MercurialRefType.BOOKMARK)
        self.assertEqual(self.client.get_hg_ref_type(b'test-tag'), MercurialRefType.TAG)
        self.assertEqual(self.client.get_hg_ref_type(tip), MercurialRefType.REVISION)
        self.assertEqual(self.client.get_hg_ref_type(b'something-invalid'), MercurialRefType.UNKNOWN)

    def test_get_commit_message_with_one_commit_in_range(self):
        """Testing MercurialClient.get_commit_message with range containing
        only one commit
        """
        self.options.guess_summary = True
        self.options.guess_description = True
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1')
        revisions = self.client.parse_revision_spec([])
        commit_message = self.client.get_commit_message(revisions)
        self.assertEqual(commit_message[b'summary'], b'commit 1')

    def test_get_commit_message_with_commit_range(self):
        """Testing MercurialClient.get_commit_message with commit range"""
        self.options.guess_summary = True
        self.options.guess_description = True
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1\n\ndesc1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2\n\ndesc2')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3\n\ndesc3')
        revisions = self.client.parse_revision_spec([])
        commit_message = self.client.get_commit_message(revisions)
        self.assertEqual(commit_message[b'summary'], b'commit 1')
        self.assertEqual(commit_message[b'description'], b'desc1\n\ncommit 2\n\ndesc2\n\ncommit 3\n\ndesc3')

    def test_get_commit_message_with_specific_commit(self):
        """Testing MercurialClient.get_commit_message with specific commit"""
        self.options.guess_summary = True
        self.options.guess_description = True
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO1, msg=b'commit 1\n\ndesc1')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO2, msg=b'commit 2\n\ndesc2')
        tip = self._hg_get_tip()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO3, msg=b'commit 3\n\ndesc3')
        revisions = self.client.parse_revision_spec([tip])
        commit_message = self.client.get_commit_message(revisions)
        self.assertEqual(commit_message[b'summary'], b'commit 2')
        self.assertEqual(commit_message[b'description'], b'desc2')

    def test_create_commit_with_run_editor_true(self):
        """Testing MercurialClient.create_commit with run_editor set to True"""
        self.spy_on(self.client._execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'Test commit message.', author=self.AUTHOR, run_editor=True, files=[
         b'foo.txt'])
        self.assertTrue(self.client._execute.last_called_with([
         b'hg', b'commit', b'-m', b'TEST COMMIT MESSAGE.', b'-u',
         b'name <email>', b'foo.txt']))

    def test_create_commit_with_run_editor_false(self):
        """Testing MercurialClient.create_commit with run_editor set to False
        """
        self.spy_on(self.client._execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'Test commit message.', author=self.AUTHOR, run_editor=False, files=[
         b'foo.txt'])
        self.assertTrue(self.client._execute.last_called_with([
         b'hg', b'commit', b'-m', b'Test commit message.', b'-u',
         b'name <email>', b'foo.txt']))

    def test_create_commit_with_all_files_true(self):
        """Testing MercurialClient.create_commit with all_files set to True"""
        self.spy_on(self.client._execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'message', author=self.AUTHOR, run_editor=False, files=[], all_files=True)
        self.assertTrue(self.client._execute.last_called_with([
         b'hg', b'commit', b'-m', b'message', b'-u', b'name <email>', b'-A']))

    def test_create_commit_with_all_files_false(self):
        """Testing MercurialClient.create_commit with all_files set to False"""
        self.spy_on(self.client._execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'message', author=self.AUTHOR, run_editor=False, files=[
         b'foo.txt'], all_files=False)
        self.assertTrue(self.client._execute.last_called_with([
         b'hg', b'commit', b'-m', b'message', b'-u', b'name <email>',
         b'foo.txt']))

    def test_create_commit_with_empty_commit_message(self):
        """Testing MercurialClient.create_commit with empty commit message"""
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        message = b"A commit message wasn't provided. The patched files are in your tree but haven't been committed."
        with self.assertRaisesMessage(CreateCommitError, message):
            self.client.create_commit(message=b'', author=self.AUTHOR, run_editor=True, files=[
             b'foo.txt'])

    def test_create_commit_without_author(self):
        """Testing MercurialClient.create_commit without author information"""
        self.spy_on(self.client._execute)
        with open(b'foo.txt', b'w') as (fp):
            fp.write(b'change')
        self.client.create_commit(message=b'Test commit message.', author=None, run_editor=True, files=[
         b'foo.txt'])
        self.assertTrue(self.client._execute.last_called_with([
         b'hg', b'commit', b'-m', b'TEST COMMIT MESSAGE.', b'foo.txt']))
        return

    def test_merge_with_branch_and_close_branch_false(self):
        """Testing MercurialClient.merge with target branch and
        close_branch=False
        """
        self.hg_add_file_commit(branch=b'test-branch')
        self.spy_on(self.client._execute)
        self.client.merge(target=b'test-branch', destination=b'default', message=b'My merge commit', author=self.AUTHOR, close_branch=False)
        calls = self.client._execute.calls
        self.assertEqual(len(calls), 5)
        self.assertTrue(calls[0].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'bookmark(test-branch)']))
        self.assertTrue(calls[1].called_with([b'hg', b'branches', b'-q']))
        self.assertTrue(calls[2].called_with([b'hg', b'update', b'default']))
        self.assertTrue(calls[3].called_with([b'hg', b'merge', b'test-branch']))
        self.assertTrue(calls[4].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'-u', b'name <email>']))

    def test_merge_with_branch_and_close_branch_true(self):
        """Testing MercurialClient.merge with target branch and
        close_branch=True
        """
        self.hg_add_file_commit(branch=b'test-branch')
        self.spy_on(self.client._execute)
        self.client.merge(target=b'test-branch', destination=b'default', message=b'My merge commit', author=self.AUTHOR, close_branch=True)
        calls = self.client._execute.calls
        self.assertEqual(len(calls), 7)
        self.assertTrue(calls[0].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'bookmark(test-branch)']))
        self.assertTrue(calls[1].called_with([b'hg', b'branches', b'-q']))
        self.assertTrue(calls[2].called_with([b'hg', b'update', b'test-branch']))
        self.assertTrue(calls[3].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'--close-branch']))
        self.assertTrue(calls[4].called_with([b'hg', b'update', b'default']))
        self.assertTrue(calls[5].called_with([b'hg', b'merge', b'test-branch']))
        self.assertTrue(calls[6].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'-u', b'name <email>']))

    def test_merge_with_bookmark_and_close_branch_false(self):
        """Testing MercurialClient.merge with target bookmark and
        close_branch=False
        """
        self.run_hg([b'branch', b'feature-work'])
        self.hg_add_file_commit(bookmark=b'test-bookmark')
        self.spy_on(self.client._execute)
        self.client.merge(target=b'test-bookmark', destination=b'default', message=b'My merge commit', author=self.AUTHOR, close_branch=False)
        calls = self.client._execute.calls
        self.assertEqual(len(calls), 4)
        self.assertTrue(calls[0].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'bookmark(test-bookmark)']))
        self.assertTrue(calls[1].called_with([b'hg', b'update', b'default']))
        self.assertTrue(calls[2].called_with([b'hg', b'merge', b'test-bookmark']))
        self.assertTrue(calls[3].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'-u', b'name <email>']))

    def test_merge_with_bookmark_and_close_branch_true(self):
        """Testing MercurialClient.merge with target bookmark and
        close_branch=True
        """
        self.run_hg([b'branch', b'feature-work'])
        self.hg_add_file_commit(bookmark=b'test-bookmark')
        self.spy_on(self.client._execute)
        self.client.merge(target=b'test-bookmark', destination=b'default', message=b'My merge commit', author=self.AUTHOR, close_branch=True)
        calls = self.client._execute.calls
        self.assertEqual(len(calls), 5)
        self.assertTrue(calls[0].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'bookmark(test-bookmark)']))
        self.assertTrue(calls[1].called_with([b'hg', b'update', b'default']))
        self.assertTrue(calls[2].called_with([b'hg', b'merge', b'test-bookmark']))
        self.assertTrue(calls[3].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'-u', b'name <email>']))
        self.assertTrue(calls[4].called_with([b'hg', b'bookmark', b'-d',
         b'test-bookmark']))

    def test_merge_with_tag(self):
        """Testing MercurialClient.merge with target tag"""
        self.run_hg([b'branch', b'feature-work'])
        self.hg_add_file_commit(tag=b'test-tag')
        self.spy_on(self.client._execute)
        self.client.merge(target=b'test-tag', destination=b'default', message=b'My merge commit', author=self.AUTHOR, close_branch=True)
        calls = self.client._execute.calls
        self.assertEqual(len(calls), 6)
        self.assertTrue(calls[0].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'bookmark(test-tag)']))
        self.assertTrue(calls[1].called_with([b'hg', b'branches', b'-q']))
        self.assertTrue(calls[2].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'tag(test-tag)']))
        self.assertTrue(calls[3].called_with([b'hg', b'update', b'default']))
        self.assertTrue(calls[4].called_with([b'hg', b'merge', b'test-tag']))
        self.assertTrue(calls[5].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'-u', b'name <email>']))

    def test_merge_with_revision(self):
        """Testing MercurialClient.merge with target revision"""
        self.run_hg([b'branch', b'feature-work'])
        self.hg_add_file_commit()
        tip = self._hg_get_tip()
        self.spy_on(self.client._execute)
        self.client.merge(target=tip, destination=b'default', message=b'My merge commit', author=self.AUTHOR, close_branch=True)
        calls = self.client._execute.calls
        self.assertEqual(len(calls), 7)
        self.assertTrue(calls[0].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'bookmark(%s)' % tip]))
        self.assertTrue(calls[1].called_with([b'hg', b'branches', b'-q']))
        self.assertTrue(calls[2].called_with([b'hg', b'log', b'-ql1', b'-r',
         b'tag(%s)' % tip]))
        self.assertTrue(calls[3].called_with([b'hg', b'identify', b'-r', tip]))
        self.assertTrue(calls[4].called_with([b'hg', b'update', b'default']))
        self.assertTrue(calls[5].called_with([b'hg', b'merge', tip]))
        self.assertTrue(calls[6].called_with([b'hg', b'commit', b'-m',
         b'My merge commit',
         b'-u', b'name <email>']))

    def test_merge_with_invalid_target(self):
        """Testing MercurialClient.merge with an invalid target"""
        expected_message = b'Could not find a valid branch, tag, bookmark, or revision called "invalid".'
        with self.assertRaisesMessage(MergeError, expected_message):
            self.client.merge(target=b'invalid', destination=b'default', message=b'commit message', author=self.AUTHOR)

    def test_merge_with_invalid_destination(self):
        """Testing MercurialClient.merge with an invalid destination branch"""
        expected_message = b'Could not switch to branch "non-existent-branch".'
        with self.assertRaisesMessage(MergeError, expected_message):
            self.client.merge(target=b'default', destination=b'non-existent-branch', message=b'commit message', author=self.AUTHOR)

    def _hg_get_tip(self):
        """Return the revision at the tip of the branch.

        Returns:
            unicode:
            The tip revision.
        """
        return force_unicode(self.run_hg([b'identify']).split()[0])


class MercurialSubversionClientTests(MercurialTestBase):
    """Unit tests for hgsubversion."""
    TESTSERVER = b'http://127.0.0.1:8080'
    SVNSERVE_MAX_RETRIES = 12
    _svnserve_pid = None
    _svn_temp_base_path = None
    _skip_reason = None

    @classmethod
    def setUpClass(cls):
        for exe in ('svnadmin', 'svnserve', 'svn'):
            if not is_exe_in_path(exe):
                cls._skip_reason = b'%s is not available on the system.' % exe
                break
        else:
            has_hgsubversion = False
            try:
                output = execute([
                 b'hg', b'--config', b'extensions.hgsubversion=',
                 b'svn', b'--help'], ignore_errors=True, extra_ignore_errors=(255, ))
                has_hgsubversion = not re.search(b'unknown command [\'"]svn[\'"]', output, re.I)
            except OSError:
                has_hgsubversion = False

            if not has_hgsubversion:
                cls._skip_reason = b'hgsubversion is not available or cannot be used.'
            super(MercurialSubversionClientTests, cls).setUpClass()
            if cls._skip_reason:
                return
            temp_base_path = tempfile.mkdtemp(prefix=b'rbtools.')
            cls._svn_temp_base_path = temp_base_path
            svn_repo_path = os.path.join(temp_base_path, b'svnrepo')
            execute([b'svnadmin', b'create', svn_repo_path])
            svn_checkout_path = os.path.join(temp_base_path, b'checkout.svn')
            execute([b'svn', b'checkout', b'file://%s' % svn_repo_path,
             svn_checkout_path])
            os.chdir(svn_checkout_path)
            execute([b'svn', b'propset', b'reviewboard:url', cls.TESTSERVER,
             svn_checkout_path])
            execute([b'svn', b'mkdir', b'trunk', b'branches', b'tags'])
            execute([b'svn', b'commit', b'-m', b'Initial commit.'])
            os.chdir(os.path.join(svn_checkout_path, b'trunk'))
            for i, data in enumerate([FOO, FOO1, FOO2]):
                cls.svn_add_file_commit(filename=b'foo.txt', data=data, msg=b'Test commit %s' % i, add_file=i == 0)

            svnserve_port = os.environ.get(b'SVNSERVE_PORT') or str(randint(30000, 40000))
            pid_file = os.path.join(temp_base_path, b'svnserve.pid')
            execute([b'svnserve', b'--single-thread', b'--pid-file', pid_file, b'-d',
             b'--listen-port', svnserve_port, b'-r', temp_base_path])
            for i in range(0, cls.SVNSERVE_MAX_RETRIES):
                try:
                    cls._svnserve_pid = int(open(pid_file).read().strip())
                except (IOError, OSError):
                    time.sleep(0.25)

            if not cls._svnserve_pid:
                raise cls.failureException(b'Unable to launch svnserve on port %s' % svnserve_port)
            cls.svn_checkout_url = b'svn://127.0.0.1:%s/svnrepo' % svnserve_port

    @classmethod
    def tearDownClass(cls):
        if cls._svnserve_pid:
            os.kill(cls._svnserve_pid, 9)
        if cls._svn_temp_base_path:
            shutil.rmtree(cls._svn_temp_base_path, ignore_errors=True)
        super(MercurialSubversionClientTests, cls).tearDownClass()

    def setUp(self):
        super(MercurialSubversionClientTests, self).setUp()
        if self._skip_reason:
            raise SkipTest(self._skip_reason)
        home_dir = self.get_user_home()
        hgrc_path = os.path.join(home_dir, b'.hgrc')
        with open(hgrc_path, b'w') as (fp):
            fp.write(b'[extensions]\n')
            fp.write(b'hgsubversion =\n')
        try:
            self.clone_dir = os.path.join(home_dir, b'checkout.hg')
            self.run_hg([b'clone', b'--stream', self.svn_checkout_url,
             self.clone_dir])
        except (OSError, IOError) as e:
            self.fail(b'Unable to clone Subversion repository: %s' % e)

        os.chdir(self.clone_dir)
        self.options.parent_branch = None
        self.client = MercurialClient(options=self.options)
        return

    @classmethod
    def svn_add_file_commit(self, filename, data, msg, add_file=True):
        with open(filename, b'wb') as (fp):
            fp.write(data)
        if add_file:
            execute([b'svn', b'add', filename], ignore_errors=True)
        execute([b'svn', b'commit', b'-m', msg])

    def test_get_repository_info(self):
        """Testing MercurialClient.get_repository_info with SVN"""
        ri = self.client.get_repository_info()
        self.assertEqual(self.client._type, b'svn')
        self.assertEqual(ri.base_path, b'/trunk')
        self.assertEqual(ri.path, self.svn_checkout_url)

    def test_calculate_repository_info(self):
        """Testing MercurialClient._calculate_hgsubversion_repository_info
        with SVN determines repository and base paths
        """
        repo_info = self.client._calculate_hgsubversion_repository_info(b'URL: svn+ssh://testuser@svn.example.net/repo/trunk\nRepository Root: svn+ssh://testuser@svn.example.net/repo\nRepository UUID: bfddb570-5023-0410-9bc8-bc1659bf7c01\nRevision: 9999\nNode Kind: directory\nLast Changed Author: user\nLast Changed Rev: 9999\nLast Changed Date: 2012-09-05 18:04:28 +0000 (Wed, 05 Sep 2012)')
        self.assertEqual(repo_info.path, b'svn+ssh://svn.example.net/repo')
        self.assertEqual(repo_info.base_path, b'/trunk')

    def test_scan_for_server_with_reviewboardrc(self):
        """Testing MercurialClient.scan_for_server with SVN and configured
        .reviewboardrc
        """
        with self.reviewboardrc({b'REVIEWBOARD_URL': b'https://example.com/'}):
            self.client.config = load_config()
            ri = self.client.get_repository_info()
            self.assertEqual(self.client.scan_for_server(ri), b'https://example.com/')

    def test_scan_for_server_with_property(self):
        """Testing MercurialClient.scan_for_server with SVN and reviewboard:url
        property
        """
        ri = self.client.get_repository_info()
        self.assertEqual(self.client.scan_for_server(ri), self.TESTSERVER)

    def test_diff(self):
        """Testing MercurialClient.diff with SVN"""
        self.client.get_repository_info()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO4, msg=b'edit 4')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'2eb0a5f2149232c43a1745d90949fcd5')
        self.assertIsNone(result[b'parent_diff'])

    def test_diff_with_multiple_commits(self):
        """Testing MercurialClient.diff with SVN and multiple commits"""
        self.client.get_repository_info()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO4, msg=b'edit 4')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO5, msg=b'edit 5')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO6, msg=b'edit 6')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'3d007394de3831d61e477cbcfe60ece8')
        self.assertIsNone(result[b'parent_diff'])

    def test_diff_with_revision(self):
        """Testing MercurialClient.diff with SVN and specific revision"""
        self.client.get_repository_info()
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO4, msg=b'edit 4', branch=b'b')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO5, msg=b'edit 5', branch=b'b')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO6, msg=b'edit 6', branch=b'b')
        self.hg_add_file_commit(filename=b'foo.txt', data=FOO4, msg=b'edit 7', branch=b'b')
        revisions = self.client.parse_revision_spec([b'3'])
        result = self.client.diff(revisions)
        self.assertIsInstance(result, dict)
        self.assertIn(b'diff', result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'2eb0a5f2149232c43a1745d90949fcd5')
        self.assertIsNone(result[b'parent_diff'])