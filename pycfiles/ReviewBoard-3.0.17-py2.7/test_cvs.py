# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_cvs.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, nose
from django.core.exceptions import ValidationError
from djblets.testing.decorators import add_fixtures
from reviewboard.diffviewer.parser import DiffParserError
from reviewboard.scmtools.core import PRE_CREATION, Revision
from reviewboard.scmtools.cvs import CVSTool
from reviewboard.scmtools.errors import SCMError, FileNotFoundError
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.scmtools.tests.testcases import SCMTestCase
from reviewboard.testing.testcase import TestCase

class CVSTests(SCMTestCase):
    """Unit tests for CVS."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(CVSTests, self).setUp()
        self.cvs_repo_path = os.path.join(os.path.dirname(__file__), b'..', b'testdata', b'cvs_repo')
        self.cvs_ssh_path = b':ext:localhost:%s' % self.cvs_repo_path.replace(b'\\', b'/')
        self.repository = Repository(name=b'CVS', path=self.cvs_repo_path, tool=Tool.objects.get(name=b'CVS'))
        try:
            self.tool = self.repository.get_scmtool()
        except ImportError:
            raise nose.SkipTest(b'cvs binary not found')

    def test_build_cvsroot_with_port(self):
        """Testing CVSTool.build_cvsroot with a port"""
        self._test_build_cvsroot(repo_path=b'example.com:123/cvsroot/test', username=b'anonymous', expected_cvsroot=b':pserver:anonymous@example.com:123/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_without_port(self):
        """Testing CVSTool.build_cvsroot without a port"""
        self._test_build_cvsroot(repo_path=b'example.com:/cvsroot/test', username=b'anonymous', expected_cvsroot=b':pserver:anonymous@example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_pserver_and_no_user_or_password(self):
        """Testing CVSTool.build_cvsroot with :pserver: and no user or
        password
        """
        self._test_build_cvsroot(repo_path=b':pserver:example.com:/cvsroot/test', expected_cvsroot=b':pserver:example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_pserver_and_inline_user(self):
        """Testing CVSTool.build_cvsroot with :pserver: and inline user"""
        self._test_build_cvsroot(repo_path=b':pserver:anonymous@example.com:/cvsroot/test', expected_cvsroot=b':pserver:anonymous@example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_pserver_and_inline_user_and_password(self):
        """Testing CVSTool.build_cvsroot with :pserver: and inline user and
        password
        """
        self._test_build_cvsroot(repo_path=b':pserver:anonymous:pass@example.com:/cvsroot/test', expected_cvsroot=b':pserver:anonymous:pass@example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_pserver_and_form_user(self):
        """Testing CVSTool.build_cvsroot with :pserver: and form-provided
        user
        """
        self._test_build_cvsroot(repo_path=b':pserver:example.com:/cvsroot/test', username=b'anonymous', expected_cvsroot=b':pserver:anonymous@example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_pserver_and_form_user_and_password(self):
        """Testing CVSTool.build_cvsroot with :pserver: and form-provided
        user and password
        """
        self._test_build_cvsroot(repo_path=b':pserver:example.com:/cvsroot/test', username=b'anonymous', password=b'pass', expected_cvsroot=b':pserver:anonymous:pass@example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_pserver_and_inline_takes_precedence(self):
        """Testing CVSTool.build_cvsroot with :pserver: and inline user/password
        taking precedence
        """
        self._test_build_cvsroot(repo_path=b':pserver:anonymous:pass@example.com:/cvsroot/test', username=b'grumpy', password=b'grr', expected_cvsroot=b':pserver:anonymous:pass@example.com:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_gserver(self):
        """Testing CVSTool.build_cvsroot with :gserver:"""
        self._test_build_cvsroot(repo_path=b':gserver:localhost:/cvsroot/test', expected_cvsroot=b':gserver:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_gserver_with_username(self):
        """Testing CVSTool.build_cvsroot with :gserver: with username"""
        self._test_build_cvsroot(repo_path=b':gserver:user@localhost:/cvsroot/test', expected_cvsroot=b':gserver:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')
        self._test_build_cvsroot(repo_path=b':gserver:localhost:/cvsroot/test', username=b'user', expected_cvsroot=b':gserver:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_gserver_with_port(self):
        """Testing CVSTool.build_cvsroot with :gserver: with port"""
        self._test_build_cvsroot(repo_path=b':gserver:localhost:123/cvsroot/test', expected_cvsroot=b':gserver:localhost:123/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_gserver_validates_password(self):
        """Testing CVSTool.build_cvsroot with :gserver: validates password"""
        self._test_build_cvsroot(repo_path=b':gserver:user:pass@localhost:/cvsroot/test', expected_error=b'"gserver" CVSROOTs do not support passwords.', expected_cvsroot=b':gserver:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_kserver(self):
        """Testing CVSTool.build_cvsroot with :kserver:"""
        self._test_build_cvsroot(repo_path=b':kserver:localhost:/cvsroot/test', expected_cvsroot=b':kserver:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_kserver_with_username(self):
        """Testing CVSTool.build_cvsroot with :kserver: with username"""
        self._test_build_cvsroot(repo_path=b':kserver:user@localhost:/cvsroot/test', expected_cvsroot=b':kserver:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')
        self._test_build_cvsroot(repo_path=b':kserver:localhost:/cvsroot/test', username=b'user', expected_cvsroot=b':kserver:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_kserver_with_port(self):
        """Testing CVSTool.build_cvsroot with :kserver: with port"""
        self._test_build_cvsroot(repo_path=b':kserver:localhost:123/cvsroot/test', expected_cvsroot=b':kserver:localhost:123/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_kserver_validates_password(self):
        """Testing CVSTool.build_cvsroot with :kserver: validates password"""
        self._test_build_cvsroot(repo_path=b':kserver:user:pass@localhost:/cvsroot/test', expected_error=b'"kserver" CVSROOTs do not support passwords.', expected_cvsroot=b':kserver:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_ext(self):
        """Testing CVSTool.build_cvsroot with :ext:"""
        self._test_build_cvsroot(repo_path=b':ext:localhost:/cvsroot/test', expected_cvsroot=b':ext:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_ext_validates_password(self):
        """Testing CVSTool.build_cvsroot with :ext: validates password"""
        self._test_build_cvsroot(repo_path=b':ext:user:pass@localhost:/cvsroot/test', expected_error=b'"ext" CVSROOTs do not support passwords.', expected_cvsroot=b':ext:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_ext_validates_port(self):
        """Testing CVSTool.build_cvsroot with :ext: validates port"""
        self._test_build_cvsroot(repo_path=b':ext:localhost:123/cvsroot/test', expected_error=b'"ext" CVSROOTs do not support specifying ports.', expected_cvsroot=b':ext:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_server(self):
        """Testing CVSTool.build_cvsroot with :server:"""
        self._test_build_cvsroot(repo_path=b':server:localhost:/cvsroot/test', expected_cvsroot=b':server:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_server_validates_password(self):
        """Testing CVSTool.build_cvsroot with :server: validates password"""
        self._test_build_cvsroot(repo_path=b':server:user:pass@localhost:/cvsroot/test', expected_error=b'"server" CVSROOTs do not support passwords.', expected_cvsroot=b':server:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_server_validates_port(self):
        """Testing CVSTool.build_cvsroot with :server: validates port"""
        self._test_build_cvsroot(repo_path=b':server:localhost:123/cvsroot/test', expected_error=b'"server" CVSROOTs do not support specifying ports.', expected_cvsroot=b':server:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_ssh(self):
        """Testing CVSTool.build_cvsroot with :ssh:"""
        self._test_build_cvsroot(repo_path=b':ssh:localhost:/cvsroot/test', expected_cvsroot=b':ssh:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_ssh_validates_password(self):
        """Testing CVSTool.build_cvsroot with :ssh: validates password"""
        self._test_build_cvsroot(repo_path=b':ssh:user:pass@localhost:/cvsroot/test', expected_error=b'"ssh" CVSROOTs do not support passwords.', expected_cvsroot=b':ssh:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_ssh_validates_port(self):
        """Testing CVSTool.build_cvsroot with :ssh: validates port"""
        self._test_build_cvsroot(repo_path=b':ssh:localhost:123/cvsroot/test', expected_error=b'"ssh" CVSROOTs do not support specifying ports.', expected_cvsroot=b':ssh:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_extssh(self):
        """Testing CVSTool.build_cvsroot with :extssh:"""
        self._test_build_cvsroot(repo_path=b':extssh:localhost:/cvsroot/test', expected_cvsroot=b':extssh:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_extssh_validates_password(self):
        """Testing CVSTool.build_cvsroot with :extssh: validates password"""
        self._test_build_cvsroot(repo_path=b':extssh:user:pass@localhost:/cvsroot/test', expected_error=b'"extssh" CVSROOTs do not support passwords.', expected_cvsroot=b':extssh:user@localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_extssh_validates_port(self):
        """Testing CVSTool.build_cvsroot with :extssh: validates port"""
        self._test_build_cvsroot(repo_path=b':extssh:localhost:123/cvsroot/test', expected_error=b'"extssh" CVSROOTs do not support specifying ports.', expected_cvsroot=b':extssh:localhost:/cvsroot/test', expected_path=b'/cvsroot/test')

    def test_path_with_fork(self):
        """Testing CVSTool.build_cvsroot with :fork:"""
        self._test_build_cvsroot(repo_path=b':fork:/home/myuser/cvsroot', expected_cvsroot=b':fork:/home/myuser/cvsroot', expected_path=b'/home/myuser/cvsroot')

    def test_path_with_fork_validates_username(self):
        """Testing CVSTool.build_cvsroot with :fork: validates usernames"""
        self._test_build_cvsroot(repo_path=b':fork:/home/myuser/cvsroot', username=b'myuser', expected_error=b'"fork" CVSROOTs do not support usernames.', expected_cvsroot=b':fork:/home/myuser/cvsroot', expected_path=b'/home/myuser/cvsroot')

    def test_path_with_fork_validates_password(self):
        """Testing CVSTool.build_cvsroot with :fork: validates passwords"""
        self._test_build_cvsroot(repo_path=b':fork:/home/myuser/cvsroot', password=b'myuser', expected_error=b'"fork" CVSROOTs do not support passwords.', expected_cvsroot=b':fork:/home/myuser/cvsroot', expected_path=b'/home/myuser/cvsroot')

    def test_path_with_local(self):
        """Testing CVSTool.build_cvsroot with :local:"""
        self._test_build_cvsroot(repo_path=b':local:/home/myuser/cvsroot', expected_cvsroot=b':local:/home/myuser/cvsroot', expected_path=b'/home/myuser/cvsroot')

    def test_path_with_local_validates_username(self):
        """Testing CVSTool.build_cvsroot with :local: validates usernames"""
        self._test_build_cvsroot(repo_path=b':local:/home/myuser/cvsroot', username=b'myuser', expected_error=b'"local" CVSROOTs do not support usernames.', expected_cvsroot=b':local:/home/myuser/cvsroot', expected_path=b'/home/myuser/cvsroot')

    def test_path_with_local_validates_password(self):
        """Testing CVSTool.build_cvsroot with :local: validates passwords"""
        self._test_build_cvsroot(repo_path=b':local:/home/myuser/cvsroot', password=b'myuser', expected_error=b'"local" CVSROOTs do not support passwords.', expected_cvsroot=b':local:/home/myuser/cvsroot', expected_path=b'/home/myuser/cvsroot')

    def test_get_file(self):
        """Testing CVSTool.get_file"""
        expected = b'test content\n'
        file = b'test/testfile'
        rev = Revision(b'1.1')
        badrev = Revision(b'2.1')
        value = self.tool.get_file(file, rev)
        self.assertTrue(isinstance(value, bytes))
        self.assertEqual(value, expected)
        self.assertEqual(self.tool.get_file(file + b',v', rev), expected)
        self.assertEqual(self.tool.get_file(self.tool.repopath + b'/' + file + b',v', rev), expected)
        self.assertTrue(self.tool.file_exists(b'test/testfile'))
        self.assertTrue(self.tool.file_exists(self.tool.repopath + b'/test/testfile'))
        self.assertTrue(self.tool.file_exists(b'test/testfile,v'))
        self.assertTrue(not self.tool.file_exists(b'test/testfile2'))
        self.assertTrue(not self.tool.file_exists(self.tool.repopath + b'/test/testfile2'))
        self.assertTrue(not self.tool.file_exists(b'test/testfile2,v'))
        self.assertTrue(not self.tool.file_exists(b'test/testfile', badrev))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b''))
        self.assertRaises(FileNotFoundError, lambda : self.tool.get_file(b'hello', PRE_CREATION))

    def test_get_file_with_keywords(self):
        """Testing CVSTool.get_file with file containing keywords"""
        value = self.tool.get_file(b'test/testfile', Revision(b'1.2'))
        self.assertEqual(value, b'$Id$\n$Author$\n\ntest content\n')

    def test_revision_parsing(self):
        """Testing CVSTool revision number parsing"""
        self.assertEqual(self.tool.parse_diff_revision(b'', b'PRE-CREATION')[1], PRE_CREATION)
        self.assertEqual(self.tool.parse_diff_revision(b'', b'7 Nov 2005 13:17:07 -0000\t1.2')[1], b'1.2')
        self.assertEqual(self.tool.parse_diff_revision(b'', b'7 Nov 2005 13:17:07 -0000\t1.2.3.4')[1], b'1.2.3.4')
        self.assertRaises(SCMError, lambda : self.tool.parse_diff_revision(b'', b'hello'))

    def test_interface(self):
        """Testing basic CVSTool API"""
        self.assertTrue(self.tool.diffs_use_absolute_paths)

    def test_simple_diff(self):
        """Testing parsing CVS simple diff"""
        diff = b'Index: testfile\n===================================================================\nRCS file: %s/test/testfile,v\nretrieving revision 1.1.1.1\ndiff -u -r1.1.1.1 testfile\n--- testfile    26 Jul 2007 08:50:30 -0000      1.1.1.1\n+++ testfile    26 Jul 2007 10:20:20 -0000\n@@ -1 +1,2 @@\n-test content\n+updated test content\n+added info\n'
        diff = diff % self.cvs_repo_path
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'test/testfile')
        self.assertEqual(file.origInfo, b'26 Jul 2007 08:50:30 -0000      1.1.1.1')
        self.assertEqual(file.newFile, b'test/testfile')
        self.assertEqual(file.newInfo, b'26 Jul 2007 10:20:20 -0000')
        self.assertEqual(file.data, diff)
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_new_diff_revision_format(self):
        """Testing parsing CVS diff with new revision format"""
        diff = b'Index: %s/test/testfile\ndiff -u %s/test/testfile:1.5.2.1 %s/test/testfile:1.5.2.2\n--- test/testfile:1.5.2.1\tThu Dec 15 16:27:47 2011\n+++ test/testfile\tTue Jan 10 10:36:26 2012\n@@ -1 +1,2 @@\n-test content\n+updated test content\n+added info\n'
        diff = diff % (self.cvs_repo_path, self.cvs_repo_path,
         self.cvs_repo_path)
        file = self.tool.get_parser(diff).parse()[0]
        f2, revision = self.tool.parse_diff_revision(file.origFile, file.origInfo, file.moved)
        self.assertEqual(f2, b'test/testfile')
        self.assertEqual(revision, b'1.5.2.1')
        self.assertEqual(file.newFile, b'test/testfile')
        self.assertEqual(file.newInfo, b'Tue Jan 10 10:36:26 2012')
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_bad_diff(self):
        """Testing parsing CVS diff with bad info"""
        diff = b'Index: newfile\n===================================================================\ndiff -N newfile\n--- /dev/null\t1 Jan 1970 00:00:00 -0000\n+++ newfile\t26 Jul 2007 10:11:45 -0000\n@@ -0,0 +1 @@\n+new file content'
        self.assertRaises(DiffParserError, lambda : self.tool.get_parser(diff).parse())

    def test_bad_diff2(self):
        """Testing parsing CVS bad diff with new file"""
        diff = b'Index: newfile\n===================================================================\nRCS file: newfile\ndiff -N newfile\n--- /dev/null\n+++ newfile\t26 Jul 2007 10:11:45 -0000\n@@ -0,0 +1 @@\n+new file content'
        self.assertRaises(DiffParserError, lambda : self.tool.get_parser(diff).parse())

    def test_newfile_diff(self):
        """Testing parsing CVS diff with new file"""
        diff = b'Index: newfile\n===================================================================\nRCS file: newfile\ndiff -N newfile\n--- /dev/null\t1 Jan 1970 00:00:00 -0000\n+++ newfile\t26 Jul 2007 10:11:45 -0000\n@@ -0,0 +1 @@\n+new file content\n'
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'newfile')
        self.assertEqual(file.origInfo, b'PRE-CREATION')
        self.assertEqual(file.newFile, b'newfile')
        self.assertEqual(file.newInfo, b'26 Jul 2007 10:11:45 -0000')
        self.assertEqual(file.data, diff)
        self.assertEqual(file.insert_count, 1)
        self.assertEqual(file.delete_count, 0)

    def test_inter_revision_diff(self):
        """Testing parsing CVS inter-revision diff"""
        diff = b'Index: testfile\n===================================================================\nRCS file: %s/test/testfile,v\nretrieving revision 1.1\nretrieving revision 1.2\ndiff -u -p -r1.1 -r1.2\n--- testfile    26 Jul 2007 08:50:30 -0000      1.1\n+++ testfile    27 Sep 2007 22:57:16 -0000      1.2\n@@ -1 +1,2 @@\n-test content\n+updated test content\n+added info\n'
        diff = diff % self.cvs_repo_path
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'test/testfile')
        self.assertEqual(file.origInfo, b'26 Jul 2007 08:50:30 -0000      1.1')
        self.assertEqual(file.newFile, b'test/testfile')
        self.assertEqual(file.newInfo, b'27 Sep 2007 22:57:16 -0000      1.2')
        self.assertEqual(file.data, diff)
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_unicode_diff(self):
        """Testing parsing CVS diff with unicode filenames"""
        diff = b'Index: téstfile\n===================================================================\nRCS file: %s/test/téstfile,v\nretrieving revision 1.1.1.1\ndiff -u -r1.1.1.1 téstfile\n--- téstfile    26 Jul 2007 08:50:30 -0000      1.1.1.1\n+++ téstfile    26 Jul 2007 10:20:20 -0000\n@@ -1 +1,2 @@\n-tést content\n+updated test content\n+added info\n'
        diff = diff % self.cvs_repo_path
        diff = diff.encode(b'utf-8')
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'test/téstfile')
        self.assertEqual(file.origInfo, b'26 Jul 2007 08:50:30 -0000      1.1.1.1')
        self.assertEqual(file.newFile, b'test/téstfile')
        self.assertEqual(file.newInfo, b'26 Jul 2007 10:20:20 -0000')
        self.assertEqual(file.data, diff)
        self.assertEqual(file.insert_count, 2)
        self.assertEqual(file.delete_count, 1)

    def test_keyword_diff(self):
        """Testing parsing CVS diff with keywords"""
        diff = self.tool.normalize_patch(b'Index: Makefile\n===================================================================\nRCS file: /cvsroot/src/Makefile,v\nretrieving revision 1.1\nretrieving revision 1.2\ndiff -u -r1.1.1.1 Makefile\n--- Makefile    26 Jul 2007 08:50:30 -0000      1.1\n+++ Makefile    26 Jul 2007 10:20:20 -0000      1.2\n@@ -1,6 +1,7 @@\n # $Author: bob $\n # $Date: 2014/12/18 13:09:42 $\n # $Header: /src/Makefile,v 1.2 2014/12/18 13:09:42 bob Exp $\n # $Id: Makefile,v 1.2 2014/12/18 13:09:42 bob Exp $\n # $Locker: bob $\n # $Name: some_name $\n # $RCSfile: Makefile,v $\n # $Revision: 1.2 $\n # $Source: /src/Makefile,v $\n # $State: Exp $\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = cvs-misc-docs\n', b'Makefile')
        self.assertEqual(diff, b'Index: Makefile\n===================================================================\nRCS file: /cvsroot/src/Makefile,v\nretrieving revision 1.1\nretrieving revision 1.2\ndiff -u -r1.1.1.1 Makefile\n--- Makefile    26 Jul 2007 08:50:30 -0000      1.1\n+++ Makefile    26 Jul 2007 10:20:20 -0000      1.2\n@@ -1,6 +1,7 @@\n # $Author$\n # $Date$\n # $Header$\n # $Id$\n # $Locker$\n # $Name$\n # $RCSfile$\n # $Revision$\n # $Source$\n # $State$\n+# foo\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = cvs-misc-docs\n')

    def test_keyword_diff_unicode(self):
        """Testing parsing CVS diff with keywords and unicode characters"""
        self.tool.normalize_patch(b'Index: Makefile\n===================================================================\nRCS file: /cvsroot/src/Makefile,v\nretrieving revision 1.1\nretrieving revision 1.2\ndiff -u -r1.1.1.1 Makefile\n--- Makefile    26 Jul 2007 08:50:30 -0000      1.1\n+++ Makefile    26 Jul 2007 10:20:20 -0000      1.2\n@@ -1,6 +1,7 @@\n # $Author: bob $\n # $Date: 2014/12/18 13:09:42 $\n # $Header: /src/Makefile,v 1.2 2014/12/18 13:09:42 bob Exp $\n # $Id: Makefile,v 1.2 2014/12/18 13:09:42 bob Exp $\n # $Locker: bob $\n # $Name: some_name $\n # $RCSfile: Makefile,v $\n # $Revision: 1.2 $\n # $Source: /src/Makefile,v $\n # $State: Exp $\n+# foo 💩\n include ../tools/Makefile.base-vars\n NAME = misc-docs\n OUTNAME = cvs-misc-docs\n', b'Makefile')

    def test_binary_diff(self):
        """Testing parsing CVS binary diff"""
        diff = b'Index: testfile\n===================================================================\nRCS file: %s/test/testfile,v\nretrieving revision 1.1.1.1\ndiff -u -r1.1.1.1 testfile\nBinary files testfile and testfile differ\n' % self.cvs_repo_path
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'test/testfile')
        self.assertEqual(file.origInfo, b'')
        self.assertEqual(file.newFile, b'test/testfile')
        self.assertEqual(file.newInfo, b'')
        self.assertTrue(file.binary)
        self.assertEqual(file.data, diff)

    def test_binary_diff_new_file(self):
        """Testing parsing CVS binary diff with new file"""
        diff = b'Index: test/testfile\n===================================================================\nRCS file: test/testfile,v\ndiff -N test/testfile\nBinary files /dev/null and testfile differ\n'
        file = self.tool.get_parser(diff).parse()[0]
        self.assertEqual(file.origFile, b'test/testfile')
        self.assertEqual(file.origInfo, b'PRE-CREATION')
        self.assertEqual(file.newFile, b'test/testfile')
        self.assertEqual(file.newInfo, b'')
        self.assertTrue(file.binary)
        self.assertEqual(file.data, diff)

    def test_bad_root(self):
        """Testing CVSTool with a bad CVSROOT"""
        file = b'test/testfile'
        rev = Revision(b'1.1')
        badrepo = Repository(name=b'CVS', path=self.cvs_repo_path + b'2', tool=Tool.objects.get(name=b'CVS'))
        badtool = badrepo.get_scmtool()
        self.assertRaises(SCMError, lambda : badtool.get_file(file, rev))

    def test_ssh(self):
        """Testing a SSH-backed CVS repository"""
        self._test_ssh(self.cvs_ssh_path, b'CVSROOT/modules')

    def test_ssh_with_site(self):
        """Testing a SSH-backed CVS repository with a LocalSite"""
        self._test_ssh_with_site(self.cvs_ssh_path, b'CVSROOT/modules')

    def _test_build_cvsroot(self, repo_path, expected_cvsroot, expected_path, expected_error=None, username=None, password=None):
        if expected_error:
            with self.assertRaisesMessage(ValidationError, expected_error):
                self.tool.build_cvsroot(repo_path, username, password, validate=True)
        cvsroot, norm_path = self.tool.build_cvsroot(repo_path, username, password, validate=False)
        self.assertEqual(cvsroot, expected_cvsroot)
        self.assertEqual(norm_path, expected_path)


class CVSAuthFormTests(TestCase):
    """Unit tests for CVSTool's authentication form."""

    def test_fields(self):
        """Testing CVSTool authentication form fields"""
        form = CVSTool.create_auth_form()
        self.assertEqual(list(form.fields), [b'username', b'password'])
        self.assertEqual(form[b'username'].help_text, b'')
        self.assertEqual(form[b'username'].label, b'Username')
        self.assertEqual(form[b'password'].help_text, b'')
        self.assertEqual(form[b'password'].label, b'Password')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting CVSTool authentication form load"""
        repository = self.create_repository(tool_name=b'CVS', username=b'test-user', password=b'test-pass')
        form = CVSTool.create_auth_form(repository=repository)
        form.load()
        self.assertEqual(form[b'username'].value(), b'test-user')
        self.assertEqual(form[b'password'].value(), b'test-pass')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting CVSTool authentication form save"""
        repository = self.create_repository(tool_name=b'CVS')
        form = CVSTool.create_auth_form(repository=repository, data={b'username': b'test-user', 
           b'password': b'test-pass'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.username, b'test-user')
        self.assertEqual(repository.password, b'test-pass')


class CVSRepositoryFormTests(TestCase):
    """Unit tests for CVSTool's repository form."""

    def test_fields(self):
        """Testing CVSTool repository form fields"""
        form = CVSTool.create_repository_form()
        self.assertEqual(list(form.fields), [b'path', b'mirror_path'])
        self.assertEqual(form[b'path'].help_text, b'The CVSROOT used to access the repository.')
        self.assertEqual(form[b'path'].label, b'Path')
        self.assertEqual(form[b'mirror_path'].help_text, b'')
        self.assertEqual(form[b'mirror_path'].label, b'Mirror Path')

    @add_fixtures([b'test_scmtools'])
    def test_load(self):
        """Tetting CVSTool repository form load"""
        repository = self.create_repository(tool_name=b'CVS', path=b'example.com:123/cvsroot/test', mirror_path=b':pserver:example.com:/cvsroot/test')
        form = CVSTool.create_repository_form(repository=repository)
        form.load()
        self.assertEqual(form[b'path'].value(), b'example.com:123/cvsroot/test')
        self.assertEqual(form[b'mirror_path'].value(), b':pserver:example.com:/cvsroot/test')

    @add_fixtures([b'test_scmtools'])
    def test_save(self):
        """Tetting CVSTool repository form save"""
        repository = self.create_repository(tool_name=b'CVS')
        form = CVSTool.create_repository_form(repository=repository, data={b'path': b'example.com:123/cvsroot/test', 
           b'mirror_path': b':pserver:example.com:/cvsroot/test'})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(repository.path, b'example.com:123/cvsroot/test')
        self.assertEqual(repository.mirror_path, b':pserver:example.com:/cvsroot/test')