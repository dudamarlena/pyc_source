# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/scmtools/tests/test_tfs.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import json
from django.utils.six.moves.urllib.error import HTTPError
from django.utils.six.moves.urllib.parse import quote, urlencode
from django.utils.six.moves.urllib.request import OpenerDirector, build_opener
from kgb import SpyAgency
from reviewboard.scmtools.errors import AuthenticationError, FileNotFoundError, RepositoryNotFoundError, SCMError
from reviewboard.scmtools.models import Tool, Repository
from reviewboard.scmtools.tests import SCMTestCase
from rbpowerpack.testing.testcases import PowerPackExtensionTestCase

class TFSTests(SpyAgency, PowerPackExtensionTestCase, SCMTestCase):
    """Unit tests for TFS."""

    def setUp(self):
        super(TFSTests, self).setUp()
        self.path = b'http://tfs:8080/tfs/DefaultCollection/'
        self.tool = Tool.objects.get(name=b'Team Foundation Server')
        self.repository = Repository(name=b'TFS', path=self.path, tool=self.tool)

    def test_url_quoting(self):
        """Testing TFSTool path quoting"""
        repository = Repository(name=b'TFS', path=b'http://tfs:8080/test%20/', tool=self.tool)
        self.assertEqual(repository.get_scmtool().client.path, b'http://tfs:8080/test%20/')
        repository = Repository(name=b'TFS', path=b'http://tfs:8080/test /', tool=self.tool)
        self.assertEqual(repository.get_scmtool().client.path, b'http://tfs:8080/test%20/')
        repository = Repository(name=b'TFS', path=b'http://tfs:8080/test%/', tool=self.tool)
        self.assertEqual(repository.get_scmtool().client.path, b'http://tfs:8080/test%25/')

    def test_check_repository(self):
        """Testing TFSTool.check_repository"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, self.path + b'_apis/projects?api-version=1.0')

                class Response(object):
                    code = 200
                    headers = {}

                    def read(self):
                        return b'{  "count": 0,  "value": []}'

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        tool.check_repository(self.path, b'username', b'password')

    def test_check_repository_disabled(self):
        """Testing TFSTool.check_repository with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'Team Foundation Server repositories cannot be used while Power Pack is disabled.', lambda : tool.check_repository(self.path, b'username', b'password'))

    def test_check_repository_403(self):
        """Testing TFSTool.check_repository with 403 response"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, self.path + b'_apis/projects?api-version=1.0')

                class Response(object):
                    code = 403
                    msg = b'Forbidden'
                    headers = {}

                    def read(self):
                        return b''

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        self.assertRaises(AuthenticationError, tool.check_repository, self.path, b'username', b'password')

    def test_check_repository_404(self):
        """Testing TFSTool.check_repository with 404 response"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, self.path + b'_apis/projects?api-version=1.0')
                raise HTTPError(url, 404, b'Not Found', {}, None)
                return

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        self.assertRaises(RepositoryNotFoundError, tool.check_repository, self.path, b'username', b'password')

    def test_check_repository_500(self):
        """Testing TFSTool.check_repository with 500 response"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, self.path + b'_apis/projects?api-version=1.0')

                class Response(object):
                    code = 500
                    msg = b'Internal Server Error'
                    headers = {}

                    def read(self):
                        return b''

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        self.assertRaises(SCMError, tool.check_repository, self.path, b'username', b'password')

    def test_check_repository_non_json_result(self):
        """Testing TFSTool.check_repository with a non-JSON response"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, self.path + b'_apis/projects?api-version=1.0')

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        return b'<p>Not json!</p>'

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        self.assertRaises(SCMError, tool.check_repository, self.path, b'username', b'password')

    def test_file_exists_disabled(self):
        """Testing TFSTool.file_exists with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS" cannot be used while Power Pack is disabled.', lambda : tool.file_exists(b'$/my_file.txt', 5, base_commit_id=None))

    def test_get_file(self):
        """Testing TFSTool.get_file"""
        data = b'File data'
        filename = b'$/my_file.txt'
        version = 5

        class Opener(OpenerDirector):

            def open(s, url):
                query = {b'path': filename, 
                   b'versionType': b'Changeset', 
                   b'version': version}
                self.assertEqual(url, b'%s_apis/tfvc/items?%s' % (
                 self.path, urlencode(query)))

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {b'Content-Type': b'application/octet-stream'}

                    def read(self):
                        return data

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        self.assertEqual(tool.get_file(filename, version, base_commit_id=None), data)
        return

    def test_get_file_disabled(self):
        """Testing TFSTool.get_file with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS" cannot be used while Power Pack is disabled.', lambda : tool.get_file(b'$/my_file.txt', 5, base_commit_id=None))

    def test_get_file_404(self):
        """Testing TFSTool.get_file with 404 response"""
        filename = b'$/my_file.txt'
        version = 5

        class Opener(OpenerDirector):

            def open(s, url):
                query = {b'path': filename, 
                   b'versionType': b'Changeset', 
                   b'version': version}
                self.assertEqual(url, b'%s_apis/tfvc/items?%s' % (
                 self.path, urlencode(query)))
                raise HTTPError(url, 404, b'Not Found', {}, None)
                return

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        self.assertRaises(FileNotFoundError, tool.get_file, filename, version)

    def test_path_without_trailing_slash(self):
        """Testing TFSTool URLs without a trailing slash"""
        path = b'http://tfs:8080/tfs/DefaultCollection'
        repository = Repository(name=b'TFS', path=path, tool=Tool.objects.get(name=b'Team Foundation Server'))
        data = b'File data'
        filename = b'$/my_file.txt'
        version = 5

        class Opener(OpenerDirector):

            def open(s, url):
                query = {b'path': filename, 
                   b'versionType': b'Changeset', 
                   b'version': version}
                self.assertEqual(url, b'%s/_apis/tfvc/items?%s' % (
                 path, urlencode(query)))

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {b'Content-Type': b'application/octet-stream'}

                    def read(self):
                        return data

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = repository.get_scmtool()
        self.assertEqual(tool.get_file(filename, version, base_commit_id=None), data)
        return

    def test_parse_diff_revision(self):
        """Testing TFSTool.parse_diff_revision"""
        tool = self.repository.get_scmtool()
        self.assertEqual(tool.parse_diff_revision(b'filename', 5), ('filename', 5))

    def test_get_branches(self):
        """Testing TFSTool.get_branches"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, b'%s_apis/tfvc/branches?api-version=1.0&includeChildren=true' % self.path)

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        return json.dumps({b'count': 1, 
                           b'value': [{b'path': b'$/branch1/'}]})

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        branches = tool.get_branches()
        self.assertEqual(len(branches), 2)

    def test_get_branches_with_children(self):
        """Testing TFSTool.get_branches with children"""

        class Opener(OpenerDirector):

            def open(s, url):
                self.assertEqual(url, b'%s_apis/tfvc/branches?api-version=1.0&includeChildren=true' % self.path)

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        return json.dumps({b'count': 1, 
                           b'value': [
                                    {b'path': b'$/b1', 
                                       b'children': [
                                                   {b'path': b'$/b1/b2', 
                                                      b'children': [
                                                                  {b'path': b'$/b1/b2/b3'}]}]}]})

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        branches = tool.get_branches()
        self.assertEqual(len(branches), 4)
        branch = branches[0]
        self.assertEqual(branch.id, b'$/')
        self.assertEqual(branch.name, b'$/')
        branch = branches[1]
        self.assertEqual(branch.id, b'$/b1')
        self.assertEqual(branch.name, b'$/b1')
        branch = branches[2]
        self.assertEqual(branch.id, b'$/b1/b2')
        self.assertEqual(branch.name, b'$/b1/b2')
        branch = branches[3]
        self.assertEqual(branch.id, b'$/b1/b2/b3')
        self.assertEqual(branch.name, b'$/b1/b2/b3')

    def test_get_branches_disabled(self):
        """Testing TFSTool.get_branches with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS" cannot be used while Power Pack is disabled.', lambda : tool.get_branches())

    def test_get_change_disabled(self):
        """Testing TFSTool.get_change with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS" cannot be used while Power Pack is disabled.', lambda : tool.get_change(1))

    def test_get_change(self):
        """Testing TFSTool.get_change"""

        def _api_request(client, resource, query=None, decode_json=True, include_api_version=True):
            return ({},
             {b'author': {b'displayName': b'Doc'}, 
                b'changesetId': b'2', 
                b'changes': [
                           {b'changeType': b'add'}], 
                b'createdDate': b'2018-02-05'})

        tool = self.repository.get_scmtool()
        self.spy_on(tool.client._api_request, call_fake=_api_request)
        change = tool.get_change(2)
        self.assertEqual(change.id, b'2')
        self.assertEqual(change.parent, b'1')
        self.assertEqual(change.author_name, b'Doc')
        return

    def test_get_change_string(self):
        """Testing TFSTool.get_change with a string revision"""

        def _api_request(client, resource, query=None, decode_json=True, include_api_version=True):
            return ({},
             {b'author': {b'displayName': b'Doc'}, 
                b'changesetId': b'2', 
                b'changes': [
                           {b'changeType': b'add'}], 
                b'createdDate': b'2018-02-05'})

        tool = self.repository.get_scmtool()
        self.spy_on(tool.client._api_request, call_fake=_api_request)
        change = tool.get_change(b'2')
        self.assertEqual(change.id, b'2')
        self.assertEqual(change.parent, b'1')
        self.assertEqual(change.author_name, b'Doc')
        return

    def _test_get_commits(self, branch=None, start=None):

        class Opener(OpenerDirector):

            def open(s, url):
                if branch is None:
                    encoded_branch_name = quote(b'$/', safe=b'')
                else:
                    encoded_branch_name = quote(branch, safe=b'')
                if start:
                    encoded_start = b'&searchCriteria.toId=%d' % start
                else:
                    encoded_start = b''
                self.assertEqual(url, b'%s_apis/tfvc/changesets?searchCriteria.itemPath=%s&%%24top=30%s&api-version=1.0' % (
                 self.path, encoded_branch_name,
                 encoded_start))

                class Response(object):
                    code = 200
                    msg = b''
                    headers = {}

                    def read(self):
                        return json.dumps({b'count': 2, 
                           b'value': [
                                    {b'changesetId': b'2', 
                                       b'author': {b'displayName': b'Author 2'}, b'createdDate': b'2014-11-12T21:53:49.22Z', 
                                       b'comment': b'Commit 2'},
                                    {b'changesetId': b'1', 
                                       b'author': {b'displayName': b'Author 1'}, b'createdDate': b'2014-09-18T06:46:39.663Z', 
                                       b'comment': b'Commit 1'}]})

                return Response()

        self.spy_on(build_opener, call_fake=lambda *args: Opener())
        tool = self.repository.get_scmtool()
        commits = tool.get_commits(branch, start)
        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0].author_name, b'Author 2')
        self.assertEqual(commits[0].message, b'Commit 2')
        self.assertEqual(commits[1].id, b'1')

    def test_get_commits(self):
        """Testing TFSTool.get_commits"""
        self._test_get_commits()

    def test_get_commits_disabled(self):
        """Testing TFSTool.get_commits with Power Pack disabled"""
        self.ext_manager.disable_extension(self.extension_class.id)
        tool = self.repository.get_scmtool()
        self.assertRaisesMessage(SCMError, b'The repository "TFS" cannot be used while Power Pack is disabled.', lambda : tool.get_commits(b'$/branch/'))

    def test_get_commits_with_branch_name(self):
        """Testing TFSTool.get_commits with a branch name"""
        self._test_get_commits(b'$/branch/')

    def test_get_commits_with_start(self):
        """Testing TFSTool.get_commits with a branch name and start
        parameter"""
        self._test_get_commits(b'$/branch/', 2)

    def test_diff_parser(self):
        """Testing TFSTool diff parsing"""
        diff = b"--- $/Test project/PythonApplication1.py\t13\n+++ $/Test project/PythonApplication1.py\t(pending)\n@@ -1,5 +1,5 @@\n-#!/usr/bin/env python\n-\n-from __future__ import print_function, unicode_literals\n-\n-print('Hello World')\n+#!/usr/bin/env python\n+\n+from __future__ import print_function, unicode_literals\n+\n+print('Héllo World\\n')\n--- $/Tést project/PythonApplication2.py\t13\n+++ $/Tést project/PythonApplication3.py\t(pending)\n@@ -1,5 +1,5 @@\n-#!/usr/bin/env python\n-\n-from __future__ import print_function, unicode_literals\n-\n-print('Hello World')\n+#!/usr/bin/env python\n+\n+from __future__ import print_function, unicode_literals\n+\n+print('Hello World\\n')\n--- $/Test project/logo.png\t13\n+++ $/Test project/logo.png\t(pending)\nBinary files $/Test project/logo.png and $/Test project/logo.png differ\nCopied from: $/Test project/PythonApplication3.py\n--- $/Test project/PythonApplication3.py\t13\n+++ $/Test project/PythonApplication4.py\t(pending)\n@@ -1,5 +1,5 @@\n-#!/usr/bin/env python\n-\n-from __future__ import print_function, unicode_literals\n-\n-print('Hello World')\n+#!/usr/bin/env python\n+\n+from __future__ import print_function, unicode_literals\n+\n+print('Hello World\\n')\n--- $/Test project/PythonApplication4.py\t13\n+++ $/Test project/PythonApplication5.py\t(pending)\n"
        tool = self.repository.get_scmtool()
        files = tool.get_parser(diff).parse()
        self.assertEqual(len(files), 5)
        f = files[0]
        self.assertIsInstance(f.origFile, bytes)
        self.assertIsInstance(f.newFile, bytes)
        self.assertIsInstance(f.origInfo, bytes)
        self.assertIsInstance(f.newInfo, bytes)
        self.assertEqual(f.origFile, b'$/Test project/PythonApplication1.py')
        self.assertEqual(f.newFile, b'$/Test project/PythonApplication1.py')
        self.assertEqual(f.origInfo, b'13')
        self.assertEqual(f.newInfo, b'(pending)')
        self.assertFalse(f.binary)
        self.assertFalse(f.deleted)
        self.assertFalse(f.moved)
        self.assertFalse(f.copied)
        f = files[1]
        self.assertIsInstance(f.origFile, bytes)
        self.assertIsInstance(f.newFile, bytes)
        self.assertIsInstance(f.origInfo, bytes)
        self.assertIsInstance(f.newInfo, bytes)
        self.assertEqual(f.origFile, (b'$/Tést project/PythonApplication2.py').encode(b'utf-8'))
        self.assertEqual(f.newFile, (b'$/Tést project/PythonApplication3.py').encode(b'utf-8'))
        self.assertEqual(f.origInfo, b'13')
        self.assertEqual(f.newInfo, b'(pending)')
        self.assertFalse(f.binary)
        self.assertFalse(f.deleted)
        self.assertTrue(f.moved)
        self.assertFalse(f.copied)
        f = files[2]
        self.assertIsInstance(f.origFile, bytes)
        self.assertIsInstance(f.newFile, bytes)
        self.assertIsInstance(f.origInfo, bytes)
        self.assertIsInstance(f.newInfo, bytes)
        self.assertEqual(f.origFile, b'$/Test project/logo.png')
        self.assertTrue(f.binary)
        self.assertFalse(f.deleted)
        self.assertFalse(f.moved)
        self.assertFalse(f.copied)
        f = files[3]
        self.assertIsInstance(f.origFile, bytes)
        self.assertIsInstance(f.newFile, bytes)
        self.assertIsInstance(f.origInfo, bytes)
        self.assertIsInstance(f.newInfo, bytes)
        self.assertEqual(f.origFile, b'$/Test project/PythonApplication3.py')
        self.assertEqual(f.newFile, b'$/Test project/PythonApplication4.py')
        self.assertEqual(f.origInfo, b'13')
        self.assertEqual(f.newInfo, b'(pending)')
        self.assertFalse(f.binary)
        self.assertFalse(f.deleted)
        self.assertFalse(f.moved)
        self.assertTrue(f.copied)
        f = files[4]
        self.assertIsInstance(f.origFile, bytes)
        self.assertIsInstance(f.newFile, bytes)
        self.assertIsInstance(f.origInfo, bytes)
        self.assertIsInstance(f.newInfo, bytes)
        self.assertEqual(f.origFile, b'$/Test project/PythonApplication4.py')
        self.assertEqual(f.newFile, b'$/Test project/PythonApplication5.py')
        self.assertEqual(f.origInfo, b'13')
        self.assertEqual(f.newInfo, b'(pending)')
        self.assertFalse(f.binary)
        self.assertFalse(f.deleted)
        self.assertTrue(f.moved)
        self.assertFalse(f.copied)
        self.assertEqual(f.data, b'')