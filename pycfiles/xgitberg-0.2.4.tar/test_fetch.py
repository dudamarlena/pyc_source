# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_fetch.py
# Compiled at: 2016-03-02 12:38:36
import os, unittest
from gitenberg.book import Book
from gitenberg.fetch import BookFetcher
from gitenberg import config

class TestBookFetcher(unittest.TestCase):

    def setUp(self):
        self.book = Book(1283)
        self.fetcher = BookFetcher(self.book)

    def test_make_local_path(self):
        self.fetcher.make_local_path()
        self.assertTrue(os.path.exists(config.data['library_path'] + '/1283'))

    def test_remote_fetch(self):
        self.fetcher.fetch_remote_book_to_local_path()
        self.assertTrue(os.path.exists(config.data['library_path'] + '/1283/1283.txt'))

    def tearDown(self):
        self.book.remove()