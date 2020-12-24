# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tests/test_invalid_character_checker.py
# Compiled at: 2019-12-05 17:01:18
# Size of source mod 2**32: 1191 bytes
import unittest
from nacc.uds3 import Field
from nacc.redcap2nacc import check_for_bad_characters

class TestInvalidCharacters(unittest.TestCase):

    def test_find_any_characters(self):
        field = Field('FOTHMUSX', 'Char', 0, 1, allowable_values='', value='agf&dfg')
        found = check_for_bad_characters(field)
        self.assertTrue(found)

    def test_many_characters(self):
        field = Field('FOTHMUSX', 'Char', 0, 1, allowable_values='', value='ag%fd"fg')
        found_many = check_for_bad_characters(field)
        many = len(found_many)
        self.assertEqual(many, 2)

    def test_closed_double_quotes(self):
        field = Field('FOTHMUSX', 'Char', 0, 1, allowable_values='', value='ag"fd"fg')
        found_two_doublequotes = check_for_bad_characters(field)
        dups = found_two_doublequotes[0]
        self.assertEqual(dups, '" (2)')

    def test_closed_single_quotes(self):
        field = Field('FOTHMUSX', 'Char', 0, 1, allowable_values='', value="ag'fdf'g")
        found_two_quotes = check_for_bad_characters(field)
        dups1 = found_two_quotes[0]
        self.assertEqual(dups1, "' (2)")


if __name__ == '__main__':
    unittest.main()