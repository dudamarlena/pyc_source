# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/network/scout/test_github_scout.py
# Compiled at: 2017-11-12 08:36:44
"""
Repo Scout
Copyright (C) 2017  JValck - Setarit

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Setarit - parcks[at]setarit.com
"""
from __future__ import absolute_import
import unittest, json
from src.network.scout.github_scout import GitHubScout
try:
    from unittest.mock import patch
    from unittest.mock import mock
except ImportError:
    from mock import patch
    import mock

def mocked_request_get(*args, **kwargs):
    json_string = '[\n          {\n            "name": "debian",\n            "path": "debian",\n            "sha": "a2020dddb26679443870ca853ac6b7488dd4210d",\n            "size": 0,\n            "url": "http://api.example.com/fileOnly",\n            "html_url": "https://github.com/Parcks/plugins/tree/master/debian",\n            "git_url": "https://api.github.com/repos/Parcks/plugins/git/trees/a2020dddb26679443870ca853ac6b7488dd4210d",\n            "download_url": null,\n            "type": "dir",\n            "_links": {\n              "self": "https://api.github.com/repos/Parcks/plugins/contents/debian?ref=master",\n              "git": "https://api.github.com/repos/Parcks/plugins/git/trees/a2020dddb26679443870ca853ac6b7488dd4210d",\n              "html": "https://github.com/Parcks/plugins/tree/master/debian"\n            }\n          },\n          {\n            "name": "fedora",\n            "path": "fedora",\n            "sha": "d564d0bc3dd917926892c55e3706cc116d5b165e",\n            "size": 0,\n            "url": "http://api.example.com/fileOnly",\n            "html_url": "https://github.com/Parcks/plugins/tree/master/fedora",\n            "git_url": "https://api.github.com/repos/Parcks/plugins/git/trees/d564d0bc3dd917926892c55e3706cc116d5b165e",\n            "download_url": null,\n            "type": "dir",\n            "_links": {\n              "self": "https://api.github.com/repos/Parcks/plugins/contents/fedora?ref=master",\n              "git": "https://api.github.com/repos/Parcks/plugins/git/trees/d564d0bc3dd917926892c55e3706cc116d5b165e",\n              "html": "https://github.com/Parcks/plugins/tree/master/fedora"\n            }\n          },\n          {\n            "name": "testPlugin.ppl",\n            "path": "testPlugin.ppl",\n            "sha": "a7ac9a74c61a993fe9c8129689fb5594eff74621",\n            "size": 213,\n            "url": "http://api.example.com/fileOnly",\n            "html_url": "https://github.com/Parcks/plugins/blob/master/testPlugin.ppl",\n            "git_url": "https://api.github.com/repos/Parcks/plugins/git/blobs/a7ac9a74c61a993fe9c8129689fb5594eff74621",\n            "download_url": "https://raw.githubusercontent.com/Parcks/plugins/master/testPlugin.ppl",\n            "type": "file",\n            "_links": {\n              "self": "https://api.github.com/repos/Parcks/plugins/contents/testPlugin.ppl?ref=master",\n              "git": "https://api.github.com/repos/Parcks/plugins/git/blobs/a7ac9a74c61a993fe9c8129689fb5594eff74621",\n              "html": "https://github.com/Parcks/plugins/blob/master/testPlugin.ppl"\n            }\n          }\n        ]'
    json_only_file = '[\n          {\n            "name": "testPlugin.ppl",\n            "path": "testPlugin.ppl",\n            "sha": "a7ac9a74c61a993fe9c8129689fb5594eff74621",\n            "size": 213,\n            "url": "http://api.example.com/fileOnly",\n            "html_url": "https://github.com/Parcks/plugins/blob/master/testPlugin.ppl",\n            "git_url": "https://api.github.com/repos/Parcks/plugins/git/blobs/a7ac9a74c61a993fe9c8129689fb5594eff74621",\n            "download_url": "https://raw.githubusercontent.com/Parcks/plugins/master/testPlugin.ppl",\n            "type": "file",\n            "_links": {\n              "self": "https://api.github.com/repos/Parcks/plugins/contents/testPlugin.ppl?ref=master",\n              "git": "https://api.github.com/repos/Parcks/plugins/git/blobs/a7ac9a74c61a993fe9c8129689fb5594eff74621",\n              "html": "https://github.com/Parcks/plugins/blob/master/testPlugin.ppl"\n            }\n          }\n        ]'

    class MockResponse:

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://api.example.com':
        return MockResponse(json.loads(json_string), 200)
    else:
        if args[0] == 'http://api.example.com/fileOnly':
            return MockResponse(json.loads(json_only_file), 200)
        return MockResponse(None, 404)


class TestGitHubScout(unittest.TestCase):

    def setUp(self):
        self.scout = GitHubScout()

    @mock.patch('requests.get', side_effect=mocked_request_get)
    @patch.object(GitHubScout, 'find_in_request_contents')
    def test_find_calls_find_in_request_contents(self, mock, patched_requests):
        self.scout.find('owner', 'name', 'file')
        self.assertTrue(mock.called)

    @mock.patch('requests.get', side_effect=mocked_request_get)
    @patch.object(GitHubScout, '_analyse_contents')
    def test_find_in_requests_contents_calls__analyse_contents(self, mock, patched_requests):
        self.scout.find_in_request_contents('http://api.example.com', 'dummy.file')
        self.assertTrue(mock.called)

    @mock.patch('requests.get', side_effect=mocked_request_get)
    @patch.object(GitHubScout, '_analyse_contents')
    def test_find_in_requests_contents_does_not_call__analyse_contents_on_bad_url(self, mock, patched_requests):
        self.scout.find_in_request_contents('http://bad.url', 'dummy.file')
        self.assertFalse(mock.called)

    @mock.patch('requests.get', side_effect=mocked_request_get)
    @patch.object(GitHubScout, 'find_in_request_contents')
    def test_find_in_directory_calls_find_in_request_contents(self, mock, patched_requests):
        self.scout.find_in_directory('owner', 'name', 'dir', 'file')
        self.assertTrue(mock.called)

    @mock.patch('requests.get', side_effect=mocked_request_get)
    def test_find_in_request_contents_returns_download_url_if_found(self, patched_requests):
        result = self.scout.find_in_request_contents('http://api.example.com', 'testPlugin.ppl')
        self.assertEqual('https://raw.githubusercontent.com/Parcks/plugins/master/testPlugin.ppl', result)

    @mock.patch('requests.get', side_effect=mocked_request_get)
    def test_find_in_request_contents_returns_None_if_not_found(self, patched_requests):
        result = self.scout.find_in_request_contents('http://api.example.com', 'notFound')
        self.assertIsNone(result)