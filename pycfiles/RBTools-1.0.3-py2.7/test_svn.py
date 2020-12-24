# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/tests/test_svn.py
# Compiled at: 2020-04-14 20:27:46
"""Unit tests for SubversionClient."""
from __future__ import unicode_literals
import json, os, sys
from functools import wraps
from hashlib import md5
from kgb import SpyAgency
from nose import SkipTest
from six.moves.urllib.request import urlopen
from rbtools.api.client import RBClient
from rbtools.api.tests import MockResponse
from rbtools.clients.errors import InvalidRevisionSpecError, TooManyRevisionsError
from rbtools.clients.svn import SVNRepositoryInfo, SVNClient
from rbtools.clients.tests import FOO1, FOO2, FOO3, SCMClientTests
from rbtools.utils.checks import is_valid_version
from rbtools.utils.filesystem import is_exe_in_path
from rbtools.utils.process import execute

def svn_version_set_hash(svn16_hash, svn17_hash, svn19_hash):
    """Pass the appropriate hash to the wrapped function.

    SVN 1.6, 1.7/1.8, and 1.9+ will generate slightly different output for
    ``svn diff`` when generating the diff with a working copy. This works
    around that by checking the installed SVN version and passing the
    appropriate hash.
    """

    def decorator(f):

        @wraps(f)
        def wrapped(self):
            self.client.get_repository_info()
            version = self.client.subversion_client_version
            if version < (1, 7):
                return f(self, svn16_hash)
            else:
                if version < (1, 9):
                    return f(self, svn17_hash)
                return f(self, svn19_hash)

        return wrapped

    return decorator


class SVNRepositoryInfoTests(SpyAgency, SCMClientTests):
    """Unit tests for rbtools.clients.svn.SVNRepositoryInfo."""
    payloads = {b'http://localhost:8080/api/': {b'mimetype': b'application/vnd.reviewboard.org.root+json', 
                                       b'rsp': {b'uri_templates': {}, b'links': {b'self': {b'href': b'http://localhost:8080/api/', 
                                                                     b'method': b'GET'}, 
                                                           b'repositories': {b'href': b'http://localhost:8080/api/repositories/', 
                                                                             b'method': b'GET'}}, 
                                                b'stat': b'ok'}}, 
       b'http://localhost:8080/api/repositories/?tool=Subversion': {b'mimetype': b'application/vnd.reviewboard.org.repositories+json', 
                                                                    b'rsp': {b'repositories': [
                                                                                             {b'id': 1, 
                                                                                                b'name': b'SVN Repo 1', 
                                                                                                b'path': b'https://svn1.example.com/', 
                                                                                                b'links': {b'info': {b'href': b'https://localhost:8080/api/repositories/1/info/', 
                                                                                                                     b'method': b'GET'}}},
                                                                                             {b'id': 2, 
                                                                                                b'name': b'SVN Repo 2', 
                                                                                                b'path': b'https://svn2.example.com/', 
                                                                                                b'mirror_path': b'svn+ssh://svn2.example.com/', 
                                                                                                b'links': {b'info': {b'href': b'https://localhost:8080/api/repositories/2/info/', 
                                                                                                                     b'method': b'GET'}}}], 
                                                                             b'links': {b'next': {b'href': b'http://localhost:8080/api/repositories/?tool=Subversion&page=2', 
                                                                                                  b'method': b'GET'}}, 
                                                                             b'total_results': 3, 
                                                                             b'stat': b'ok'}}, 
       b'http://localhost:8080/api/repositories/?tool=Subversion&page=2': {b'mimetype': b'application/vnd.reviewboard.org.repositories+json', 
                                                                           b'rsp': {b'repositories': [
                                                                                                    {b'id': 3, 
                                                                                                       b'name': b'SVN Repo 3', 
                                                                                                       b'path': b'https://svn3.example.com/', 
                                                                                                       b'mirror_path': b'svn+ssh://svn3.example.com/', 
                                                                                                       b'links': {b'info': {b'href': b'https://localhost:8080/api/repositories/3/info/', 
                                                                                                                            b'method': b'GET'}}}], 
                                                                                    b'total_results': 3, 
                                                                                    b'stat': b'ok'}}, 
       b'https://localhost:8080/api/repositories/1/info/': {b'mimetype': b'application/vnd.reviewboard.org.repository-info+json', 
                                                            b'rsp': {b'info': {b'uuid': b'UUID-1', 
                                                                               b'url': b'https://svn1.example.com/', 
                                                                               b'root_url': b'https://svn1.example.com/'}, 
                                                                     b'stat': b'ok'}}, 
       b'https://localhost:8080/api/repositories/2/info/': {b'mimetype': b'application/vnd.reviewboard.org.repository-info+json', 
                                                            b'rsp': {b'info': {b'uuid': b'UUID-2', 
                                                                               b'url': b'https://svn2.example.com/', 
                                                                               b'root_url': b'https://svn2.example.com/'}, 
                                                                     b'stat': b'ok'}}, 
       b'https://localhost:8080/api/repositories/3/info/': {b'mimetype': b'application/vnd.reviewboard.org.repository-info+json', 
                                                            b'rsp': {b'info': {b'uuid': b'UUID-3', 
                                                                               b'url': b'https://svn3.example.com/', 
                                                                               b'root_url': b'https://svn3.example.com/'}, 
                                                                     b'stat': b'ok'}}}

    def setUp(self):
        super(SVNRepositoryInfoTests, self).setUp()

        def _urlopen(url, **kwargs):
            url = url.get_full_url()
            try:
                payload = self.payloads[url]
            except KeyError:
                return MockResponse(404, {}, json.dumps({b'rsp': {b'stat': b'fail', 
                            b'err': {b'code': 100, 
                                     b'msg': b'Object does not exist'}}}))

            return MockResponse(200, {b'Content-Type': payload[b'mimetype']}, json.dumps(payload[b'rsp']))

        self.spy_on(urlopen, call_fake=_urlopen)
        self.api_client = RBClient(b'http://localhost:8080/')
        self.root_resource = self.api_client.get_root()

    def test_find_server_repository_info_with_path_match(self):
        """Testing SVNRepositoryInfo.find_server_repository_info with
        path matching
        """
        info = SVNRepositoryInfo(b'https://svn1.example.com/', b'/', b'')
        repo_info = info.find_server_repository_info(self.root_resource)
        self.assertEqual(repo_info, info)
        self.assertEqual(repo_info.repository_id, 1)

    def test_find_server_repository_info_with_mirror_path_match(self):
        """Testing SVNRepositoryInfo.find_server_repository_info with
        mirror_path matching
        """
        info = SVNRepositoryInfo(b'svn+ssh://svn2.example.com/', b'/', b'')
        repo_info = info.find_server_repository_info(self.root_resource)
        self.assertEqual(repo_info, info)
        self.assertEqual(repo_info.repository_id, 2)

    def test_find_server_repository_info_with_uuid_match(self):
        """Testing SVNRepositoryInfo.find_server_repository_info with
        UUID matching
        """
        info = SVNRepositoryInfo(b'svn+ssh://blargle/', b'/', b'UUID-3')
        repo_info = info.find_server_repository_info(self.root_resource)
        self.assertNotEqual(repo_info, info)
        self.assertEqual(repo_info.repository_id, 3)

    def test_relative_paths(self):
        """Testing SVNRepositoryInfo._get_relative_path"""
        info = SVNRepositoryInfo(b'http://svn.example.com/svn/', b'/', b'')
        self.assertEqual(info._get_relative_path(b'/foo', b'/bar'), None)
        self.assertEqual(info._get_relative_path(b'/', b'/trunk/myproject'), None)
        self.assertEqual(info._get_relative_path(b'/trunk/myproject', b'/'), b'/trunk/myproject')
        self.assertEqual(info._get_relative_path(b'/trunk/myproject', b''), b'/trunk/myproject')
        self.assertEqual(info._get_relative_path(b'/trunk/myproject', b'/trunk'), b'/myproject')
        self.assertEqual(info._get_relative_path(b'/trunk/myproject', b'/trunk/myproject'), b'/')
        return


class SVNClientTests(SCMClientTests):

    def setUp(self):
        super(SVNClientTests, self).setUp()
        if not is_exe_in_path(b'svn'):
            raise SkipTest(b'svn not found in path')
        self.svn_dir = os.path.join(self.testdata_dir, b'svn-repo')
        self.clone_dir = self.chdir_tmp()
        self.svn_repo_url = b'file://' + self.svn_dir
        self._run_svn([b'co', self.svn_repo_url, b'svn-repo'])
        os.chdir(os.path.join(self.clone_dir, b'svn-repo'))
        self.client = SVNClient(options=self.options)
        self.options.svn_show_copies_as_adds = None
        return

    def _run_svn(self, command):
        return execute([b'svn'] + command, env=None, split_lines=False, ignore_errors=False, extra_ignore_errors=())

    def _svn_add_file(self, filename, data, changelist=None):
        """Add a file to the test repo."""
        is_new = not os.path.exists(filename)
        with open(filename, b'wb') as (f):
            f.write(data)
        if is_new:
            self._run_svn([b'add', filename])
        if changelist:
            self._run_svn([b'changelist', changelist, filename])

    def _svn_add_dir(self, dirname):
        """Add a directory to the test repo."""
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        self._run_svn([b'add', dirname])

    def test_parse_revision_spec_no_args(self):
        """Testing SVNClient.parse_revision_spec with no specified revisions"""
        revisions = self.client.parse_revision_spec()
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], b'BASE')
        self.assertEqual(revisions[b'tip'], b'--rbtools-working-copy')

    def test_parse_revision_spec_one_revision(self):
        """Testing SVNClient.parse_revision_spec with one specified numeric
        revision"""
        revisions = self.client.parse_revision_spec([b'3'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], 2)
        self.assertEqual(revisions[b'tip'], 3)

    def test_parse_revision_spec_one_revision_changelist(self):
        """Testing SVNClient.parse_revision_spec with one specified changelist
        revision"""
        self._svn_add_file(b'foo.txt', FOO3, b'my-change')
        revisions = self.client.parse_revision_spec([b'my-change'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], b'BASE')
        self.assertEqual(revisions[b'tip'], SVNClient.REVISION_CHANGELIST_PREFIX + b'my-change')

    def test_parse_revision_spec_one_revision_nonexistant_changelist(self):
        """Testing SVNClient.parse_revision_spec with one specified invalid
        changelist revision"""
        self._svn_add_file(b'foo.txt', FOO3, b'my-change')
        self.assertRaises(InvalidRevisionSpecError, lambda : self.client.parse_revision_spec([b'not-my-change']))

    def test_parse_revision_spec_one_arg_two_revisions(self):
        """Testing SVNClient.parse_revision_spec with R1:R2 syntax"""
        revisions = self.client.parse_revision_spec([b'1:3'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], 1)
        self.assertEqual(revisions[b'tip'], 3)

    def test_parse_revision_spec_two_arguments(self):
        """Testing SVNClient.parse_revision_spec with two revisions"""
        revisions = self.client.parse_revision_spec([b'1', b'3'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], 1)
        self.assertEqual(revisions[b'tip'], 3)

    def test_parse_revision_spec_one_revision_url(self):
        """Testing SVNClient.parse_revision_spec with one revision and a
        repository URL"""
        self.options.repository_url = b'http://svn.apache.org/repos/asf/subversion/trunk'
        revisions = self.client.parse_revision_spec([b'1549823'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], 1549822)
        self.assertEqual(revisions[b'tip'], 1549823)

    def test_parse_revision_spec_two_revisions_url(self):
        """Testing SVNClient.parse_revision_spec with R1:R2 syntax and a
        repository URL"""
        self.options.repository_url = b'http://svn.apache.org/repos/asf/subversion/trunk'
        revisions = self.client.parse_revision_spec([b'1549823:1550211'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], 1549823)
        self.assertEqual(revisions[b'tip'], 1550211)

    def test_parse_revision_spec_invalid_spec(self):
        """Testing SVNClient.parse_revision_spec with invalid specifications"""
        self.assertRaises(InvalidRevisionSpecError, self.client.parse_revision_spec, [
         b'aoeu'])
        self.assertRaises(InvalidRevisionSpecError, self.client.parse_revision_spec, [
         b'aoeu', b'1234'])
        self.assertRaises(TooManyRevisionsError, self.client.parse_revision_spec, [
         b'1', b'2', b'3'])

    def test_parse_revision_spec_non_unicode_log(self):
        """Testing SVNClient.parse_revision_spec with a non-utf8 log entry"""
        revisions = self.client.parse_revision_spec([b'2'])
        self.assertTrue(isinstance(revisions, dict))
        self.assertTrue(b'base' in revisions)
        self.assertTrue(b'tip' in revisions)
        self.assertTrue(b'parent_base' not in revisions)
        self.assertEqual(revisions[b'base'], 1)
        self.assertEqual(revisions[b'tip'], 2)

    def test_get_commit_message_working_copy(self):
        """Testing SVNClient.get_commit_message with a working copy change"""
        revisions = self.client.parse_revision_spec()
        message = self.client.get_commit_message(revisions)
        self.assertIsNone(message)

    def test_get_commit_message_committed_revision(self):
        """Testing SVNClient.get_commit_message with a single committed
        revision
        """
        revisions = self.client.parse_revision_spec([b'2'])
        message = self.client.get_commit_message(revisions)
        self.assertTrue(b'summary' in message)
        self.assertTrue(b'description' in message)
        self.assertEqual(message[b'summary'], b'Commit 2 -- a non-utf8 character: é')
        self.assertEqual(message[b'description'], b'Commit 2 -- a non-utf8 character: é\n')

    def test_get_commit_message_committed_revisions(self):
        """Testing SVNClient.get_commit_message with multiple committed
        revisions
        """
        revisions = self.client.parse_revision_spec([b'1:3'])
        message = self.client.get_commit_message(revisions)
        self.assertTrue(b'summary' in message)
        self.assertTrue(b'description' in message)
        self.assertEqual(message[b'summary'], b'Commit 2 -- a non-utf8 character: é')
        self.assertEqual(message[b'description'], b'Commit 3')

    @svn_version_set_hash(b'6613644d417f7c90f83f3a2d16b1dad5', b'7630ea80056a7340d93a556e9af60c63', b'6a5339da19e60c7706e44aeebfa4da5f')
    def test_diff_exclude(self, md5sum):
        """Testing SVNClient diff with file exclude patterns"""
        self._svn_add_file(b'bar.txt', FOO1)
        self._svn_add_file(b'exclude.txt', FOO2)
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[
         b'exclude.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5sum)

    def test_diff_exclude_in_subdir(self):
        """Testing SVNClient diff with exclude patterns in a subdir"""
        self._svn_add_file(b'foo.txt', FOO1)
        self._svn_add_dir(b'subdir')
        self._svn_add_file(os.path.join(b'subdir', b'exclude.txt'), FOO2)
        os.chdir(b'subdir')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[
         b'exclude.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(result[b'diff'], b'')

    def test_diff_exclude_root_pattern_in_subdir(self):
        """Testing SVNClient diff with repo exclude patterns in a subdir"""
        self._svn_add_file(b'exclude.txt', FOO1)
        self._svn_add_dir(b'subdir')
        os.chdir(b'subdir')
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, exclude_patterns=[
         os.path.join(os.path.sep, b'exclude.txt'),
         b'.'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(result[b'diff'], b'')

    @svn_version_set_hash(b'043befc507b8177a0f010dc2cecc4205', b'1b68063237c584d38a9a3ddbdf1f72a2', b'466f7c2092e085354f5b24b91d48dd80')
    def test_same_diff_multiple_methods(self, md5_sum):
        """Testing SVNClient identical diff generated from root, subdirectory,
        and via target"""
        self._svn_add_dir(b'dir1')
        self._svn_add_file(b'dir1/A.txt', FOO3)
        revisions = self.client.parse_revision_spec()
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5_sum)
        os.chdir(b'dir1')
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5_sum)
        os.chdir(b'..')
        self._svn_add_dir(b'dir2')
        os.chdir(b'dir2')
        result = self.client.diff(revisions, [b'../dir1/A.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5_sum)

    @svn_version_set_hash(b'902d662a110400f7470294b2d9e72d36', b'13803373ded9af750384a4601d5173ce', b'f11dfbe58925871c5f64b6ca647a8d3c')
    def test_diff_non_unicode_characters(self, md5_sum):
        """Testing SVNClient diff with a non-utf8 file"""
        self._svn_add_file(b'A.txt', (b'â').encode(b'iso-8859-1'))
        self._run_svn([b'propset', b'svn:mime-type', b'text/plain', b'A.txt'])
        revisions = self.client.parse_revision_spec()
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5_sum)

    @svn_version_set_hash(b'60c4d21f4d414da947f4e7273e6d1326', b'60c4d21f4d414da947f4e7273e6d1326', b'571e47c456698bad35bca06523473008')
    def test_diff_non_unicode_filename_repository_url(self, md5sum):
        """Testing SVNClient diff with a non-utf8 filename via repository_url
        option"""
        self.options.repository_url = self.svn_repo_url
        revisions = self.client.parse_revision_spec([b'4'])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5sum)

    @svn_version_set_hash(b'ac1835240ec86ee14ddccf1f2236c442', b'ac1835240ec86ee14ddccf1f2236c442', b'610f5506e670dc55a2464a6ad9af015c')
    def test_show_copies_as_adds_enabled(self, md5sum):
        """Testing SVNClient with --show-copies-as-adds functionality
        enabled"""
        self.check_show_copies_as_adds(b'y', md5sum)

    @svn_version_set_hash(b'd41d8cd98f00b204e9800998ecf8427e', b'd41d8cd98f00b204e9800998ecf8427e', b'b656e2f9b70ade256c3fe855c13ee52c')
    def test_show_copies_as_adds_disabled(self, md5sum):
        """Testing SVNClient with --show-copies-as-adds functionality
        disabled"""
        self.check_show_copies_as_adds(b'n', md5sum)

    def check_show_copies_as_adds(self, state, md5sum):
        """Helper function to evaluate --show-copies-as-adds"""
        self.client.get_repository_info()
        if not is_valid_version(self.client.subversion_client_version, self.client.SHOW_COPIES_AS_ADDS_MIN_VERSION):
            raise SkipTest(b'Subversion client is too old to test --show-copies-as-adds.')
        self.options.svn_show_copies_as_adds = state
        self._svn_add_dir(b'dir1')
        self._svn_add_dir(b'dir2')
        self._run_svn([b'copy', b'foo.txt', b'dir1'])
        revisions = self.client.parse_revision_spec()
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5sum)
        self._run_svn([b'changelist', b'cl1', b'dir1/foo.txt'])
        revisions = self.client.parse_revision_spec([b'cl1'])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5sum)
        revisions = self.client.parse_revision_spec()
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5sum)
        self._run_svn([b'changelist', b'--remove', b'dir1/foo.txt'])
        os.chdir(b'dir2')
        revisions = self.client.parse_revision_spec()
        result = self.client.diff(revisions, [b'../dir1'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), md5sum)

    def test_history_scheduled_with_commit_nominal(self):
        """Testing SVNClient.history_scheduled_with_commit nominal cases"""
        self.client.get_repository_info()
        if not is_valid_version(self.client.subversion_client_version, self.client.SHOW_COPIES_AS_ADDS_MIN_VERSION):
            raise SkipTest(b'Subversion client is too old to test history_scheduled_with_commit().')
        self._svn_add_dir(b'dir1')
        self._svn_add_dir(b'dir2')
        self._run_svn([b'copy', b'foo.txt', b'dir1'])
        sys.stderr = open(os.devnull, b'w')
        revisions = self.client.parse_revision_spec()
        self.assertRaises(SystemExit, self.client.diff, revisions)
        self._run_svn([b'changelist', b'cl1', b'dir1/foo.txt'])
        revisions = self.client.parse_revision_spec([b'cl1'])
        self.assertRaises(SystemExit, self.client.diff, revisions)
        revisions = self.client.parse_revision_spec()
        self.assertRaises(SystemExit, self.client.diff, revisions)
        self._run_svn([b'changelist', b'--remove', b'dir1/foo.txt'])
        os.chdir(b'dir2')
        revisions = self.client.parse_revision_spec()
        self.assertRaises(SystemExit, self.client.diff, revisions, [b'../dir1'])

    def test_history_scheduled_with_commit_special_case_non_local_mods(self):
        """Testing SVNClient.history_scheduled_with_commit is bypassed when
        diff is not for local modifications in a working copy"""
        self.client.get_repository_info()
        if not is_valid_version(self.client.subversion_client_version, self.client.SHOW_COPIES_AS_ADDS_MIN_VERSION):
            raise SkipTest(b'Subversion client is too old to test history_scheduled_with_commit().')
        self._run_svn([b'copy', b'foo.txt', b'foo_copy.txt'])
        revisions = self.client.parse_revision_spec([b'1:2'])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'ed154720a7459c2649cab4d2fa34fa93')
        self.options.repository_url = self.svn_repo_url
        revisions = self.client.parse_revision_spec([b'2'])
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'ed154720a7459c2649cab4d2fa34fa93')

    def test_history_scheduled_with_commit_special_case_exclude(self):
        """Testing SVNClient.history_scheduled_with_commit with exclude file"""
        self.client.get_repository_info()
        if not is_valid_version(self.client.subversion_client_version, self.client.SHOW_COPIES_AS_ADDS_MIN_VERSION):
            raise SkipTest(b'Subversion client is too old to test history_scheduled_with_commit().')
        self._run_svn([b'copy', b'foo.txt', b'foo_copy.txt'])
        revisions = self.client.parse_revision_spec([])
        result = self.client.diff(revisions, [], [b'foo_copy.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'd41d8cd98f00b204e9800998ecf8427e')
        self._run_svn([b'changelist', b'cl1', b'foo_copy.txt'])
        revisions = self.client.parse_revision_spec([b'cl1'])
        result = self.client.diff(revisions, [], [b'foo_copy.txt'])
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertEqual(md5(result[b'diff']).hexdigest(), b'd41d8cd98f00b204e9800998ecf8427e')

    def test_rename_diff_mangling_bug_4546(self):
        """Test diff with removal of lines that look like headers"""
        with open(b'bug-4546.txt', b'w') as (f):
            f.write(b'-- test line1\n-- test line2\n-- test line (test2)\n')
        revisions = self.client.parse_revision_spec()
        result = self.client.diff(revisions)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(b'diff' in result)
        self.assertTrue(b'--- test line (test1)' in result[b'diff'])