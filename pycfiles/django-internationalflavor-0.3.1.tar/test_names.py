# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_names.py
# Compiled at: 2017-01-28 08:53:07
from __future__ import unicode_literals
from django.test import SimpleTestCase
from internationalflavor.names.utils import split_name

class NameSplitTestCase(SimpleTestCase):

    def test_nl_split(self):
        self.assertEqual(split_name(b'John de Boer', b'NL'), [b'John', b'de', b'Boer'])
        self.assertEqual(split_name(b'John van de Boer', b'NL'), [b'John', b'van de', b'Boer'])
        self.assertEqual(split_name(b'John Boer', b'NL'), [b'John', b'', b'Boer'])
        self.assertEqual(split_name(b'John van de Boer-van Janssen', b'NL'), [b'John', b'van de', b'Boer-van Janssen'])
        self.assertEqual(split_name(b'John Boer Bakker', b'NL'), [b'John', b'', b'Boer Bakker'])
        self.assertEqual(split_name(b'John Boer Bakker', b'NL', long_first=True), [b'John Boer', b'', b'Bakker'])
        self.assertEqual(split_name(b'John de Boer Bakker', b'NL', long_first=True), [b'John', b'de', b'Boer Bakker'])

    def test_world_split(self):
        self.assertEqual(split_name(b'James Darwin', b'001'), [b'James', b'Darwin'])
        self.assertEqual(split_name(b'James Darwin Doe', b'001'), [b'James', b'Darwin Doe'])
        self.assertEqual(split_name(b'James Darwin Doe', b'001', long_first=True), [b'James Darwin', b'Doe'])