# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_old_metadata.py
# Compiled at: 2018-03-06 15:16:12
import unittest
from mock import MagicMock
from gitenberg.util.catalog import BookMetadata

class TestBookMetadata(unittest.TestCase):

    def setUp(self):
        mock_book = MagicMock()
        mock_book.book_id = 1234
        self.rdf_library = './gitenberg/tests/test_data/rdf_library'
        self.meta = BookMetadata(mock_book, rdf_library=self.rdf_library)

    def test_init(self):
        self.assertEqual(self.meta.rdf_path, ('{0}/1234/pg1234.rdf').format(self.rdf_library))

    def test_parse_rdf(self):
        self.meta.parse_rdf()
        self.assertEqual(self.meta.agents('editor')[0]['agent_name'], 'Conant, James Bryant')
        self.assertEqual(self.meta.title, 'Organic Syntheses\r\nAn Annual Publication of Satisfactory Methods for the Preparation of Organic Chemicals')