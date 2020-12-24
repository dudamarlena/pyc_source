# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_names.py
# Compiled at: 2017-01-28 09:05:01
# Size of source mod 2**32: 1510 bytes
from __future__ import unicode_literals
from django.test import SimpleTestCase
from internationalflavor.names.utils import split_name, join_name

class NameSplitTestCase(SimpleTestCase):

    def test_nl_split(self):
        self.assertEqual(split_name('John de Boer', 'NL'), ('John', 'de', 'Boer'))
        self.assertEqual(split_name('John van de Boer', 'NL'), ('John', 'van de', 'Boer'))
        self.assertEqual(split_name('John Boer', 'NL'), ('John', '', 'Boer'))
        self.assertEqual(split_name('John van de Boer-van Janssen', 'NL'), ('John',
                                                                            'van de',
                                                                            'Boer-van Janssen'))
        self.assertEqual(split_name('John Boer Bakker', 'NL'), ('John', '', 'Boer Bakker'))
        self.assertEqual(split_name('John Boer Bakker', 'NL', long_first=True), ('John Boer',
                                                                                 '',
                                                                                 'Bakker'))
        self.assertEqual(split_name('John de Boer Bakker', 'NL', long_first=True), ('John',
                                                                                    'de',
                                                                                    'Boer Bakker'))

    def test_world_split(self):
        self.assertEqual(split_name('James Darwin', '001'), ('James', 'Darwin'))
        self.assertEqual(split_name('James Darwin Doe', '001'), ('James', 'Darwin Doe'))
        self.assertEqual(split_name('James Darwin Doe', '001', long_first=True), ('James Darwin',
                                                                                  'Doe'))

    def test_join(self):
        self.assertEqual(join_name('Charles', 'Darwin'), 'Charles Darwin')
        self.assertEqual(join_name('Charles', 'the', 'Darwin'), 'Charles the Darwin')
        self.assertEqual(join_name(*('Charles', 'the', 'Darwin')), 'Charles the Darwin')