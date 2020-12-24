# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_hg.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, nose
from djblets.testing.decorators import add_fixtures
from reviewboard.scmtools.core import PRE_CREATION, Revision
from reviewboard.scmtools.errors import SCMError, FileNotFoundError
from reviewboard.scmtools.hg import HgDiffParser, HgGitDiffParser, HgTool
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.scmtools.tests.testcases import SCMTestCase
from reviewboard.testing import online_only
from reviewboard.testing.testcase import TestCase

class MercurialTests(SCMTestCase):
    """Unit tests for mercurial."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(MercurialTests, self).setUp()
        hg_repo_path = os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'hg_repo')
        self.repository = Repository(name=b'Test HG', path=hg_repo_path, tool=Tool.objects.get(name=b'Mercurial'))
        try:
            self.tool = self.repository.get_scmtool()
        except ImportError:
            raise nose.SkipTest(b'Hg is not installed')

    def _first_file_in_diff(self, diff):
        return self.tool.get_parser(diff).parse()[0]

    def test_ssh_disallowed(self):
        """Testing HgTool does not allow SSH URLs"""
        with self.assertRaises(SCMError):
            self.tool.check_repository(b'ssh://foo')

    def test_git_parser_selection_with_header(self):
        """Testing HgTool returns the git parser when a header is present"""
        diffContents = b'# HG changeset patch\n# Node ID 6187592a72d7\n# Parent  9d3f4147f294\ndiff --git a/emptyfile b/emptyfile\nnew file mode 100644\n'
        parser = self.tool.get_parser(diffContents)
        self.assertEqual(type(parser), HgGitDiffParser)

    def test_hg_parser_selection_with_header(self):
        """Testing HgTool returns the hg parser when a header is present"""
        diffContents = b'# HG changeset patch# Node ID 6187592a72d7\n# Parent  9d3f4147f294\ndiff -r 9d3f4147f294 -r 6187592a72d7 new.py\n--- /dev/null   Thu Jan 01 00:00:00 1970 +0000\n+++ b/new.py  Tue Apr 21 12:20:05 2015 -0400\n'
        parser = self.tool.get_parser(diffContents)
        self.assertEqual(type(parser), HgDiffParser)

    def test_git_parser_sets_commit_ids(self):
        """Testing HgGitDiffParser sets the parser commit ids"""
        diffContents = b'# HG changeset patch\n# Node ID 6187592a72d7\n# Parent  9d3f4147f294\ndiff --git a/emptyfile b/emptyfile\nnew file mode 100644\n'
        parser = self.tool.get_parser(diffContents)
        parser.parse()
        self.assertEqual(parser.new_commit_id, b'6187592a72d7')
        self.assertEqual(parser.base_commit_id, b'9d3f4147f294')

    def test_patch_creates_new_file(self):
        """Testing HgTool with a patch that creates a new file"""
        self.assertEqual(PRE_CREATION, self.tool.parse_diff_revision(b'/dev/null', b'bf544ea505f8')[1])

    def test_diff_parser_new_file(self):
        """Testing HgDiffParser with a diff that creates a new file"""
        diffContents = b'diff -r bf544ea505f8 readme\n--- /dev/null\n+++ b/readme\n'
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origFile, b'readme')

    def test_diff_parser_with_added_empty_file(self):
        """Testing HgDiffParser with a diff with an added empty file"""
        diff = b'diff -r 356a6127ef19 -r 4960455a8e88 empty\n--- /dev/null\n+++ b/empty\n'
        file = self._first_file_in_diff(diff)
        self.assertEqual(file.origInfo, PRE_CREATION)
        self.assertEqual(file.origFile, b'empty')
        self.assertEqual(file.newInfo, b'4960455a8e88')
        self.assertEqual(file.newFile, b'empty')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertEqual(file.insert_count, 0)
        self.assertEqual(file.delete_count, 0)

    def test_diff_parser_with_deleted_empty_file(self):
        """Testing HgDiffParser with a diff with a deleted empty file"""
        diff = b'diff -r 356a6127ef19 -r 4960455a8e88 empty\n--- a/empty\n+++ /dev/null\n'
        file = self._first_file_in_diff(diff)
        self.assertEqual(file.origInfo, b'356a6127ef19')
        self.assertEqual(file.origFile, b'empty')
        self.assertEqual(file.newInfo, b'4960455a8e88')
        self.assertEqual(file.newFile, b'empty')
        self.assertFalse(file.binary)
        self.assertTrue(file.deleted)
        self.assertEqual(file.insert_count, 0)
        self.assertEqual(file.delete_count, 0)

    def test_diff_parser_uncommitted(self):
        """Testing HgDiffParser with a diff with an uncommitted change"""
        diffContents = b'diff -r bf544ea505f8 readme\n--- a/readme\n+++ b/readme\n'
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origInfo, b'bf544ea505f8')
        self.assertEqual(file.origFile, b'readme')
        self.assertEqual(file.newInfo, b'Uncommitted')
        self.assertEqual(file.newFile, b'readme')

    def test_diff_parser_committed(self):
        """Testing HgDiffParser with a diff between committed revisions"""
        diffContents = b'diff -r 356a6127ef19 -r 4960455a8e88 readme\n--- a/readme\n+++ b/readme\n'
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origInfo, b'356a6127ef19')
        self.assertEqual(file.origFile, b'readme')
        self.assertEqual(file.newInfo, b'4960455a8e88')
        self.assertEqual(file.newFile, b'readme')

    def test_diff_parser_with_preamble_junk(self):
        """Testing HgDiffParser with a diff that contains non-diff junk test
        as a preamble
        """
        diffContents = b'changeset:   60:3613c58ad1d5\nuser:        Michael Rowe <mrowe@mojain.com>\ndate:        Fri Jul 27 11:44:37 2007 +1000\nfiles:       readme\ndescription:\nUpdate the readme file\n\n\ndiff -r 356a6127ef19 -r 4960455a8e88 readme\n--- a/readme\n+++ b/readme\n'
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origInfo, b'356a6127ef19')
        self.assertEqual(file.origFile, b'readme')
        self.assertEqual(file.newInfo, b'4960455a8e88')
        self.assertEqual(file.newFile, b'readme')

    def test_git_diff_parsing(self):
        """Testing HgDiffParser git diff support"""
        diffContents = b'# Node ID 4960455a8e88\n# Parent bf544ea505f8\ndiff --git a/path/to file/readme.txt b/new/path to/readme.txt\nrename from path/to file/readme.txt\nrename to new/path to/readme.txt\n--- a/path/to file/readme.txt\n+++ b/new/path to/readme.txt\n'
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origInfo, b'bf544ea505f8')
        self.assertEqual(file.origFile, b'path/to file/readme.txt')
        self.assertEqual(file.newInfo, b'4960455a8e88')
        self.assertEqual(file.newFile, b'new/path to/readme.txt')

    def test_diff_parser_unicode(self):
        """Testing HgDiffParser with unicode characters"""
        diffContents = (b'diff -r bf544ea505f8 réadme\n--- a/réadme\n+++ b/réadme\n').encode(b'utf-8')
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origInfo, b'bf544ea505f8')
        self.assertEqual(file.origFile, b'réadme')
        self.assertEqual(file.newInfo, b'Uncommitted')
        self.assertEqual(file.newFile, b'réadme')

    def test_git_diff_parsing_unicode(self):
        """Testing HgDiffParser git diff with unicode characters"""
        diffContents = (b'# Node ID 4960455a8e88\n# Parent bf544ea505f8\ndiff --git a/path/to file/réadme.txt b/new/path to/réadme.txt\nrename from path/to file/réadme.txt\nrename to new/path to/réadme.txt\n--- a/path/to file/réadme.txt\n+++ b/new/path to/réadme.txt\n').encode(b'utf-8')
        file = self._first_file_in_diff(diffContents)
        self.assertEqual(file.origInfo, b'bf544ea505f8')
        self.assertEqual(file.origFile, b'path/to file/réadme.txt')
        self.assertEqual(file.newInfo, b'4960455a8e88')
        self.assertEqual(file.newFile, b'new/path to/réadme.txt')

    def test_revision_parsing(self):
        """Testing HgDiffParser revision number parsing"""
        self.assertEqual(self.tool.parse_diff_revision(b'doc/readme', b'bf544ea505f8'), ('doc/readme',
                                                                                         'bf544ea505f8'))
        self.assertEqual(self.tool.parse_diff_revision(b'/dev/null', b'bf544ea505f8'), (
         b'/dev/null', PRE_CREATION))

    def test_get_branches(self):
        """Testing list of branches in HgClient.get_change"""
        value = self.tool.get_branches()
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0].id, b'default')
        self.assertEqual(value[0].commit, b'661e5dd3c4938ecbe8f77e2fdfa905d70485f94c')
        self.assertEqual(value[0].default, True)

    def test_get_change(self):
        """Testing raw diff of HgClient.get_change"""
        self.assertRaises(SCMError, lambda : self.tool.get_change(b'dummy'))
        value = self.tool.get_change(b'0')
        self.assertNotIn(b'goodbye', value.diff)
        self.assertEqual(value.id, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        value = self.tool.get_change(b'1')
        self.assertIn(b'goodbye', value.diff)
        self.assertEqual(value.id, b'661e5dd3c4938ecbe8f77e2fdfa905d70485f94c')

    def test_get_commits(self):
        """Testing commit objects in HgClient.get_commits"""
        value = self.tool.get_commits()
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)
        self.assertEqual(value[0].id, b'661e5dd3c4938ecbe8f77e2fdfa905d70485f94c')
        self.assertEqual(value[0].message, b'second')
        self.assertEqual(value[0].author_name, b'Michael Rowe <mike.rowe@nab.com.au>')
        self.assertEqual(value[0].date, b'2007-08-07T17:12:23')
        self.assertEqual(value[0].parent, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        self.assertEqual(value[0].base_commit_id, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        self.assertEqual(value[1].id, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        self.assertEqual(value[1].message, b'first')
        self.assertEqual(value[1].author_name, b'Michael Rowe <mike.rowe@nab.com.au>')
        self.assertEqual(value[1].date, b'2007-08-07T17:11:57')
        self.assertEqual(value[1].parent, b'0000000000000000000000000000000000000000')
        self.assertEqual(value[1].base_commit_id, b'0000000000000000000000000000000000000000')
        self.assertRaisesRegexp(SCMError, b'Cannot load commits: ', lambda : self.tool.get_commits(branch=b'x'))
        rev = b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786'
        value = self.tool.get_commits(start=rev)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

    def test_get_commits_with_non_utc_server_timezone(self):
        """Testing commit objects in HgClient.get_commits with
        settings.TIME_ZONE != UTC
        """
        old_tz = os.environ[b'TZ']
        os.environ[b'TZ'] = b'US/Pacific'
        try:
            value = self.tool.get_commits()
        finally:
            os.environ[b'TZ'] = old_tz

        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)
        self.assertEqual(value[0].id, b'661e5dd3c4938ecbe8f77e2fdfa905d70485f94c')
        self.assertEqual(value[0].message, b'second')
        self.assertEqual(value[0].author_name, b'Michael Rowe <mike.rowe@nab.com.au>')
        self.assertEqual(value[0].date, b'2007-08-07T17:12:23')
        self.assertEqual(value[0].parent, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        self.assertEqual(value[0].base_commit_id, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        self.assertEqual(value[1].id, b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786')
        self.assertEqual(value[1].message, b'first')
        self.assertEqual(value[1].author_name, b'Michael Rowe <mike.rowe@nab.com.au>')
        self.assertEqual(value[1].date, b'2007-08-07T17:11:57')
        self.assertEqual(value[1].parent, b'0000000000000000000000000000000000000000')
        self.assertEqual(value[1].base_commit_id, b'0000000000000000000000000000000000000000')
        self.assertRaisesRegexp(SCMError, b'Cannot load commits: ', lambda : self.tool.get_commits(branch=b'x'))
        rev = b'f814b6e226d2ba6d26d02ca8edbff91f57ab2786'
        value = self.tool.get_commits(start=rev)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

    def test_get_file(self):
        """Testing HgTool.get_file"""
        rev = Revision(b'661e5dd3c493')
        file = b'doc/readme'
        value = self.tool.get_file(file, rev)
        self.assertTrue(isinstance(value, bytes))
        self.assertEqual(value, b'Hello\n\ngoodbye\n')
        self.assertTrue(self.tool.file_exists(b'doc/readme', rev))
        self.assertTrue(not self.tool.file_exists(b'doc/readme2', rev))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b''))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b'hello', PRE_CREATION))

    def test_get_file_base_commit_id_override(self):
        """Testing base_commit_id overrides revision in HgTool.get_file"""
        base_commit_id = Revision(b'661e5dd3c493')
        bogus_rev = Revision(b'bogusrevision')
        file = b'doc/readme'
        value = self.tool.get_file(file, bogus_rev, base_commit_id=base_commit_id)
        self.assertTrue(isinstance(value, bytes))
        self.assertEqual(value, b'Hello\n\ngoodbye\n')
        self.assertTrue(self.tool.file_exists(b'doc/readme', bogus_rev, base_commit_id=base_commit_id))
        self.assertTrue(not self.tool.file_exists(b'doc/readme2', bogus_rev, base_commit_id=base_commit_id))

    def test_interface(self):
        """Testing basic HgTool API"""
        self.assertTrue(self.tool.diffs_use_absolute_paths)
        self.assertRaises(NotImplementedError, lambda : self.tool.get_changeset(1))

    @online_only
    def test_https_repo(self):
        """Testing HgTool.file_exists with an HTTPS-based repository"""
        repo = Repository(name=b'Test HG2', path=b'https://bitbucket.org/pypy/pypy', tool=Tool.objects.get(name=b'Mercurial'))
        tool = repo.get_scmtool()
        rev = Revision(b'877cf1960916')
        self.assertTrue(tool.file_exists(b'TODO.rst', rev))
        self.assertTrue(not tool.file_exists(b'TODO.rstNotFound', rev))


class HgAuthFormTests(TestCase):
    """Unit tests for HgTool's authentication form."""

    def test_fields(self):
        """Testing HgTool authentication form fields"""
        form = HgTool.create_auth_form()
        self.assertEqual(list(form.fields), [b'username', b'password'])
        self.assertEqual(form[b'username'].help_text, b'')
        self.assertEqual(form[b'username'].label, b'Username')
        self.assertEqual(form[b'password'].help_text, b'')
        self.assertEqual(form[b'password'].label, b'Password')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting HgTool authentication form load"""
        repository = self.create_repository(tool_name=b'Mercurial', username=b'test-user', password=b'test-pass')
        form = HgTool.create_auth_form(repository=repository)
        form.load()
        self.assertEqual(form[b'username'].value(), b'test-user')
        self.assertEqual(form[b'password'].value(), b'test-pass')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting HgTool authentication form save"""
        repository = self.create_repository(tool_name=b'Mercurial')
        form = HgTool.create_auth_form(repository=repository, data={b'username': b'test-user', 
           b'password': b'test-pass'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.username, b'test-user')
        self.assertEqual(repository.password, b'test-pass')


class HgRepositoryFormTests(TestCase):
    """Unit tests for HgTool's repository form."""

    def test_fields(self):
        """Testing HgTool repository form fields"""
        form = HgTool.create_repository_form()
        self.assertEqual(list(form.fields), [b'path', b'mirror_path'])
        self.assertEqual(form[b'path'].help_text, b'The path to the repository. This will generally be the URL you would use to check out the repository.')
        self.assertEqual(form[b'path'].label, b'Path')
        self.assertEqual(form[b'mirror_path'].help_text, b'')
        self.assertEqual(form[b'mirror_path'].label, b'Mirror Path')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting HgTool repository form load"""
        repository = self.create_repository(tool_name=b'Mercurial', path=b'https://hg.example.com/repo', mirror_path=b'https://hg.mirror.example.com/repo')
        form = HgTool.create_repository_form(repository=repository)
        form.load()
        self.assertEqual(form[b'path'].value(), b'https://hg.example.com/repo')
        self.assertEqual(form[b'mirror_path'].value(), b'https://hg.mirror.example.com/repo')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting HgTool repository form save"""
        repository = self.create_repository(tool_name=b'Mercurial')
        form = HgTool.create_repository_form(repository=repository, data={b'path': b'https://hg.example.com/repo', 
           b'mirror_path': b'https://hg.mirror.example.com/repo'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.path, b'https://hg.example.com/repo')
        self.assertEqual(repository.mirror_path, b'https://hg.mirror.example.com/repo')