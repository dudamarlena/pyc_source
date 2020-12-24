# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/github/tests/test_handlers.py
# Compiled at: 2016-10-26 23:34:56
# Size of source mod 2**32: 2769 bytes
import os
from unittest import TestCase
from ....utils import transform_ipynb_uri
from ..handlers import uri_rewrites
uri_rewrite_list = uri_rewrites()

class TestRewrite(TestCase):

    def assert_rewrite(self, uri, rewrite):
        new = transform_ipynb_uri(uri, uri_rewrite_list)
        self.assertEqual(new, rewrite)

    def assert_rewrite_ghe(self, uri, rewrite):
        os.environ['GITHUB_API_URL'] = 'https://example.com/api/v3/'
        uri_rewrite_ghe_list = uri_rewrites()
        os.environ.pop('GITHUB_API_URL', None)
        new = transform_ipynb_uri(uri, uri_rewrite_ghe_list)
        self.assertEqual(new, rewrite)

    def test_githubusercontent(self):
        uri = 'https://raw.githubusercontent.com/user/reopname/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/blob/deadbeef/a mřížka.ipynb'
        self.assert_rewrite(uri, rewrite)

    def test_blob(self):
        uri = 'https://github.com/user/reopname/blob/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/blob/deadbeef/a mřížka.ipynb'
        self.assert_rewrite(uri, rewrite)

    def test_raw_uri(self):
        uri = 'https://github.com/user/reopname/raw/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/blob/deadbeef/a mřížka.ipynb'
        self.assert_rewrite(uri, rewrite)

    def test_raw_subdomain(self):
        uri = 'https://raw.github.com/user/reopname/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/blob/deadbeef/a mřížka.ipynb'
        self.assert_rewrite(uri, rewrite)

    def test_tree(self):
        uri = 'https://github.com/user/reopname/tree/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/tree/deadbeef/a mřížka.ipynb'
        self.assert_rewrite(uri, rewrite)

    def test_userrepo(self):
        uri = 'username/reponame'
        rewrite = '/github/username/reponame/tree/master/'
        self.assert_rewrite(uri, rewrite)

    def test_user(self):
        uri = 'username'
        rewrite = '/github/username/'
        self.assert_rewrite(uri, rewrite)

    def test_ghe_blob(self):
        uri = 'https://example.com/user/reopname/blob/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/blob/deadbeef/a mřížka.ipynb'
        self.assert_rewrite_ghe(uri, rewrite)

    def test_ghe_raw_uri(self):
        uri = 'https://example.com/user/reopname/raw/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/blob/deadbeef/a mřížka.ipynb'
        self.assert_rewrite_ghe(uri, rewrite)

    def test_ghe_tree(self):
        uri = 'https://example.com/user/reopname/tree/deadbeef/a mřížka.ipynb'
        rewrite = '/github/user/reopname/tree/deadbeef/a mřížka.ipynb'
        self.assert_rewrite_ghe(uri, rewrite)