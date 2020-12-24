# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_book.py
# Compiled at: 2016-03-02 12:39:27
import unittest
from gitenberg.book import Book

class TestBookPath(unittest.TestCase):

    def setUp(self):
        self.book = Book(3456)

    def test_remote_path(self):
        self.assertEqual(self.book.remote_path, '3/4/5/3456/')

    def test_local_path(self):
        self.assertTrue(self.book.local_path.endswith('/3456'))


class TestBookPathSubTen(unittest.TestCase):

    def setUp(self):
        self.book = Book(7)

    def test_path_to_pg(self):
        self.assertEqual(self.book.remote_path, '7/')