# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/tests/test_utils.py
# Compiled at: 2017-05-09 16:03:28
# Size of source mod 2**32: 6005 bytes
from django.test import TestCase
from mote.utils import deepmerge

class UtilsTestCase(TestCase):

    def test_deepmerge(self):
        source = {'one': {'aaa': 1, 'bbb': 2}, 
         'two': [1, 2, 3], 
         'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks'}},
                   {'actor': {'name': 'Denzel', 'surname': 'Washington'}}], 
         
         'four': [
                  {'actor': {'name': 'Alec', 'surname': 'Baldwin'}},
                  {'actor': {'name': 'Brad', 'surname': 'Pitt'}}], 
         
         'five': [
                  {'movie': {'title': 'Good Will Hunting', 
                             'actors': [
                                        {'actor': {'name': 'Ben', 'surname': 'Affleck'}}]}}]}
        delta = {'one': {'bbb': 777, 'ccc': 888}, 
         'two': [3, 4, 5], 
         'three': {'actor': {'name': 'Colin'}}, 
         'four': [
                  {'actor': {'name': 'Stephen'}},
                  {'actor': {'name': 'Harrison', 'surname': 'Ford'}},
                  {'actor': {'name': 'William'}}], 
         
         'five': [
                  {'movie': {'title': 'Good Will Hunting', 
                             'actors': [
                                        {'actor': {'name': 'Matt', 'surname': 'Damon'}},
                                        {'actor': {'name': 'Casey'}}]}}], 
         
         'infinity': {'a': 0}}
        result = deepmerge(source, delta)
        self.assertEqual({'one': {'aaa': 1, 'bbb': 777, 'ccc': 888}, 
         'two': [3, 4, 5], 
         'three': [
                   {'actor': {'name': 'Colin', 'surname': 'Hanks'}}], 
         
         'four': [
                  {'actor': {'name': 'Stephen', 'surname': 'Baldwin'}},
                  {'actor': {'name': 'Harrison', 'surname': 'Ford'}},
                  {'actor': {'name': 'William', 'surname': 'Baldwin'}}], 
         
         'five': [
                  {'movie': {'title': 'Good Will Hunting', 
                             'actors': [
                                        {'actor': {'name': 'Matt', 'surname': 'Damon'}},
                                        {'actor': {'name': 'Casey', 'surname': 'Affleck'}}]}}], 
         
         'infinity': {'a': 0}}, result)

    def test_deepmerge_nones(self):
        source = None
        delta = None
        result = deepmerge(source, delta)
        assert (result, None)
        source = {'one': {'aaa': 1, 'bbb': 2}, 
         'two': [1, 2, 3], 
         'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks'}},
                   {'actor': {'name': 'Denzel', 'surname': 'Washington'}}], 
         
         'four': [
                  {'actor': {'name': 'Alec', 'surname': 'Baldwin'}},
                  {'actor': {'name': 'Brad', 'surname': 'Pitt'}}], 
         
         'five': [
                  {'movie': {'title': 'Good Will Hunting', 
                             'actors': [
                                        {'actor': {'name': 'Ben', 'surname': 'Affleck'}}]}}]}
        delta = None
        result = deepmerge(source, delta)
        self.assertEqual(result, source, 'Result must be == source!')
        source = None
        delta = {'one': {'aaa': 1, 'bbb': 2}, 
         'two': [1, 2, 3], 
         'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks'}},
                   {'actor': {'name': 'Denzel', 'surname': 'Washington'}}], 
         
         'four': [
                  {'actor': {'name': 'Alec', 'surname': 'Baldwin'}},
                  {'actor': {'name': 'Brad', 'surname': 'Pitt'}}], 
         
         'five': [
                  {'movie': {'title': 'Good Will Hunting', 
                             'actors': [
                                        {'actor': {'name': 'Ben', 'surname': 'Affleck'}}]}}]}
        result = deepmerge(source, delta)
        self.assertEqual(result, source, 'Result must be == None!')

    def test_list_with_nones(self):
        """`None` values are discarded from lists.
        """
        source = {'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks'}},
                   {'actor': {'name': 'Denzel', 'surname': 'Washington'}}]}
        delta = {'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks'}},
                   None]}
        result = deepmerge(source, delta)
        self.assertEqual(result, {'three': [{'actor': {'name': 'Tom', 'surname': 'Hanks'}}]})

    def test_arbitrary_keys(self):
        """Introduce keys that are not in source.
        """
        source = {'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks'}}]}
        delta = {'three': [
                   {'actor': {'name': 'Tom', 'surname': 'Hanks', 'age': 50}}], 
         
         'four': 1}
        result = deepmerge(source, delta)
        self.assertEqual(result, {'three': [{'actor': {'name': 'Tom', 'surname': 'Hanks', 'age': 50}}], 
         'four': 1})