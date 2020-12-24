# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_fetch.py
# Compiled at: 2018-08-23 10:55:00
import unittest
from mock import MagicMock
from mock import patch
from gitenberg.fetch import BookFetcher
from gitenberg.parameters import PG_RSYNC

class TestBookFetcher(unittest.TestCase):

    def setUp(self):
        self.test_book_dir = './gitenberg/tests/test_data/test_book'
        self.remote_path = '1234/1234.txt'
        mock_book = MagicMock()
        mock_book.local_path = self.test_book_dir
        mock_book.remote_path = self.remote_path
        self.fetcher = BookFetcher(mock_book)

    @patch('sh.rsync')
    def test_remote_fetch(self, mock_rsync):
        self.fetcher.fetch_remote_book_to_local_path()
        mock_rsync.assert_called_once_with('-rvhz', ('{}1234/1234.txt').format(PG_RSYNC), self.test_book_dir + '/', '--exclude-from=exclude.txt')