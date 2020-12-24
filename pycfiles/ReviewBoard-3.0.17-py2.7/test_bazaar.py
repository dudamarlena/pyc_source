# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_bazaar.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, nose
from django.utils import six
from djblets.testing.decorators import add_fixtures
from djblets.util.filesystem import is_exe_in_path
from reviewboard.scmtools.bzr import BZRTool
from reviewboard.scmtools.errors import FileNotFoundError, InvalidRevisionFormatError, RepositoryNotFoundError, SCMError
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.scmtools.tests.testcases import SCMTestCase
from reviewboard.testing.testcase import TestCase

class BZRTests(SCMTestCase):
    """Unit tests for bzr."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(BZRTests, self).setUp()
        if not is_exe_in_path(b'bzr'):
            raise nose.SkipTest()
        self.bzr_repo_path = os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'bzr_repo')
        self.bzr_ssh_path = b'bzr+ssh://localhost/%s' % self.bzr_repo_path.replace(b'\\', b'/')
        self.bzr_sftp_path = b'sftp://localhost/%s' % self.bzr_repo_path.replace(b'\\', b'/')
        self.repository = Repository(name=b'Bazaar', path=b'file://' + self.bzr_repo_path, tool=Tool.objects.get(name=b'Bazaar'))
        self.tool = self.repository.get_scmtool()

    def test_check_repository(self):
        """Testing BZRTool.check_repository"""
        self.tool.check_repository(self.repository.path)

    def test_check_repository_with_not_found(self):
        """Testing BZRTool.check_repository with repository not found"""
        with self.assertRaises(RepositoryNotFoundError):
            self.tool.check_repository(b'file:///dummy')

    def test_ssh(self):
        """Testing BZRTool with a SSH-backed repository"""
        self._test_ssh(self.bzr_ssh_path, b'README')

    def test_ssh_with_site(self):
        """Testing BZRTool with a SSH-backed repository with a LocalSite"""
        self._test_ssh_with_site(self.bzr_ssh_path, b'README')

    def test_sftp(self):
        """Testing BZRTool with a SFTP-backed repository"""
        try:
            self._test_ssh(self.bzr_sftp_path, b'README')
        except SCMError as e:
            err = six.text_type(e)
            if b'Installed bzr and paramiko modules are incompatible' in err:
                raise nose.SkipTest(err)
            raise

    def test_get_file(self):
        """Testing BZRTool.get_file"""
        content = self.tool.get_file(b'README', b'2011-02-02 10:53:04 +0000')
        self.assertEqual(content, b'This is a test.\n')
        self.assertIsInstance(content, bytes)

    def test_get_file_with_timezone_offset(self):
        """Testing BZRTool.get_file with timezone offset"""
        content = self.tool.get_file(b'README', b'2011-02-02 02:53:04 -0800')
        self.assertEqual(content, b'This is a test.\n')
        self.assertIsInstance(content, bytes)

    def test_get_file_with_non_utc_server_timezone(self):
        """Testing BZRTool.get_file with settings.TIME_ZONE != UTC"""
        old_timezone = os.environ[b'TZ']
        os.environ[b'TZ'] = b'US/Pacific'
        try:
            content = self.tool.get_file(b'README', b'2011-02-02 02:53:04 -0800')
        finally:
            os.environ[b'TZ'] = old_timezone

        self.assertEqual(content, b'This is a test.\n')
        self.assertIsInstance(content, bytes)

    def test_get_file_with_revision_id(self):
        """Testing BZRTool.get_file with revision ID"""
        content = self.tool.get_file(b'README', b'revid:chipx86@chipx86.com-20110202105304-8lkgyb18aqr11b21')
        self.assertEqual(content, b'This is a test.\n')
        self.assertIsInstance(content, bytes)

    def test_get_file_with_unknown_file(self):
        """Testing BZRTool.get_file with unknown file"""
        with self.assertRaises(FileNotFoundError):
            self.tool.get_file(b'NOT_REAL', b'2011-02-02 02:53:04 -0800')

    def test_get_file_with_unknown_revision(self):
        """Testing BZRTool.get_file with unknown revision"""
        with self.assertRaises(FileNotFoundError):
            self.tool.get_file(b'README', b'9999-02-02 02:53:04 -0800')

    def test_get_file_with_invalid_revision(self):
        """Testing BZRTool.get_file with invalid revision"""
        with self.assertRaises(InvalidRevisionFormatError):
            self.tool.get_file(b'README', b'\\o/')

    def test_file_exists(self):
        """Testing BZRTool.files_exists"""
        self.assertTrue(self.tool.file_exists(b'README', b'2011-02-02 10:53:04 +0000'))
        self.assertFalse(self.tool.file_exists(b'NOT_REAL', b'2011-02-02 10:53:04 +0000'))
        self.assertFalse(self.tool.file_exists(b'README', b'9999-02-02 10:53:04 +0000'))

    def test_file_exists_with_timezone_offset(self):
        """Testing BZRTool.files_exists with timezone offset"""
        self.assertTrue(self.tool.file_exists(b'README', b'2011-02-02 02:53:04 -0800'))

    def test_file_exists_with_non_utc_server_timezone(self):
        """Testing BZRTool.files_exists with settings.TIME_ZONE != UTC"""
        old_timezone = os.environ[b'TZ']
        os.environ[b'TZ'] = b'US/Pacific'
        try:
            self.assertTrue(self.tool.file_exists(b'README', b'2011-02-02 02:53:04 -0800'))
        finally:
            os.environ[b'TZ'] = old_timezone

    def test_file_exists_with_revision_id(self):
        """Testing BZRTool.files_exists with revision ID"""
        self.assertTrue(self.tool.file_exists(b'README', b'revid:chipx86@chipx86.com-20110202105304-8lkgyb18aqr11b21'))

    def test_file_exists_with_invalid_revision(self):
        """Testing BZRTool.files_exists with invalid revision"""
        with self.assertRaises(InvalidRevisionFormatError):
            self.tool.file_exists(b'README', b'\\o/')


class BZRAuthFormTests(TestCase):
    """Unit tests for BZRTool's authentication form."""

    def test_fields(self):
        """Testing BZRTool authentication form fields"""
        form = BZRTool.create_auth_form()
        self.assertEqual(list(form.fields), [b'username', b'password'])
        self.assertEqual(form[b'username'].help_text, b'')
        self.assertEqual(form[b'username'].label, b'Username')
        self.assertEqual(form[b'password'].help_text, b'')
        self.assertEqual(form[b'password'].label, b'Password')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting BZRTool authentication form load"""
        repository = self.create_repository(tool_name=b'Bazaar', username=b'test-user', password=b'test-pass')
        form = BZRTool.create_auth_form(repository=repository)
        form.load()
        self.assertEqual(form[b'username'].value(), b'test-user')
        self.assertEqual(form[b'password'].value(), b'test-pass')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting BZRTool authentication form save"""
        repository = self.create_repository(tool_name=b'Bazaar')
        form = BZRTool.create_auth_form(repository=repository, data={b'username': b'test-user', 
           b'password': b'test-pass'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.username, b'test-user')
        self.assertEqual(repository.password, b'test-pass')


class BZRRepositoryFormTests(TestCase):
    """Unit tests for BZRTool's repository form."""

    def test_fields(self):
        """Testing BZRTool repository form fields"""
        form = BZRTool.create_repository_form()
        self.assertEqual(list(form.fields), [b'path', b'mirror_path'])
        self.assertEqual(form[b'path'].help_text, b'The path to the repository. This will generally be the URL you would use to check out the repository.')
        self.assertEqual(form[b'path'].label, b'Path')
        self.assertEqual(form[b'mirror_path'].help_text, b'')
        self.assertEqual(form[b'mirror_path'].label, b'Mirror Path')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting BZRTool repository form load"""
        repository = self.create_repository(tool_name=b'Bazaar', path=b'bzr+ssh://bzr.example.com/repo', mirror_path=b'sftp://bzr.example.com/repo')
        form = BZRTool.create_repository_form(repository=repository)
        form.load()
        self.assertEqual(form[b'path'].value(), b'bzr+ssh://bzr.example.com/repo')
        self.assertEqual(form[b'mirror_path'].value(), b'sftp://bzr.example.com/repo')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting BZRTool repository form save"""
        repository = self.create_repository(tool_name=b'Bazaar')
        form = BZRTool.create_repository_form(repository=repository, data={b'path': b'bzr+ssh://bzr.example.com/repo', 
           b'mirror_path': b'sftp://bzr.example.com/repo'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.path, b'bzr+ssh://bzr.example.com/repo')
        self.assertEqual(repository.mirror_path, b'sftp://bzr.example.com/repo')