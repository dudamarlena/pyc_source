# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_old_metadata.py
# Compiled at: 2016-03-02 14:17:40
import unittest
from gitenberg.book import Book
from gitenberg.util.catalog import BookMetadata
from gitenberg import config

class TestBookMetadata(unittest.TestCase):

    def setUp(self):
        book = Book(1234)
        self.rdf_library = config.data['rdf_library']
        self.meta = BookMetadata(book, rdf_library=self.rdf_library)

    def test_init(self):
        self.assertEqual(self.meta.rdf_path, ('{0}/1234/pg1234.rdf').format(self.rdf_library))

    def test_parse_rdf(self):
        self.meta.parse_rdf()
        self.assertEqual(self.meta.agents('editor')[0]['agent_name'], 'Conant, James Bryant')
        self.assertEqual(self.meta.title, 'Organic Syntheses\r\nAn Annual Publication of Satisfactory Methods for the Preparation of Organic Chemicals')