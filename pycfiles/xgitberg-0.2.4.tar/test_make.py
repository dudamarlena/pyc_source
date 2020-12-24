# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_make.py
# Compiled at: 2016-03-02 12:52:48
import os, unittest, sh
from gitenberg.book import Book
from gitenberg.make import LocalRepo
from gitenberg import config

class TestLocalRepo(unittest.TestCase):

    def setUp(self):
        self.book = Book(13529)

        def copy_test_book():
            sh.cp('./gitenberg/tests/test_data/1234', library_path)

        self.book.fetch_remote_book_to_local_path = copy_test_book
        self.book.fetch()

    def test_init(self):
        l_r = LocalRepo(self.book)
        self.assertEqual(l_r.book, self.book)

    def test_init_repo(self):
        l_r = LocalRepo(self.book)
        l_r.add_all_files()
        self.assertTrue(os.path.exists(config.data['library_path'] + '/13529/.git'))

    def tearDown(self):
        self.book.remove()


def null():
    pass