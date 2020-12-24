# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/prettylogger/tests.py
# Compiled at: 2014-07-28 23:39:29
from unittest import TestCase
from prettylogger.utils import prettify

class TestPrettyLogger(TestCase):

    def test_prettify_with_strings(self):
        given = 'this is a string'
        expected = 'this is a string'
        self.assertEqual(expected, prettify(given))

    def test_prettiffy_with_numbers(self):
        given = 12
        expected = '12'
        self.assertEqual(expected, prettify(given))
        given = 1.23
        expected = '1.23'
        self.assertEqual(expected, prettify(given))

    def test_prettify_with_lists(self):
        given = [
         1, 2, 3, 4, 5]
        expected = '[1, 2, 3, 4, 5]'
        self.assertEqual(expected, prettify(given))

    def test_prettify_with_dictionaries(self):
        given = {'firstname': 'arnelle', 'lastname': 'balane'}
        expected = '{\n    lastname: balane,\n    firstname: arnelle\n}'
        self.assertEqual(expected, prettify(given))

    def test_prettify_with_tuples(self):
        given = (1, 2, 3)
        expected = '(\n    1,\n    2,\n    3,\n)'
        self.assertEqual(expected, prettify(given))

    def test_prettify_with_lists(self):
        given = [
         1, 2, 3]
        expected = '[\n    1,\n    2,\n    3\n]'
        self.assertEqual(expected, prettify(given))