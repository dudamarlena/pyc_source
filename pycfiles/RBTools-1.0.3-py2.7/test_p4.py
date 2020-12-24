# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/tests/test_p4.py
# Compiled at: 2020-04-14 20:27:46
"""Unit tests for PerforceClient."""
from __future__ import unicode_literals
import os, re, time
from hashlib import md5
from rbtools.api.capabilities import Capabilities
from rbtools.clients.errors import InvalidRevisionSpecError, TooManyRevisionsError
from rbtools.clients.perforce import PerforceClient, P4Wrapper
from rbtools.clients.tests import SCMClientTests
from rbtools.utils.filesystem import make_tempfile
from rbtools.utils.testbase import RBTestBase

class P4WrapperTests(RBTestBase):
    """Unit tests for P4Wrapper."""

    def is_supported(self):
        return True

    def test_counters(self):
        """Testing P4Wrapper.counters"""

        class TestWrapper(P4Wrapper):

            def run_p4(self, cmd, *args, **kwargs):
                return [
                 b'a = 1\n',
                 b'b = 2\n',
                 b'c = 3\n']

        p4 = TestWrapper(None)
        info = p4.counters()
        self.assertEqual(len(info), 3)
        self.assertEqual(info[b'a'], b'1')
        self.assertEqual(info[b'b'], b'2')
        self.assertEqual(info[b'c'], b'3')
        return

    def test_info(self):
        """Testing P4Wrapper.info"""

        class TestWrapper(P4Wrapper):

            def run_p4(self, cmd, *args, **kwargs):
                return [
                 b'User name: myuser\n',
                 b'Client name: myclient\n',
                 b'Client host: myclient.example.com\n',
                 b'Client root: /path/to/client\n',
                 b'Server uptime: 111:43:38\n']

        p4 = TestWrapper(None)
        info = p4.info()
        self.assertEqual(len(info), 5)
        self.assertEqual(info[b'User name'], b'myuser')
        self.assertEqual(info[b'Client name'], b'myclient')
        self.assertEqual(info[b'Client host'], b'myclient.example.com')
        self.assertEqual(info[b'Client root'], b'/path/to/client')
        self.assertEqual(info[b'Server uptime'], b'111:43:38')
        return


class PerforceClientTests(SCMClientTests):
    """Unit tests for PerforceClient."""

    class P4DiffTestWrapper(P4Wrapper):

        def __init__(self, options):
            super(PerforceClientTests.P4DiffTestWrapper, self).__init__(options)
            self._timestamp = time.mktime(time.gmtime(0))

        def fstat(self, depot_path, fields=[]):
            assert depot_path in self.fstat_files
            fstat_info = self.fstat_files[depot_path]
            for field in fields:
                assert field in fstat_info

            return fstat_info

        def opened(self, changenum):
            return [ info for info in self.repo_files if info[b'change'] == changenum
                   ]

        def print_file(self, depot_path, out_file):
            for info in self.repo_files:
                if depot_path == b'%s#%s' % (info[b'depotFile'], info[b'rev']):
                    fp = open(out_file, b'w')
                    fp.write(info[b'text'])
                    fp.close()
                    return

            assert False

        def where(self, depot_path):
            assert depot_path in self.where_files
            return [
             {b'path': self.where_files[depot_path]}]

        def change(self, changenum):
            return [
             {b'Change': str(changenum), 
                b'Date': b'2013/01/02 22:33:44', 
                b'User': b'joe@example.com', 
                b'Status': b'pending', 
                b'Description': b'This is a test.\n'}]

        def info(self):
            return {b'Client root': b'/'}

        def run_p4(self, *args, **kwargs):
            assert False

    def test_scan_for_server_counter_with_reviewboard_url(self):
        """Testing PerforceClient.scan_for_server_counter with
        reviewboard.url"""
        RB_URL = b'http://reviewboard.example.com/'

        class TestWrapper(P4Wrapper):

            def counters(self):
                return {b'reviewboard.url': RB_URL, 
                   b'foo': b'bar'}

        client = PerforceClient(TestWrapper)
        url = client.scan_for_server_counter(None)
        self.assertEqual(url, RB_URL)
        return

    def test_repository_info(self):
        """Testing PerforceClient.get_repository_info"""
        SERVER_PATH = b'perforce.example.com:1666'

        class TestWrapper(P4Wrapper):

            def is_supported(self):
                return True

            def info(self):
                return {b'Client root': os.getcwd(), 
                   b'Server address': SERVER_PATH, 
                   b'Server version': b'P4D/FREEBSD60X86_64/2012.2/525804 (2012/09/18)'}

        client = PerforceClient(TestWrapper)
        info = client.get_repository_info()
        self.assertNotEqual(info, None)
        self.assertEqual(info.path, SERVER_PATH)
        self.assertEqual(client.p4d_version, (2012, 2))
        return

    def test_repository_info_outside_client_root(self):
        """Testing PerforceClient.get_repository_info outside client root"""
        SERVER_PATH = b'perforce.example.com:1666'

        class TestWrapper(P4Wrapper):

            def is_supported(self):
                return True

            def info(self):
                return {b'Client root': b'/', 
                   b'Server address': SERVER_PATH, 
                   b'Server version': b'P4D/FREEBSD60X86_64/2012.2/525804 (2012/09/18)'}

        client = PerforceClient(TestWrapper)
        info = client.get_repository_info()
        self.assertEqual(info, None)
        return

    def test_scan_for_server_counter_with_reviewboard_url_encoded(self):
        """Testing PerforceClient.scan_for_server_counter with encoded
        reviewboard.url.http:||"""
        URL_KEY = b'reviewboard.url.http:||reviewboard.example.com/'
        RB_URL = b'http://reviewboard.example.com/'

        class TestWrapper(P4Wrapper):

            def counters(self):
                return {URL_KEY: b'1', 
                   b'foo': b'bar'}

        client = PerforceClient(TestWrapper)
        url = client.scan_for_server_counter(None)
        self.assertEqual(url, RB_URL)
        return

    def test_diff_with_pending_changelist(self):
        """Testing PerforceClient.diff with a pending changelist"""
        client = self._build_client()
        client.p4.repo_files = [
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'2', 
            b'action': b'edit', 
            b'change': b'12345', 
            b'text': b'This is a test.\n'},
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'3', 
            b'action': b'edit', 
            b'change': b'', 
            b'text': b'This is a mess.\n'},
         {b'depotFile': b'//mydepot/test/COPYING', 
            b'rev': b'1', 
            b'action': b'add', 
            b'change': b'12345', 
            b'text': b'Copyright 2013 Joe User.\n'},
         {b'depotFile': b'//mydepot/test/Makefile', 
            b'rev': b'3', 
            b'action': b'delete', 
            b'change': b'12345', 
            b'text': b'all: all\n'}]
        readme_file = make_tempfile()
        copying_file = make_tempfile()
        makefile_file = make_tempfile()
        client.p4.print_file(b'//mydepot/test/README#3', readme_file)
        client.p4.print_file(b'//mydepot/test/COPYING#1', copying_file)
        client.p4.where_files = {b'//mydepot/test/README': readme_file, 
           b'//mydepot/test/COPYING': copying_file, 
           b'//mydepot/test/Makefile': makefile_file}
        revisions = client.parse_revision_spec([b'12345'])
        diff = client.diff(revisions)
        self._compare_diff(diff, b'07aa18ff67f9aa615fcda7ecddcb354e')

    def test_diff_for_submitted_changelist(self):
        """Testing PerforceClient.diff with a submitted changelist"""

        class TestWrapper(self.P4DiffTestWrapper):

            def change(self, changelist):
                return [
                 {b'Change': b'12345', 
                    b'Date': b'2013/12/19 11:32:45', 
                    b'User': b'example', 
                    b'Status': b'submitted', 
                    b'Description': b'My change description\n'}]

            def filelog(self, path):
                return [
                 {b'change0': b'12345', 
                    b'action0': b'edit', 
                    b'rev0': b'3', 
                    b'depotFile': b'//mydepot/test/README'}]

        client = PerforceClient(TestWrapper)
        client.p4.repo_files = [
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'2', 
            b'action': b'edit', 
            b'change': b'12345', 
            b'text': b'This is a test.\n'},
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'3', 
            b'action': b'edit', 
            b'change': b'', 
            b'text': b'This is a mess.\n'}]
        readme_file = make_tempfile()
        client.p4.print_file(b'//mydepot/test/README#3', readme_file)
        client.p4.where_files = {b'//mydepot/test/README': readme_file}
        client.p4.repo_files = [
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'2', 
            b'action': b'edit', 
            b'change': b'12345', 
            b'text': b'This is a test.\n'},
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'3', 
            b'action': b'edit', 
            b'change': b'', 
            b'text': b'This is a mess.\n'}]
        revisions = client.parse_revision_spec([b'12345'])
        diff = client.diff(revisions)
        self._compare_diff(diff, b'8af5576f5192ca87731673030efb5f39', expect_changenum=False)

    def test_diff_with_moved_files_cap_on(self):
        """Testing PerforceClient.diff with moved files and capability on"""
        self._test_diff_with_moved_files(b'5926515eaf4cf6d8257a52f7d9f0e530', caps={b'scmtools': {b'perforce': {b'moved_files': True}}})

    def test_diff_with_moved_files_cap_off(self):
        """Testing PerforceClient.diff with moved files and capability off"""
        self._test_diff_with_moved_files(b'20e5ab395e170dce1b062a796e6c2c13')

    def _test_diff_with_moved_files(self, expected_diff_hash, caps={}):
        client = self._build_client()
        client.capabilities = Capabilities(caps)
        client.p4.repo_files = [
         {b'depotFile': b'//mydepot/test/README', 
            b'rev': b'2', 
            b'action': b'move/delete', 
            b'change': b'12345', 
            b'text': b'This is a test.\n'},
         {b'depotFile': b'//mydepot/test/README-new', 
            b'rev': b'1', 
            b'action': b'move/add', 
            b'change': b'12345', 
            b'text': b'This is a mess.\n'},
         {b'depotFile': b'//mydepot/test/COPYING', 
            b'rev': b'2', 
            b'action': b'move/delete', 
            b'change': b'12345', 
            b'text': b'Copyright 2013 Joe User.\n'},
         {b'depotFile': b'//mydepot/test/COPYING-new', 
            b'rev': b'1', 
            b'action': b'move/add', 
            b'change': b'12345', 
            b'text': b'Copyright 2013 Joe User.\n'}]
        readme_file = make_tempfile()
        copying_file = make_tempfile()
        readme_file_new = make_tempfile()
        copying_file_new = make_tempfile()
        client.p4.print_file(b'//mydepot/test/README#2', readme_file)
        client.p4.print_file(b'//mydepot/test/COPYING#2', copying_file)
        client.p4.print_file(b'//mydepot/test/README-new#1', readme_file_new)
        client.p4.print_file(b'//mydepot/test/COPYING-new#1', copying_file_new)
        client.p4.where_files = {b'//mydepot/test/README': readme_file, 
           b'//mydepot/test/COPYING': copying_file, 
           b'//mydepot/test/README-new': readme_file_new, 
           b'//mydepot/test/COPYING-new': copying_file_new}
        client.p4.fstat_files = {b'//mydepot/test/README': {b'clientFile': readme_file, 
                                      b'movedFile': b'//mydepot/test/README-new'}, 
           b'//mydepot/test/README-new': {b'clientFile': readme_file_new, 
                                          b'depotFile': b'//mydepot/test/README-new'}, 
           b'//mydepot/test/COPYING': {b'clientFile': copying_file, 
                                       b'movedFile': b'//mydepot/test/COPYING-new'}, 
           b'//mydepot/test/COPYING-new': {b'clientFile': copying_file_new, 
                                           b'depotFile': b'//mydepot/test/COPYING-new'}}
        revisions = client.parse_revision_spec([b'12345'])
        diff = client.diff(revisions)
        self._compare_diff(diff, expected_diff_hash)

    def _build_client(self):
        self.options.p4_client = b'myclient'
        self.options.p4_port = b'perforce.example.com:1666'
        self.options.p4_passwd = b''
        client = PerforceClient(self.P4DiffTestWrapper, options=self.options)
        client.p4d_version = (2012, 2)
        return client

    def _compare_diff(self, diff_info, expected_diff_hash, expect_changenum=True):
        self.assertTrue(isinstance(diff_info, dict))
        self.assertTrue(b'diff' in diff_info)
        if expect_changenum:
            self.assertTrue(b'changenum' in diff_info)
        diff_content = re.sub(b'\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}', b'1970-01-01 00:00:00', diff_info[b'diff'])
        self.assertEqual(md5(diff_content).hexdigest(), expected_diff_hash)

    def test_parse_revision_spec_no_args(self):
        """Testing PerforceClient.parse_revision_spec with no specified
        revisions"""
        client = self._build_client()
        revisions = client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertEqual(revisions[b'base'], PerforceClient.REVISION_CURRENT_SYNC)
        self.assertEqual(revisions[b'tip'], PerforceClient.REVISION_PENDING_CLN_PREFIX + b'default')

    def test_parse_revision_spec_pending_cln(self):
        """Testing PerforceClient.parse_revision_spec with a pending
        changelist"""

        class TestWrapper(P4Wrapper):

            def change(self, changelist):
                return [
                 {b'Change': b'12345', 
                    b'Date': b'2013/12/19 11:32:45', 
                    b'User': b'example', 
                    b'Status': b'pending', 
                    b'Description': b'My change description\n'}]

        client = PerforceClient(TestWrapper)
        revisions = client.parse_revision_spec([b'12345'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], PerforceClient.REVISION_CURRENT_SYNC)
        self.assertEqual(revisions[b'tip'], PerforceClient.REVISION_PENDING_CLN_PREFIX + b'12345')

    def test_parse_revision_spec_submitted_cln(self):
        """Testing PerforceClient.parse_revision_spec with a submitted
        changelist"""

        class TestWrapper(P4Wrapper):

            def change(self, changelist):
                return [
                 {b'Change': b'12345', 
                    b'Date': b'2013/12/19 11:32:45', 
                    b'User': b'example', 
                    b'Status': b'submitted', 
                    b'Description': b'My change description\n'}]

        client = PerforceClient(TestWrapper)
        revisions = client.parse_revision_spec([b'12345'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], b'12344')
        self.assertEqual(revisions[b'tip'], b'12345')

    def test_parse_revision_spec_shelved_cln(self):
        """Testing PerforceClient.parse_revision_spec with a shelved
        changelist"""

        class TestWrapper(P4Wrapper):

            def change(self, changelist):
                return [
                 {b'Change': b'12345', 
                    b'Date': b'2013/12/19 11:32:45', 
                    b'User': b'example', 
                    b'Status': b'shelved', 
                    b'Description': b'My change description\n'}]

        client = PerforceClient(TestWrapper)
        revisions = client.parse_revision_spec([b'12345'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], PerforceClient.REVISION_CURRENT_SYNC)
        self.assertEqual(revisions[b'tip'], PerforceClient.REVISION_PENDING_CLN_PREFIX + b'12345')

    def test_parse_revision_spec_two_args(self):
        """Testing PerforceClient.parse_revision_spec with two changelists"""

        class TestWrapper(P4Wrapper):

            def change(self, changelist):
                change = {b'Change': str(changelist), 
                   b'Date': b'2013/12/19 11:32:45', 
                   b'User': b'example', 
                   b'Description': b'My change description\n'}
                if changelist == b'99' or changelist == b'100':
                    change[b'Status'] = b'submitted'
                elif changelist == b'101':
                    change[b'Status'] = b'pending'
                elif changelist == b'102':
                    change[b'Status'] = b'shelved'
                else:
                    assert False
                return [change]

        client = PerforceClient(TestWrapper)
        revisions = client.parse_revision_spec([b'99', b'100'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], b'99')
        self.assertEqual(revisions[b'tip'], b'100')
        self.assertRaises(InvalidRevisionSpecError, client.parse_revision_spec, [
         b'99', b'101'])
        self.assertRaises(InvalidRevisionSpecError, client.parse_revision_spec, [
         b'99', b'102'])
        self.assertRaises(InvalidRevisionSpecError, client.parse_revision_spec, [
         b'101', b'100'])
        self.assertRaises(InvalidRevisionSpecError, client.parse_revision_spec, [
         b'102', b'100'])
        self.assertRaises(InvalidRevisionSpecError, client.parse_revision_spec, [
         b'102', b'10284'])

    def test_parse_revision_spec_invalid_spec(self):
        """Testing PerforceClient.parse_revision_spec with invalid
        specifications"""

        class TestWrapper(P4Wrapper):

            def change(self, changelist):
                return []

        client = PerforceClient(TestWrapper)
        self.assertRaises(InvalidRevisionSpecError, client.parse_revision_spec, [
         b'aoeu'])
        self.assertRaises(TooManyRevisionsError, client.parse_revision_spec, [
         b'1', b'2', b'3'])

    def test_diff_exclude(self):
        """Testing PerforceClient.normalize_exclude_patterns"""
        repo_root = self.chdir_tmp()
        os.mkdir(b'subdir')
        cwd = os.getcwd()

        class ExcludeWrapper(P4Wrapper):

            def info(self):
                return {b'Client root': repo_root}

        client = PerforceClient(ExcludeWrapper)
        patterns = [
         b'//depot/path',
         os.path.join(os.path.sep, b'foo'),
         b'foo']
        normalized_patterns = [
         patterns[0],
         os.path.join(repo_root, patterns[1][1:]),
         os.path.join(cwd, patterns[2])]
        result = client.normalize_exclude_patterns(patterns)
        self.assertEqual(result, normalized_patterns)