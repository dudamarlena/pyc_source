# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subdicts/tests/test_subdicts.py
# Compiled at: 2014-07-09 22:31:26
import unittest
from subdicts import utils

class TestSubDicts(unittest.TestCase):

    def test_parse_given_dictionary_keys(self):
        given = {'firstname': 'arnelle', 'lastname': 'balane'}
        expected = {'firstname': 'arnelle', 'lastname': 'balane'}
        self.assertEqual(expected, utils.parse(given))

    def test_parse_given_simple_nested_dictionary_keys(self):
        given = {'person[firstname]': 'arnelle', 'person[lastname]': 'balane'}
        expected = {'person': {'firstname': 'arnelle', 'lastname': 'balane'}}
        self.assertEqual(expected, utils.parse(given))

    def test_parse_given_deeply_nested_dictionary_keys(self):
        given = {'person[personal_information][name][first]': 'arnelle', 'person[personal_information][name][last]': 'balane', 
           'person[personal_information][gender]': 'male', 
           'person[personal_information][email]': 'arnellebalane@gmail.com', 
           'person[address][province]': 'bohol', 
           'person[address][city][name]': 'tagbilaran city', 
           'person[address][city][zip_code]': '6300'}
        expected = {'person': {'personal_information': {'name': {'first': 'arnelle', 
                                                        'last': 'balane'}, 
                                               'gender': 'male', 
                                               'email': 'arnellebalane@gmail.com'}, 
                      'address': {'province': 'bohol', 
                                  'city': {'name': 'tagbilaran city', 
                                           'zip_code': '6300'}}}}
        self.assertEqual(expected, utils.parse(given))