# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_git.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, nose
from django.utils import six
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency
from reviewboard.diffviewer.parser import DiffParserError
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.scmtools.errors import SCMError, FileNotFoundError
from reviewboard.scmtools.git import ShortSHA1Error, GitClient, GitTool
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.scmtools.tests.testcases import SCMTestCase
from reviewboard.testing.testcase import TestCase

class GitTests(SpyAgency, SCMTestCase):
    """Unit tests for Git."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(GitTests, self).setUp()
        tool = Tool.objects.get(name=b'Git')
        self.local_repo_path = os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'git_repo')
        self.git_ssh_path = b'localhost:%s' % self.local_repo_path.replace(b'\\', b'/')
        remote_repo_path = b'git@github.com:reviewboard/reviewboard.git'
        remote_repo_raw_url = b'http://github.com/api/v2/yaml/blob/show/reviewboard/reviewboard/<revision>'
        self.repository = Repository(name=b'Git test repo', path=self.local_repo_path, tool=tool)
        self.remote_repository = Repository(name=b'Remote Git test repo', path=remote_repo_path, raw_file_url=remote_repo_raw_url, tool=tool)
        try:
            self.tool = self.repository.get_scmtool()
            self.remote_tool = self.remote_repository.get_scmtool()
        except ImportError:
            raise nose.SkipTest(b'git binary not found')

    def _read_fixture(self, filename):
        filename = os.path.join(os.path.dirname(__file__), b'..', b'testdata', filename)
        with open(filename, b'rb') as (f):
            return f.read()

    def _get_file_in_diff(self, diff, filenum=0):
        files = self.tool.get_parser(diff).parse()
        self.assertTrue(filenum < len(files))
        return files[filenum]

    def test_ssh(self):
        """Testing a SSH-backed git repository"""
        self._test_ssh(self.git_ssh_path)

    def test_ssh_with_site(self):
        """Testing a SSH-backed git repository with a LocalSite"""
        self._test_ssh_with_site(self.git_ssh_path)

    def test_filemode_diff(self):
        """Testing parsing filemode changes Git diff"""
        diff = self._read_fixture(b'git_filemode.diff')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'testing')
        self.assertEqual(file.newFile, b'testing')
        self.assertEqual(file.origInfo, b'e69de29')
        self.assertEqual(file.newInfo, b'bcae657')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        self.assertEqual(file.data.splitlines()[0], b'diff --git a/testing b/testing')
        self.assertEqual(file.data.splitlines()[(-1)], b'+ADD')
        self.assertEqual(file.insert_count, 1)
        self.assertEqual(file.delete_count, 0)

    def test_filemode_with_following_diff(self):
        """Testing parsing filemode changes with following Git diff"""
        diff = self._read_fixture(b'git_filemode2.diff')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'testing')
        self.assertEqual(file.newFile, b'testing')
        self.assertEqual(file.origInfo, b'e69de29')
        self.assertEqual(file.newInfo, b'bcae657')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        self.assertEqual(file.data.splitlines()[0], b'diff --git a/testing b/testing')
        self.assertEqual(file.data.splitlines()[(-1)], b'+ADD')
        self.assertEqual(file.insert_count, 1)
        self.assertEqual(file.delete_count, 0)
        file = self._get_file_in_diff(diff, 1)
        self.assertEqual(file.origFile, b'cfg/testcase.ini')
        self.assertEqual(file.newFile, b'cfg/testcase.ini')
        self.assertEqual(file.origInfo, b'cc18ec8')
        self.assertEqual(file.newInfo, b'5e70b73')
        self.assertEqual(file.data.splitlines()[0], b'diff --git a/cfg/testcase.ini b/cfg/testcase.ini')
        self.assertEqual(file.data.splitlines()[(-1)], b'+db = pyunit')
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_simple_diff(self):
        """Testing parsing simple Git diff"""
        diff = self._read_fixture(b'git_simple.diff')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'cfg/testcase.ini')
        self.assertEqual(file.newFile, b'cfg/testcase.ini')
        self.assertEqual(file.origInfo, b'cc18ec8')
        self.assertEqual(file.newInfo, b'5e70b73')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        self.assertEqual(len(file.data), 249)
        self.assertEqual(file.data.splitlines()[0], b'diff --git a/cfg/testcase.ini b/cfg/testcase.ini')
        self.assertEqual(file.data.splitlines()[(-1)], b'+db = pyunit')
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_diff_with_unicode(self):
        """Testing parsing Git diff with unicode characters"""
        diff = (b'diff --git a/cfg/téstcase.ini b/cfg/téstcase.ini\nindex cc18ec8..5e70b73 100644\n--- a/cfg/téstcase.ini\n+++ b/cfg/téstcase.ini\n@@ -1,6 +1,7 @@\n+blah blah blah\n [mysql]\n hóst = localhost\n pórt = 3306\n user = user\n pass = pass\n-db = pyunít\n+db = pyunít\n').encode(b'utf-8')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'cfg/téstcase.ini')
        self.assertEqual(file.newFile, b'cfg/téstcase.ini')
        self.assertEqual(file.origInfo, b'cc18ec8')
        self.assertEqual(file.newInfo, b'5e70b73')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        self.assertEqual(file.data.splitlines()[0].decode(b'utf-8'), b'diff --git a/cfg/téstcase.ini b/cfg/téstcase.ini')
        self.assertEqual(file.data.splitlines()[(-1)].decode(b'utf-8'), b'+db = pyunít')
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_diff_with_tabs_after_filename(self):
        """Testing parsing Git diffs with tabs after the filename"""
        diff = b'diff --git a/README b/README\nindex 712544e4343bf04967eb5ea80257f6c64d6f42c7..f88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1 100644\n--- a/README\t\n+++ b/README\t\n@ -1,1 +1,1 @@\n-blah blah\n+blah\n-\n1.7.1\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(files[0].origFile, b'README')
        self.assertEqual(files[0].newFile, b'README')
        self.assertEqual(files[0].origInfo, b'712544e4343bf04967eb5ea80257f6c64d6f42c7')
        self.assertEqual(files[0].newInfo, b'f88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1')
        self.assertEqual(files[0].data, diff)
        self.assertEqual(files[0].insert_count, 1)
        self.assertEqual(files[0].delete_count, 2)

    def test_new_file_diff(self):
        """Testing parsing Git diff with new file"""
        diff = self._read_fixture(b'git_newfile.diff')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'IAMNEW')
        self.assertEqual(file.newFile, b'IAMNEW')
        self.assertEqual(file.origInfo, PRE_CREATION)
        self.assertEqual(file.newInfo, b'e69de29')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        self.assertEqual(len(file.data), 123)
        self.assertEqual(file.data.splitlines()[0], b'diff --git a/IAMNEW b/IAMNEW')
        self.assertEqual(file.data.splitlines()[(-1)], b'+Hello')
        self.assertEqual(file.insert_count, 1)
        self.assertEqual(file.delete_count, 0)

    def test_new_file_no_content_diff(self):
        """Testing parsing Git diff new file, no content"""
        diff = self._read_fixture(b'git_newfile_nocontent.diff')
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'newfile')
        self.assertEqual(file.newFile, b'newfile')
        self.assertEqual(file.origInfo, PRE_CREATION)
        self.assertEqual(file.newInfo, b'e69de29')
        self.assertFalse(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        lines = file.data.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], b'diff --git a/newfile b/newfile')
        self.assertEqual(file.insert_count, 0)
        self.assertEqual(file.delete_count, 0)

    def test_new_file_no_content_with_following_diff(self):
        """Testing parsing Git diff new file, no content, with following"""
        diff = self._read_fixture(b'git_newfile_nocontent2.diff')
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].origFile, b'newfile')
        self.assertEqual(files[0].newFile, b'newfile')
        self.assertEqual(files[0].origInfo, PRE_CREATION)
        self.assertEqual(files[0].newInfo, b'e69de29')
        self.assertFalse(files[0].binary)
        self.assertFalse(files[0].deleted)
        self.assertFalse(files[0].is_symlink)
        lines = files[0].data.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], b'diff --git a/newfile b/newfile')
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)
        self.assertEqual(files[1].origFile, b'cfg/testcase.ini')
        self.assertEqual(files[1].newFile, b'cfg/testcase.ini')
        self.assertEqual(files[1].origInfo, b'cc18ec8')
        self.assertEqual(files[1].newInfo, b'5e70b73')
        lines = files[1].data.splitlines()
        self.assertEqual(len(lines), 13)
        self.assertEqual(lines[0], b'diff --git a/cfg/testcase.ini b/cfg/testcase.ini')
        self.assertEqual(lines[(-1)], b'+db = pyunit')
        self.assertEqual(files[1].insert_count, 2)
        self.assertEqual(files[1].delete_count, 1)

    def test_del_file_diff(self):
        """Testing parsing Git diff with deleted file"""
        diff = self._read_fixture(b'git_delfile.diff')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'OLDFILE')
        self.assertEqual(file.newFile, b'OLDFILE')
        self.assertEqual(file.origInfo, b'8ebcb01')
        self.assertEqual(file.newInfo, b'0000000')
        self.assertFalse(file.binary)
        self.assertTrue(file.deleted)
        self.assertFalse(file.is_symlink)
        self.assertEqual(len(file.data), 132)
        self.assertEqual(file.data.splitlines()[0], b'diff --git a/OLDFILE b/OLDFILE')
        self.assertEqual(file.data.splitlines()[(-1)], b'-Goodbye')
        self.assertEqual(file.insert_count, 0)
        self.assertEqual(file.delete_count, 1)

    def test_del_file_no_content_diff(self):
        """Testing parsing Git diff with deleted file, no content"""
        diff = b'diff --git a/empty b/empty\ndeleted file mode 100644\nindex e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..0000000000000000000000000000000000000000\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'empty')
        self.assertEqual(files[0].newFile, b'empty')
        self.assertEqual(files[0].origInfo, b'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')
        self.assertEqual(files[0].newInfo, b'0000000000000000000000000000000000000000')
        self.assertFalse(files[0].binary)
        self.assertTrue(files[0].deleted)
        self.assertFalse(files[0].is_symlink)
        self.assertEqual(len(files[0].data), 141)
        self.assertEqual(files[0].data.splitlines()[0], b'diff --git a/empty b/empty')
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)

    def test_del_file_no_content_with_following_diff(self):
        """Testing parsing Git diff with deleted file, no content, with
        following
        """
        diff = b'diff --git a/empty b/empty\ndeleted file mode 100644\nindex e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..0000000000000000000000000000000000000000\ndiff --git a/foo/bar b/foo/bar\nindex 484ba93ef5b0aed5b72af8f4e9dc4cfd10ef1a81..0ae4095ddfe7387d405bd53bd59bbb5d861114c5 100644\n--- a/foo/bar\n+++ b/foo/bar\n@@ -1 +1,2 @@\n+Hello!\nblah\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].origFile, b'empty')
        self.assertEqual(files[0].newFile, b'empty')
        self.assertEqual(files[0].origInfo, b'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')
        self.assertEqual(files[0].newInfo, b'0000000000000000000000000000000000000000')
        self.assertFalse(files[0].binary)
        self.assertTrue(files[0].deleted)
        self.assertFalse(files[0].is_symlink)
        self.assertEqual(len(files[0].data), 141)
        self.assertEqual(files[0].data.splitlines()[0], b'diff --git a/empty b/empty')
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)
        self.assertEqual(files[1].origFile, b'foo/bar')
        self.assertEqual(files[1].newFile, b'foo/bar')
        self.assertEqual(files[1].origInfo, b'484ba93ef5b0aed5b72af8f4e9dc4cfd10ef1a81')
        self.assertEqual(files[1].newInfo, b'0ae4095ddfe7387d405bd53bd59bbb5d861114c5')
        self.assertFalse(files[1].binary)
        self.assertFalse(files[1].deleted)
        self.assertFalse(files[1].is_symlink)
        lines = files[1].data.splitlines()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], b'diff --git a/foo/bar b/foo/bar')
        self.assertEqual(lines[5], b'+Hello!')
        self.assertEqual(files[1].insert_count, 1)
        self.assertEqual(files[1].delete_count, 0)

    def test_binary_diff(self):
        """Testing parsing Git diff with binary"""
        diff = self._read_fixture(b'git_binary.diff')
        file = self._get_file_in_diff(diff)
        self.assertEqual(file.origFile, b'pysvn-1.5.1.tar.gz')
        self.assertEqual(file.newFile, b'pysvn-1.5.1.tar.gz')
        self.assertEqual(file.origInfo, PRE_CREATION)
        self.assertEqual(file.newInfo, b'86b520c')
        self.assertTrue(file.binary)
        self.assertFalse(file.deleted)
        self.assertFalse(file.is_symlink)
        lines = file.data.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], b'diff --git a/pysvn-1.5.1.tar.gz b/pysvn-1.5.1.tar.gz')
        self.assertEqual(lines[3], b'Binary files /dev/null and b/pysvn-1.5.1.tar.gz differ')
        self.assertEqual(file.insert_count, 0)
        self.assertEqual(file.delete_count, 0)

    def test_complex_diff(self):
        """Testing parsing Git diff with existing and new files"""
        diff = self._read_fixture(b'git_complex.diff')
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 7)
        self.assertEqual(files[0].origFile, b'cfg/testcase.ini')
        self.assertEqual(files[0].newFile, b'cfg/testcase.ini')
        self.assertEqual(files[0].origInfo, b'5e35098')
        self.assertEqual(files[0].newInfo, b'e254ef4')
        self.assertFalse(files[0].binary)
        self.assertFalse(files[0].deleted)
        self.assertFalse(files[0].is_symlink)
        self.assertEqual(files[0].insert_count, 2)
        self.assertEqual(files[0].delete_count, 1)
        self.assertEqual(len(files[0].data), 549)
        self.assertEqual(files[0].data.splitlines()[0], b'diff --git a/cfg/testcase.ini b/cfg/testcase.ini')
        self.assertEqual(files[0].data.splitlines()[13], b'         if isinstance(value, basestring):')
        self.assertEqual(files[1].origFile, b'tests/models.py')
        self.assertEqual(files[1].newFile, b'tests/models.py')
        self.assertEqual(files[1].origInfo, PRE_CREATION)
        self.assertEqual(files[1].newInfo, b'e69de29')
        self.assertFalse(files[1].binary)
        self.assertFalse(files[1].deleted)
        self.assertFalse(files[1].is_symlink)
        self.assertEqual(files[1].insert_count, 0)
        self.assertEqual(files[1].delete_count, 0)
        lines = files[1].data.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], b'diff --git a/tests/models.py b/tests/models.py')
        self.assertEqual(files[2].origFile, b'tests/tests.py')
        self.assertEqual(files[2].newFile, b'tests/tests.py')
        self.assertEqual(files[2].origInfo, PRE_CREATION)
        self.assertEqual(files[2].newInfo, b'e279a06')
        self.assertFalse(files[2].binary)
        self.assertFalse(files[2].deleted)
        self.assertFalse(files[2].is_symlink)
        self.assertEqual(files[2].insert_count, 2)
        self.assertEqual(files[2].delete_count, 0)
        lines = files[2].data.splitlines()
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], b'diff --git a/tests/tests.py b/tests/tests.py')
        self.assertEqual(lines[7], b'+This is some new content')
        self.assertEqual(files[3].origFile, b'pysvn-1.5.1.tar.gz')
        self.assertEqual(files[3].newFile, b'pysvn-1.5.1.tar.gz')
        self.assertEqual(files[3].origInfo, PRE_CREATION)
        self.assertEqual(files[3].newInfo, b'86b520c')
        self.assertTrue(files[3].binary)
        self.assertFalse(files[3].deleted)
        self.assertFalse(files[3].is_symlink)
        self.assertEqual(files[3].insert_count, 0)
        self.assertEqual(files[3].delete_count, 0)
        lines = files[3].data.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], b'diff --git a/pysvn-1.5.1.tar.gz b/pysvn-1.5.1.tar.gz')
        self.assertEqual(lines[3], b'Binary files /dev/null and b/pysvn-1.5.1.tar.gz differ')
        self.assertEqual(files[4].origFile, b'readme')
        self.assertEqual(files[4].newFile, b'readme')
        self.assertEqual(files[4].origInfo, b'5e35098')
        self.assertEqual(files[4].newInfo, b'e254ef4')
        self.assertFalse(files[4].binary)
        self.assertFalse(files[4].deleted)
        self.assertFalse(files[4].is_symlink)
        self.assertEqual(files[4].insert_count, 1)
        self.assertEqual(files[4].delete_count, 1)
        lines = files[4].data.splitlines()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], b'diff --git a/readme b/readme')
        self.assertEqual(lines[6], b'+Hello there')
        self.assertEqual(files[5].origFile, b'OLDFILE')
        self.assertEqual(files[5].newFile, b'OLDFILE')
        self.assertEqual(files[5].origInfo, b'8ebcb01')
        self.assertEqual(files[5].newInfo, b'0000000')
        self.assertFalse(files[5].binary)
        self.assertTrue(files[5].deleted)
        self.assertFalse(files[5].is_symlink)
        self.assertEqual(files[5].insert_count, 0)
        self.assertEqual(files[5].delete_count, 1)
        lines = files[5].data.splitlines()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], b'diff --git a/OLDFILE b/OLDFILE')
        self.assertEqual(lines[6], b'-Goodbye')
        self.assertEqual(files[6].origFile, b'readme2')
        self.assertEqual(files[6].newFile, b'readme2')
        self.assertEqual(files[6].origInfo, b'5e43098')
        self.assertEqual(files[6].newInfo, b'e248ef4')
        self.assertFalse(files[6].binary)
        self.assertFalse(files[6].deleted)
        self.assertFalse(files[6].is_symlink)
        self.assertEqual(files[6].insert_count, 1)
        self.assertEqual(files[6].delete_count, 1)
        lines = files[6].data.splitlines()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], b'diff --git a/readme2 b/readme2')
        self.assertEqual(lines[6], b'+Hello there')

    def test_parse_diff_with_index_range(self):
        """Testing Git diff parsing with an index range"""
        diff = b'diff --git a/foo/bar b/foo/bar2\nsimilarity index 88%\nrename from foo/bar\nrename to foo/bar2\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1 100644\n--- a/foo/bar\n+++ b/foo/bar2\n@ -1,1 +1,1 @@\n-blah blah\n+blah\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].origFile, b'foo/bar')
        self.assertEqual(files[0].newFile, b'foo/bar2')
        self.assertEqual(files[0].origInfo, b'612544e4343bf04967eb5ea80257f6c64d6f42c7')
        self.assertEqual(files[0].newInfo, b'e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1')
        self.assertEqual(files[0].insert_count, 1)
        self.assertEqual(files[0].delete_count, 1)

    def test_parse_diff_with_deleted_binary_files(self):
        """Testing Git diff parsing with deleted binary files"""
        diff = b'diff --git a/foo.bin b/foo.bin\ndeleted file mode 100644\nBinary file foo.bin has changed\ndiff --git a/bar.bin b/bar.bin\ndeleted file mode 100644\nBinary file bar.bin has changed\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].origFile, b'foo.bin')
        self.assertEqual(files[0].newFile, b'foo.bin')
        self.assertEqual(files[0].binary, True)
        self.assertEqual(files[0].deleted, True)
        self.assertFalse(files[0].is_symlink)
        self.assertEqual(files[0].insert_count, 0)
        self.assertEqual(files[0].delete_count, 0)
        self.assertEqual(files[1].origFile, b'bar.bin')
        self.assertEqual(files[1].newFile, b'bar.bin')
        self.assertEqual(files[1].binary, True)
        self.assertEqual(files[1].deleted, True)
        self.assertFalse(files[1].is_symlink)
        self.assertEqual(files[1].insert_count, 0)
        self.assertEqual(files[1].delete_count, 0)

    def test_parse_diff_with_all_headers(self):
        """Testing Git diff parsing and preserving all headers"""
        preamble = b'From 38d8fa94a9aa0c5b27943bec31d94e880165f1e0 Mon Sep 17 00:00:00 2001\nFrom: Example Joe <joe@example.com>\nDate: Thu, 5 Apr 2012 00:41:12 -0700\nSubject: [PATCH 1/1] Sample patch.\n\nThis is a test summary.\n\nWith a description.\n---\n foo/bar |   2 -+n README  |   2 -+n 2 files changed, 2 insertions(+), 2 deletions(-)\n\n'
        diff1 = b'diff --git a/foo/bar b/foo/bar2\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1 100644\n--- a/foo/bar\n+++ b/foo/bar2\n@ -1,1 +1,1 @@\n-blah blah\n+blah\n'
        diff2 = b'diff --git a/README b/README\nindex 712544e4343bf04967eb5ea80257f6c64d6f42c7..f88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1 100644\n--- a/README\n+++ b/README\n@ -1,1 +1,1 @@\n-blah blah\n+blah\n-\n1.7.1\n'
        diff = preamble + diff1 + diff2
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].origFile, b'foo/bar')
        self.assertEqual(files[0].newFile, b'foo/bar2')
        self.assertEqual(files[0].origInfo, b'612544e4343bf04967eb5ea80257f6c64d6f42c7')
        self.assertEqual(files[0].newInfo, b'e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1')
        self.assertEqual(files[0].data, preamble + diff1)
        self.assertEqual(files[0].insert_count, 1)
        self.assertEqual(files[0].delete_count, 1)
        self.assertEqual(files[1].origFile, b'README')
        self.assertEqual(files[1].newFile, b'README')
        self.assertEqual(files[1].origInfo, b'712544e4343bf04967eb5ea80257f6c64d6f42c7')
        self.assertEqual(files[1].newInfo, b'f88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1')
        self.assertEqual(files[1].data, diff2)
        self.assertEqual(files[1].insert_count, 1)
        self.assertEqual(files[1].delete_count, 2)

    def test_parse_diff_revision(self):
        """Testing Git revision number parsing"""
        self.assertEqual(self.tool.parse_diff_revision(b'doc/readme', b'bf544ea'), ('doc/readme',
                                                                                    'bf544ea'))
        self.assertEqual(self.tool.parse_diff_revision(b'/dev/null', b'bf544ea'), (
         b'/dev/null', PRE_CREATION))
        self.assertEqual(self.tool.parse_diff_revision(b'/dev/null', b'0000000'), (
         b'/dev/null', PRE_CREATION))

    def test_parse_diff_with_copy_and_rename_same_file(self):
        """Testing Git diff parsing with copy and rename of same file"""
        diff = b'diff --git a/foo/bar b/foo/bar2\nsimilarity index 100%\ncopy from foo/bar\ncopy to foo/bar2\ndiff --git a/foo/bar b/foo/bar3\nsimilarity index 92%\nrename from foo/bar\nrename to foo/bar3\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1 100644\n--- a/foo/bar\n+++ b/foo/bar3\n@@ -1,1 +1,1 @@\n-blah blah\n+blah\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 2)
        f = files[0]
        self.assertEqual(f.origFile, b'foo/bar')
        self.assertEqual(f.newFile, b'foo/bar2')
        self.assertEqual(f.origInfo, b'')
        self.assertEqual(f.newInfo, b'')
        self.assertEqual(f.insert_count, 0)
        self.assertEqual(f.delete_count, 0)
        self.assertFalse(f.moved)
        self.assertTrue(f.copied)
        self.assertFalse(f.is_symlink)
        f = files[1]
        self.assertEqual(f.origFile, b'foo/bar')
        self.assertEqual(f.newFile, b'foo/bar3')
        self.assertEqual(f.origInfo, b'612544e4343bf04967eb5ea80257f6c64d6f42c7')
        self.assertEqual(f.newInfo, b'e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1')
        self.assertEqual(f.insert_count, 1)
        self.assertEqual(f.delete_count, 1)
        self.assertTrue(f.moved)
        self.assertFalse(f.copied)
        self.assertFalse(f.is_symlink)

    def test_parse_diff_with_mode_change_and_rename(self):
        """Testing Git diff parsing with mode change and rename"""
        diff = b'diff --git a/foo/bar b/foo/bar2\nold mode 100755\nnew mode 100644\nsimilarity index 99%\nrename from foo/bar\nrename to foo/bar2\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1\n--- a/foo/bar\n+++ b/foo/bar2\n@@ -1,1 +1,1 @@\n-blah blah\n+blah\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origFile, b'foo/bar')
        self.assertEqual(f.newFile, b'foo/bar2')
        self.assertEqual(f.origInfo, b'612544e4343bf04967eb5ea80257f6c64d6f42c7')
        self.assertEqual(f.newInfo, b'e88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1')
        self.assertEqual(f.insert_count, 1)
        self.assertEqual(f.delete_count, 1)
        self.assertTrue(f.moved)
        self.assertFalse(f.copied)
        self.assertFalse(f.is_symlink)

    def test_diff_git_line_without_a_b(self):
        """Testing parsing Git diff with deleted file without a/ and
        b/ filename prefixes
        """
        diff = b'diff --git foo foo\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origFile, b'foo')
        self.assertEqual(f.newFile, b'foo')
        self.assertTrue(f.deleted)
        self.assertFalse(f.is_symlink)

    def test_diff_git_line_without_a_b_quotes(self):
        """Testing parsing Git diff with deleted file without a/ and
        b/ filename prefixes and with quotes
        """
        diff = b'diff --git "foo" "foo"\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origFile, b'foo')
        self.assertEqual(f.newFile, b'foo')
        self.assertTrue(f.deleted)
        self.assertFalse(f.is_symlink)

    def test_diff_git_line_without_a_b_and_spaces(self):
        """Testing parsing Git diff with deleted file without a/ and
        b/ filename prefixes and with spaces
        """
        diff = b'diff --git foo bar1 foo bar1\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origFile, b'foo bar1')
        self.assertEqual(f.newFile, b'foo bar1')
        self.assertTrue(f.deleted)
        self.assertFalse(f.is_symlink)

    def test_diff_git_line_without_a_b_and_spaces_quotes(self):
        """Testing parsing Git diff with deleted file without a/ and
        b/ filename prefixes and with space and quotes
        """
        diff = b'diff --git "foo bar1" "foo bar1"\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origFile, b'foo bar1')
        self.assertEqual(f.newFile, b'foo bar1')

    def test_diff_git_line_without_a_b_and_spaces_changed(self):
        """Testing parsing Git diff with deleted file without a/ and
        b/ filename prefixes and with spaces, with filename changes
        """
        diff = b'diff --git foo bar1 foo bar2\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\n'
        with self.assertRaises(DiffParserError) as (cm):
            self.tool.get_parser(diff).parse()
        self.assertTrue(six.text_type(cm.exception).startswith(b'Unable to parse the "diff --git" line'))

    def test_diff_git_line_without_a_b_and_spaces_quotes_changed(self):
        """Testing parsing Git diff with deleted file without a/ and
        b/ filename prefixes and with spaces and quotes, with filename
        changes
        """
        diff = b'diff --git "foo bar1" "foo bar2"\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\ndiff --git "foo bar1" foo\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\ndiff --git foo "foo bar1"\ndeleted file mode 100644\nindex 612544e4343bf04967eb5ea80257f6c64d6f42c7..0000000000000000000000000000000000000000\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 3)
        f = files[0]
        self.assertEqual(f.origFile, b'foo bar1')
        self.assertEqual(f.newFile, b'foo bar2')
        self.assertTrue(f.deleted)
        self.assertFalse(f.is_symlink)
        f = files[1]
        self.assertEqual(f.origFile, b'foo bar1')
        self.assertEqual(f.newFile, b'foo')
        f = files[2]
        self.assertEqual(f.origFile, b'foo')
        self.assertEqual(f.newFile, b'foo bar1')

    def test_diff_git_symlink_added(self):
        """Testing parsing Git diff with symlink added"""
        diff = b'diff --git a/link b/link\nnew file mode 120000\nindex 0000000..100b938\n--- /dev/null\n+++ b/link\n@@ -0,0 +1 @@\n+README\n\\ No newline at end of file\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origInfo, PRE_CREATION)
        self.assertEqual(f.newFile, b'link')
        self.assertTrue(f.is_symlink)

    def test_diff_git_symlink_changed(self):
        """Testing parsing Git diff with symlink changed"""
        diff = b'diff --git a/link b/link\nindex 100b937..100b938 120000\n--- a/link\n+++ b/link\n@@ -1 +1 @@\n-README\n\\ No newline at end of file\n+README.md\n\\ No newline at end of file\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.newFile, b'link')
        self.assertEqual(f.origFile, b'link')
        self.assertTrue(f.is_symlink)

    def test_diff_git_symlink_removed(self):
        """Testing parsing Git diff with symlink removed"""
        diff = b'diff --git a/link b/link\ndeleted file mode 120000\nindex 100b938..0000000\n--- a/link\n+++ /dev/null\n@@ -1 +0,0 @@\n-README.txt\n\\ No newline at end of file\n'
        files = self.tool.get_parser(diff).parse()
        self.assertEqual(len(files), 1)
        f = files[0]
        self.assertEqual(f.origFile, b'link')
        self.assertTrue(f.deleted)
        self.assertTrue(f.is_symlink)

    def test_file_exists(self):
        """Testing GitTool.file_exists"""
        self.assertTrue(self.tool.file_exists(b'readme', b'e965047'))
        self.assertTrue(self.tool.file_exists(b'readme', b'd6613f5'))
        self.assertTrue(not self.tool.file_exists(b'readme', PRE_CREATION))
        self.assertTrue(not self.tool.file_exists(b'readme', b'fffffff'))
        self.assertTrue(not self.tool.file_exists(b'readme2', b'fffffff'))
        self.assertTrue(not self.tool.file_exists(b'readme', b'a62df6c'))
        self.assertTrue(not self.tool.file_exists(b'readme2', b'ccffbb4'))

    def test_get_file(self):
        """Testing GitTool.get_file"""
        self.assertEqual(self.tool.get_file(b'readme', PRE_CREATION), b'')
        self.assertTrue(isinstance(self.tool.get_file(b'readme', b'e965047'), bytes))
        self.assertEqual(self.tool.get_file(b'readme', b'e965047'), b'Hello\n')
        self.assertEqual(self.tool.get_file(b'readme', b'd6613f5'), b'Hello there\n')
        self.assertEqual(self.tool.get_file(b'readme'), b'Hello there\n')
        self.assertRaises(SCMError, lambda : self.tool.get_file(b''))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b'', b'0000000'))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b'hello', b'0000000'))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b'readme', b'0000000'))

    def test_parse_diff_revision_with_remote_and_short_SHA1_error(self):
        """Testing GitTool.parse_diff_revision with remote files and short
        SHA1 error
        """
        self.assertRaises(ShortSHA1Error, lambda : self.remote_tool.parse_diff_revision(b'README', b'd7e96b3'))

    def test_get_file_with_remote_and_short_SHA1_error(self):
        """Testing GitTool.get_file with remote files and short SHA1 error"""
        self.assertRaises(ShortSHA1Error, lambda : self.remote_tool.get_file(b'README', b'd7e96b3'))

    def test_valid_repository_https_username(self):
        """Testing GitClient.is_valid_repository with an HTTPS URL and external
        credentials
        """
        client = GitClient(b'https://example.com/test.git', username=b'username', password=b'pass/word')
        self.spy_on(client._run_git)
        client.is_valid_repository()
        self.assertEqual(client._run_git.calls[0].args[0], [
         b'ls-remote',
         b'https://username:pass%2Fword@example.com/test.git',
         b'HEAD'])

    def test_raw_file_url_error(self):
        """Testing Repository.get_file re-fetches when raw file URL changes"""
        self.spy_on(self.remote_repository._get_file_uncached, call_fake=lambda a, b, x, y, z: b'first')
        self.assertEqual(self.remote_repository.get_file(b'PATH', b'd7e96b3'), b'first')
        self.remote_repository._get_file_uncached.unspy()
        self.spy_on(self.remote_repository._get_file_uncached, call_fake=lambda a, b, x, y, z: b'second')
        self.assertEqual(self.remote_repository.get_file(b'PATH', b'd7e96b3'), b'first')
        self.remote_repository.raw_file_url = b'http://github.com/api/v2/yaml/blob/show/reviewboard/<revision>'
        self.assertEqual(self.remote_repository.get_file(b'PATH', b'd7e96b3'), b'second')

    def test_get_file_exists_caching_with_raw_url(self):
        """Testing Repository.get_file_exists properly checks file existence in
        repository or cache when raw file URL changes
        """
        self.spy_on(self.remote_repository._get_file_exists_uncached, call_fake=lambda a, b, x, y, z: True)
        self.assertTrue(self.remote_repository.get_file_exists(b'PATH', b'd7e96b3'))
        self.remote_repository._get_file_exists_uncached.unspy()
        self.assertTrue(self.remote_repository.get_file_exists(b'PATH', b'd7e96b3'))
        self.remote_repository.raw_file_url = b'http://github.com/api/v2/yaml/blob/show/reviewboard/<revision>'
        self.assertFalse(self.remote_repository.get_file_exists(b'PATH', b'd7e96b3'))


class GitAuthFormTests(TestCase):
    """Unit tests for GitTool's authentication form."""

    def test_fields(self):
        """Testing GitTool authentication form fields"""
        form = GitTool.create_auth_form()
        self.assertEqual(list(form.fields), [b'username', b'password'])
        self.assertEqual(form[b'username'].help_text, b'')
        self.assertEqual(form[b'username'].label, b'Username')
        self.assertEqual(form[b'password'].help_text, b'')
        self.assertEqual(form[b'password'].label, b'Password')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting GitTool authentication form load"""
        repository = self.create_repository(tool_name=b'Git', username=b'test-user', password=b'test-pass')
        form = GitTool.create_auth_form(repository=repository)
        form.load()
        self.assertEqual(form[b'username'].value(), b'test-user')
        self.assertEqual(form[b'password'].value(), b'test-pass')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting GitTool authentication form save"""
        repository = self.create_repository(tool_name=b'Git')
        form = GitTool.create_auth_form(repository=repository, data={b'username': b'test-user', 
           b'password': b'test-pass'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.username, b'test-user')
        self.assertEqual(repository.password, b'test-pass')


class GitRepositoryFormTests(TestCase):
    """Unit tests for GitTool's repository form."""

    def test_fields(self):
        """Testing GitTool repository form fields"""
        form = GitTool.create_repository_form()
        self.assertEqual(list(form.fields), [
         b'path', b'mirror_path', b'raw_file_url'])
        self.assertEqual(form[b'path'].help_text, b'For local Git repositories, this should be the path to a .git directory that Review Board can read from. For remote Git repositories, it should be the clone URL.')
        self.assertEqual(form[b'path'].label, b'Path')
        self.assertEqual(form[b'mirror_path'].help_text, b'')
        self.assertEqual(form[b'mirror_path'].label, b'Mirror Path')
        self.assertEqual(form[b'raw_file_url'].label, b'Raw File URL Mask')
        self.assertEqual(form[b'raw_file_url'].help_text, b"A URL mask used to check out a particular revision of a file using HTTP. This is needed for repository types that can't access remote files natively. Use <tt>&lt;revision&gt;</tt> and <tt>&lt;filename&gt;</tt> in the URL in place of the revision and filename parts of the path.")

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting GitTool repository form load"""
        repository = self.create_repository(tool_name=b'Git', path=b'https://github.com/reviewboard/reviewboard', mirror_path=b'git@github.com:reviewboard/reviewboard.git', raw_file_url=b'http://git.example.com/raw/<revision>')
        form = GitTool.create_repository_form(repository=repository)
        form.load()
        self.assertEqual(form[b'path'].value(), b'https://github.com/reviewboard/reviewboard')
        self.assertEqual(form[b'mirror_path'].value(), b'git@github.com:reviewboard/reviewboard.git')
        self.assertEqual(form[b'raw_file_url'].value(), b'http://git.example.com/raw/<revision>')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting GitTool repository form save"""
        repository = self.create_repository(tool_name=b'Git')
        form = GitTool.create_repository_form(repository=repository, data={b'path': b'https://github.com/reviewboard/reviewboard', 
           b'mirror_path': b'git@github.com:reviewboard/reviewboard.git', 
           b'raw_file_url': b'http://git.example.com/raw/<revision>'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.path, b'https://github.com/reviewboard/reviewboard')
        self.assertEqual(repository.mirror_path, b'git@github.com:reviewboard/reviewboard.git')
        self.assertEqual(repository.raw_file_url, b'http://git.example.com/raw/<revision>')