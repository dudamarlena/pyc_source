# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_book.py
# Compiled at: 2018-10-24 01:11:21
import os, unittest
from mock import patch
import gitenberg
from gitenberg.book import Book

class TestBookPath(unittest.TestCase):

    def setUp(self):
        self.test_book_dir = 'test_book'

        def here(appname):
            return os.path.join(os.path.dirname(__file__), 'test_data')

        with patch.object(gitenberg.config.appdirs, 'user_config_dir', here) as (path):
            with patch('github3.login') as (login):
                self.login = login
                self.book = Book(1234)

    def test_remote_path(self):
        self.assertEqual(self.book.remote_path, '1/2/3/1234/')

    def test_local_path(self):
        self.assertTrue(self.book.local_path.endswith('/1234'))

    def test_remote_path_below_ten(self):
        with patch('github3.login'):
            self.book = Book(7)
            self.assertEqual(self.book.remote_path, '0/7/')

    @patch('os.makedirs')
    @patch('os.chmod')
    def test_make_existing_local_path(self, mock_chmod, mock_makedirs):
        self.book.set_local_path_ifexists(self.test_book_dir)
        self.book.make_local_path()
        mock_makedirs.assert_not_called()
        mock_chmod.assert_not_called()