# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_svn.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os
from hashlib import md5
import nose
from django.conf import settings
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency
from reviewboard.diffviewer.diffutils import patch
from reviewboard.scmtools.core import Branch, Commit, Revision, HEAD, PRE_CREATION
from reviewboard.scmtools.errors import SCMError, FileNotFoundError
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.scmtools.svn import SVNTool, recompute_svn_backend
from reviewboard.scmtools.svn.utils import collapse_svn_keywords, has_expanded_svn_keywords
from reviewboard.scmtools.tests.testcases import SCMTestCase
from reviewboard.testing.testcase import TestCase

class _CommonSVNTestCase(SpyAgency, SCMTestCase):
    """Common unit tests for Subversion.

    This is meant to be subclassed for each backend that wants to run
    the common set of tests.
    """
    backend = None
    backend_name = None
    fixtures = [b'test_scmtools']

    def setUp(self):
        super(_CommonSVNTestCase, self).setUp()
        self._old_backend_setting = settings.SVNTOOL_BACKENDS
        settings.SVNTOOL_BACKENDS = [self.backend]
        recompute_svn_backend()
        self.svn_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'svn_repo'))
        self.svn_ssh_path = b'svn+ssh://localhost%s' % self.svn_repo_path.replace(b'\\', b'/')
        self.repository = Repository(name=b'Subversion SVN', path=b'file://' + self.svn_repo_path, tool=Tool.objects.get(name=b'Subversion'))
        try:
            self.tool = self.repository.get_scmtool()
        except ImportError:
            raise nose.SkipTest(b'The %s backend could not be used. A dependency may be missing.' % self.backend)

        assert self.tool.client.__class__.__module__ == self.backend

    def tearDown(self):
        super(_CommonSVNTestCase, self).tearDown()
        settings.SVNTOOL_BACKENDS = self._old_backend_setting
        recompute_svn_backend()

    def shortDescription(self):
        desc = super(_CommonSVNTestCase, self).shortDescription()
        desc = desc.replace(b'<backend>', self.backend_name)
        return desc

    def test_ssh(self):
        """Testing SVN (<backend>) with a SSH-backed Subversion repository"""
        self._test_ssh(self.svn_ssh_path, b'trunk/doc/misc-docs/Makefile')

    def test_ssh_with_site(self):
        """Testing SVN (<backend>) with a SSH-backed Subversion repository
        with a LocalSite
        """
        self._test_ssh_with_site(self.svn_ssh_path, b'trunk/doc/misc-docs/Makefile')

    def test_get_file(self):
        """Testing SVN (<backend>) get_file"""
        expected = b'include ../tools/Makefile.base-vars\nNAME = misc-docs\nOUTNAME = svn-misc-docs\nINSTALL_DIR = $(DESTDIR)/usr/share/doc/subversion\ninclude ../tools/Makefile.base-rules\n'
        rev = Revision(b'2')
        file = b'trunk/doc/misc-docs/Makefile'
        value = self.tool.get_file(file, rev)
        self.assertTrue(isinstance(value, bytes))
        self.assertEqual(value, expected)
        self.assertEqual(self.tool.get_file(b'/' + file, rev), expected)
        self.assertEqual(self.tool.get_file(self.repository.path + b'/' + file, rev), expected)
        self.assertTrue(self.tool.file_exists(b'trunk/doc/misc-docs/Makefile'))
        self.assertTrue(not self.tool.file_exists(b'trunk/doc/misc-docs/Makefile2'))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b''))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b'hello', PRE_CREATION))

    def test_revision_parsing(self):
        """Testing SVN (<backend>) revision number parsing"""
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(working copy)')[1], HEAD)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'   (revision 0)')[1], PRE_CREATION)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(revision 1)')[1], b'1')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(revision 23)')[1], b'23')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'\t(revision 4)')[1], b'4')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'2007-06-06 15:32:23 UTC (rev 10958)')[1], b'10958')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(revision )')[1], PRE_CREATION)
        self.assertRaises(SCMError, lambda : self.tool.parse_diff_revision(b'', b'hello'))
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(revisión: 5)')[1], b'5')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(リビジョン 6)')[1], b'6')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(版本 7)')[1], b'7')

    def test_revision_parsing_with_nonexistent(self):
        """Testing SVN (<backend>) revision parsing with "(nonexistent)"
        revision indicator
        """
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(nonexistent)')[1], PRE_CREATION)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(nicht existent)')[1], PRE_CREATION)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(不存在的)')[1], PRE_CREATION)

    def test_revision_parsing_with_nonexistent_and_branches(self):
        """Testing SVN (<backend>) revision parsing with relocation
        information and nonexisitent revision specifier.
        """
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(.../trunk) (nonexistent)')[1], PRE_CREATION)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'(.../branches/branch-1.0)     (nicht existent)')[1], PRE_CREATION)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'        (.../trunk)     (不存在的)')[1], PRE_CREATION)

    def test_interface(self):
        """Testing SVN (<backend>) with basic SVNTool API"""
        self.assertFalse(self.tool.diffs_use_absolute_paths)
        self.assertRaises(NotImplementedError, lambda : self.tool.get_changeset(1))

    def test_binary_diff(self):
        """Testing SVN (<backend>) parsing SVN diff with binary file"""
        diff = b'Index: binfile\n===================================================================\nCannot display: file marked as a binary type.\nsvn:mime-type = application/octet-stream\n'
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'binfile')
        self.assertEqual(file.binary, True)

    def test_binary_diff_with_property_change(self):
        """Testing SVN (<backend>) parsing SVN diff with binary file with
        property change
        """
        diff = b'Index: binfile\n===================================================================\nCannot display: file marked as a binary type.\nsvn:mime-type = application/octet-stream\n\nProperty changes on: binfile\n___________________________________________________________________\nAdded: svn:mime-type\n## -0,0 +1 ##\n+application/octet-stream\n\\ No newline at end of property\n'
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'binfile')
        self.assertTrue(file.binary)

    def test_keyword_diff(self):
        """Testing SVN (<backend>) parsing diff with keywords"""
        diff = b'Index: Makefile\n===================================================================\n--- Makefile    (revision 4)\n+++ Makefile    (working copy)\n@@ -1,6 +1,7 @@\n # $Id$\n # $Rev$\n # $Revision::     $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n'
        filename = b'trunk/doc/misc-docs/Makefile'
        rev = Revision(b'4')
        file = self.tool.get_file(filename, rev)
        patch(diff, file, filename)

    def test_unterminated_keyword_diff(self):
        """Testing SVN (<backend>) parsing diff with unterminated keywords"""
        diff = b'Index: Makefile\n===================================================================\n--- Makefile    (revision 4)\n+++ Makefile    (working copy)\n@@ -1,6 +1,7 @@\n # $Id$\n # $Id:\n # $Rev$\n # $Revision::     $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n'
        filename = b'trunk/doc/misc-docs/Makefile'
        rev = Revision(b'5')
        file = self.tool.get_file(filename, rev)
        patch(diff, file, filename)

    def test_svn16_property_diff(self):
        """Testing SVN (<backend>) parsing SVN 1.6 diff with property changes
        """
        prop_diff = b'Index:\n===================================================================\n--- (revision 123)\n+++ (working copy)\nProperty changes on: .\n___________________________________________________________________\nModified: reviewboard:url\n## -1 +1 ##\n-http://reviews.reviewboard.org\n+http://reviews.reviewboard.org\n'
        bin_diff = b'Index: binfile\n===================================================================\nCannot display: file marked as a binary type.\nsvn:mime-type = application/octet-stream\n'
        diff = prop_diff + bin_diff
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'binfile')
        self.assertTrue(files[0].binary)
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)

    def test_svn17_property_diff(self):
        """Testing SVN (<backend>) parsing SVN 1.7+ diff with property changes
        """
        prop_diff = b'Index .:\n===================================================================\n--- .  (revision 123)\n+++ .  (working copy)\n\nProperty changes on: .\n___________________________________________________________________\nModified: reviewboard:url\n## -0,0 +1,3 ##\n-http://reviews.reviewboard.org\n+http://reviews.reviewboard.org\nAdded: myprop\n## -0,0 +1 ##\n+Property test.\n'
        bin_diff = b'Index: binfile\n===================================================================\nCannot display: file marked as a binary type.\nsvn:mime-type = application/octet-stream\n'
        diff = prop_diff + bin_diff
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'binfile')
        self.assertTrue(files[0].binary)
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)

    def test_unicode_diff(self):
        """Testing SVN (<backend>) parsing diff with unicode characters"""
        diff = (b'Index: Filé\n===================================================================\n--- Filé    (revision 4)\n+++ Filé    (working copy)\n@@ -1,6 +1,7 @@\n+# foó\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n').encode(b'utf-8')
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'Filé')
        self.assertFalse(files[0].binary)
        self.assertEqual(files[0].insert_count, 1)
        self.assertEqual(files[0].delete_count, 0)

    def test_diff_with_spaces_in_filenames(self):
        """Testing SVN (<backend>) parsing diff with spaces in filenames"""
        diff = b'Index: File with spaces\n===================================================================\n--- File with spaces    (revision 4)\n+++ File with spaces    (working copy)\n@@ -1,6 +1,7 @@\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'File with spaces')
        self.assertFalse(files[0].binary)
        self.assertEqual(files[0].insert_count, 1)
        self.assertEqual(files[0].delete_count, 0)

    def test_diff_with_added_empty_file(self):
        """Testing parsing SVN diff with added empty file"""
        diff = b'Index: empty-file\t(added)\n===================================================================\n--- empty-file\t(revision 0)\n+++ empty-file\t(revision 0)\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'empty-file')
        self.assertEqual(files[0].newFile, b'empty-file')
        self.assertEqual(files[0].origInfo, b'(revision 0)')
        self.assertEqual(files[0].newInfo, b'(revision 0)')
        self.assertFalse(files[0].binary)
        self.assertFalse(files[0].deleted)
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)

    def test_diff_with_deleted_empty_file(self):
        """Testing parsing SVN diff with deleted empty file"""
        diff = b'Index: empty-file\t(deleted)\n===================================================================\n--- empty-file\t(revision 4)\n+++ empty-file\t(working copy)\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'empty-file')
        self.assertEqual(files[0].newFile, b'empty-file')
        self.assertEqual(files[0].origInfo, b'(revision 4)')
        self.assertEqual(files[0].newInfo, b'(working copy)')
        self.assertFalse(files[0].binary)
        self.assertTrue(files[0].deleted)
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)

    def test_idea_diff(self):
        """Testing parsing SVN diff with multi-file diff generated by IDEA
        IDEs
        """
        diff1 = b'Index: path/to/README\nIDEA additional info:\nSubsystem: org.reviewboard.org.test\n<+>ISO-8859-1\n===================================================================\n--- path/to/README\t(revision 4)\n+++ path/to/README\t(revision )\n@@ -1,6 +1,7 @@\n #\n #\n #\n+# test\n #\n #\n #\n'
        diff2 = b'Index: path/to/README2\nIDEA additional info:\nSubsystem: org.reviewboard.org.test\n<+>ISO-8859-1\n===================================================================\n--- path/to/README2\t(revision 4)\n+++ path/to/README2\t(revision )\n@@ -1,6 +1,7 @@\n #\n #\n #\n+# test\n #\n #\n #\n'
        diff_files = self.tool.get_parser(diff1 + diff2).parse()
        self.assertEqual(len(diff_files), 2)
        diff_file = diff_files[1]
        self.assertEqual(diff_file.origFile, b'path/to/README2')
        self.assertEqual(diff_file.newFile, b'path/to/README2')
        self.assertEqual(diff_file.origInfo, b'(revision 4)')
        self.assertEqual(diff_file.newInfo, b'(revision )')
        self.assertFalse(diff_file.binary)
        self.assertFalse(diff_file.deleted)
        self.assertEqual(diff_file.insert_count, 1)
        self.assertEqual(diff_file.delete_count, 0)
        self.assertEqual(diff_file.data, diff2)

    def test_get_branches(self):
        """Testing SVN (<backend>) get_branches"""
        branches = self.tool.get_branches()
        self.assertEqual(len(branches), 3)
        self.assertEqual(branches[0], Branch(id=b'trunk', name=b'trunk', commit=b'9', default=True))
        self.assertEqual(branches[1], Branch(id=b'branches/branch1', name=b'branch1', commit=b'7', default=False))
        self.assertEqual(branches[2], Branch(id=b'top-level-branch', name=b'top-level-branch', commit=b'10', default=False))

    def test_get_commits(self):
        """Testing SVN (<backend>) get_commits"""
        commits = self.tool.get_commits(start=b'5')
        self.assertEqual(len(commits), 5)
        self.assertEqual(commits[0], Commit(b'chipx86', b'5', b'2010-05-21T09:33:40.893946', b'Add an unterminated keyword for testing bug #1523\n', b'4'))
        commits = self.tool.get_commits(start=b'7')
        self.assertEqual(len(commits), 7)
        self.assertEqual(commits[1], Commit(b'david', b'6', b'2013-06-13T07:43:04.725088', b'Add a branches directory', b'5'))

    def test_get_commits_with_branch(self):
        """Testing SVN (<backend>) get_commits with branch"""
        commits = self.tool.get_commits(branch=b'/branches/branch1', start=b'5')
        self.assertEqual(len(commits), 5)
        self.assertEqual(commits[0], Commit(b'chipx86', b'5', b'2010-05-21T09:33:40.893946', b'Add an unterminated keyword for testing bug #1523\n', b'4'))
        commits = self.tool.get_commits(branch=b'/branches/branch1', start=b'7')
        self.assertEqual(len(commits), 6)
        self.assertEqual(commits[0], Commit(b'david', b'7', b'2013-06-13T07:43:27.259554', b'Add a branch', b'5'))
        self.assertEqual(commits[1], Commit(b'chipx86', b'5', b'2010-05-21T09:33:40.893946', b'Add an unterminated keyword for testing bug #1523\n', b'4'))

    def test_get_commits_with_no_date(self):
        """Testing SVN (<backend>) get_commits with no date in commit"""

        def _get_log(*args, **kwargs):
            return [
             {b'author': b'chipx86', 
                b'revision': b'5', 
                b'message': b'Commit 1'}]

        self.spy_on(self.tool.client.get_log, _get_log)
        commits = self.tool.get_commits(start=b'5')
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0], Commit(b'chipx86', b'5', b'', b'Commit 1'))

    def test_get_commits_with_exception(self):
        """Testing SVN (<backend>) get_commits with exception"""

        def _get_log(*args, **kwargs):
            raise Exception(b'Bad things happened')

        self.spy_on(self.tool.client.get_log, _get_log)
        with self.assertRaisesMessage(SCMError, b'Bad things happened'):
            self.tool.get_commits(start=b'5')

    def test_get_change(self):
        """Testing SVN (<backend>) get_change"""
        commit = self.tool.get_change(b'5')
        self.assertEqual(md5(commit.message.encode(b'utf-8')).hexdigest(), b'928336c082dd756e3f7af4cde4724ebf')
        self.assertEqual(md5(commit.diff).hexdigest(), b'56e50374056931c03a333f234fa63375')

    def test_utf8_keywords(self):
        """Testing SVN (<backend>) with UTF-8 files with keywords"""
        self.repository.get_file(b'trunk/utf8-file.txt', b'9')

    def test_normalize_patch_with_svn_and_expanded_keywords(self):
        """Testing SVN (<backend>) normalize_patch with expanded keywords"""
        diff = b'Index: Makefile\n===================================================================\n--- Makefile    (revision 4)\n+++ Makefile    (working copy)\n@@ -1,6 +1,7 @@\n # $Id$\n # $Rev: 123$\n # $Revision:: 123   $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n'
        normalized = self.tool.normalize_patch(patch=diff, filename=b'trunk/doc/misc-docs/Makefile', revision=b'4')
        self.assertEqual(normalized, b'Index: Makefile\n===================================================================\n--- Makefile    (revision 4)\n+++ Makefile    (working copy)\n@@ -1,6 +1,7 @@\n # $Id$\n # $Rev$\n # $Revision::       $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n')

    def test_normalize_patch_with_svn_and_no_expanded_keywords(self):
        """Testing SVN (<backend>) normalize_patch with no expanded keywords"""
        diff = b'Index: Makefile\n===================================================================\n--- Makefile    (revision 4)\n+++ Makefile    (working copy)\n@@ -1,6 +1,7 @@\n # $Id$\n # $Rev$\n # $Revision::    $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n'
        normalized = self.tool.normalize_patch(patch=diff, filename=b'trunk/doc/misc-docs/Makefile', revision=b'4')
        self.assertEqual(normalized, b'Index: Makefile\n===================================================================\n--- Makefile    (revision 4)\n+++ Makefile    (working copy)\n@@ -1,6 +1,7 @@\n # $Id$\n # $Rev$\n # $Revision::    $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = svn-misc-docs\n')


class PySVNTests(_CommonSVNTestCase):
    backend = b'reviewboard.scmtools.svn.pysvn'
    backend_name = b'pysvn'


class SubvertpyTests(_CommonSVNTestCase):
    backend = b'reviewboard.scmtools.svn.subvertpy'
    backend_name = b'subvertpy'


class UtilsTests(SCMTestCase):
    """Unit tests for reviewboard.scmtools.svn.utils."""

    def test_collapse_svn_keywords(self):
        """Testing collapse_svn_keywords"""
        keyword_test_data = [
         ('Id', '/* $Id: test2.c 3 2014-08-04 22:55:09Z david $ */', '/* $Id$ */'),
         ('id', '/* $Id: test2.c 3 2014-08-04 22:55:09Z david $ */', '/* $Id$ */'),
         ('id', '/* $id: test2.c 3 2014-08-04 22:55:09Z david $ */', '/* $id$ */'),
         ('Id', '/* $id: test2.c 3 2014-08-04 22:55:09Z david $ */', '/* $id$ */')]
        for keyword, data, result in keyword_test_data:
            self.assertEqual(collapse_svn_keywords(data, keyword), result)

    def test_has_expanded_svn_keywords(self):
        """Testing has_expanded_svn_keywords"""
        self.assertTrue(has_expanded_svn_keywords(b'.. $ID: 123$ ..'))
        self.assertTrue(has_expanded_svn_keywords(b'.. $id::  123$ ..'))
        self.assertFalse(has_expanded_svn_keywords(b'.. $Id::   $ ..'))
        self.assertFalse(has_expanded_svn_keywords(b'.. $Id$ ..'))
        self.assertFalse(has_expanded_svn_keywords(b'.. $Id ..'))
        self.assertFalse(has_expanded_svn_keywords(b'.. $Id Here$ ..'))


class SVNAuthFormTests(TestCase):
    """Unit tests for SVNTool's authentication form."""

    def test_fields(self):
        """Testing SVNTool authentication form fields"""
        form = SVNTool.create_auth_form()
        self.assertEqual(list(form.fields), [b'username', b'password'])
        self.assertEqual(form[b'username'].help_text, b'')
        self.assertEqual(form[b'username'].label, b'Username')
        self.assertEqual(form[b'password'].help_text, b'')
        self.assertEqual(form[b'password'].label, b'Password')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting SVNTool authentication form load"""
        repository = self.create_repository(tool_name=b'Subversion', username=b'test-user', password=b'test-pass')
        form = SVNTool.create_auth_form(repository=repository)
        form.load()
        self.assertEqual(form[b'username'].value(), b'test-user')
        self.assertEqual(form[b'password'].value(), b'test-pass')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting SVNTool authentication form save"""
        repository = self.create_repository(tool_name=b'Subversion')
        form = SVNTool.create_auth_form(repository=repository, data={b'username': b'test-user', 
           b'password': b'test-pass'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.username, b'test-user')
        self.assertEqual(repository.password, b'test-pass')


class SVNRepositoryFormTests(TestCase):
    """Unit tests for SVNTool's repository form."""

    def test_fields(self):
        """Testing SVNTool repository form fields"""
        form = SVNTool.create_repository_form()
        self.assertEqual(list(form.fields), [b'path', b'mirror_path'])
        self.assertEqual(form[b'path'].help_text, b'The path to the repository. This will generally be the URL you would use to check out the repository.')
        self.assertEqual(form[b'path'].label, b'Path')
        self.assertEqual(form[b'mirror_path'].help_text, b'')
        self.assertEqual(form[b'mirror_path'].label, b'Mirror Path')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting SVNTool repository form load"""
        repository = self.create_repository(tool_name=b'Subversion', path=b'https://svn.example.com/', mirror_path=b'https://svn.mirror.example.com')
        form = SVNTool.create_repository_form(repository=repository)
        form.load()
        self.assertEqual(form[b'path'].value(), b'https://svn.example.com/')
        self.assertEqual(form[b'mirror_path'].value(), b'https://svn.mirror.example.com')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting SVNTool repository form save"""
        repository = self.create_repository(tool_name=b'Subversion')
        form = SVNTool.create_repository_form(repository=repository, data={b'path': b'https://svn.example.com/', 
           b'mirror_path': b'https://svn.mirror.example.com'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.path, b'https://svn.example.com/')
        self.assertEqual(repository.mirror_path, b'https://svn.mirror.example.com')