# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_condorcet.py
# Compiled at: 2012-04-23 20:44:29
from pyvotecore.schulze_method import SchulzeMethod
import unittest

class TestCondorcet(unittest.TestCase):

    def test_grouping_format(self):
        input = [{'count': 12, 'ballot': [['Andrea'], ['Brad'], ['Carter']]}, {'count': 26, 'ballot': [['Andrea'], ['Carter'], ['Brad']]}, {'count': 12, 'ballot': [['Andrea'], ['Carter'], ['Brad']]}, {'count': 13, 'ballot': [['Carter'], ['Andrea'], ['Brad']]}, {'count': 27, 'ballot': [['Brad']]}]
        output = SchulzeMethod(input, ballot_notation='grouping').as_dict()
        self.assertEqual(output, {'candidates': set(['Carter', 'Brad', 'Andrea']), 
           'pairs': {('Andrea', 'Brad'): 63, 
                     ('Brad', 'Carter'): 39, 
                     ('Carter', 'Andrea'): 13, 
                     ('Andrea', 'Carter'): 50, 
                     ('Brad', 'Andrea'): 27, 
                     ('Carter', 'Brad'): 51}, 
           'strong_pairs': {('Andrea', 'Brad'): 63, 
                            ('Carter', 'Brad'): 51, 
                            ('Andrea', 'Carter'): 50}, 
           'winner': 'Andrea'})

    def test_ranking_format(self):
        input = [{'count': 12, 'ballot': {'Andrea': 1, 'Brad': 2, 'Carter': 3}}, {'count': 26, 'ballot': {'Andrea': 1, 'Carter': 2, 'Brad': 3}}, {'count': 12, 'ballot': {'Andrea': 1, 'Carter': 2, 'Brad': 3}}, {'count': 13, 'ballot': {'Carter': 1, 'Andrea': 2, 'Brad': 3}}, {'count': 27, 'ballot': {'Brad': 1}}]
        output = SchulzeMethod(input, ballot_notation='ranking').as_dict()
        self.assertEqual(output, {'candidates': set(['Carter', 'Brad', 'Andrea']), 
           'pairs': {('Andrea', 'Brad'): 63, 
                     ('Brad', 'Carter'): 39, 
                     ('Carter', 'Andrea'): 13, 
                     ('Andrea', 'Carter'): 50, 
                     ('Brad', 'Andrea'): 27, 
                     ('Carter', 'Brad'): 51}, 
           'strong_pairs': {('Andrea', 'Brad'): 63, 
                            ('Carter', 'Brad'): 51, 
                            ('Andrea', 'Carter'): 50}, 
           'winner': 'Andrea'})

    def test_rating_format(self):
        input = [{'count': 12, 'ballot': {'Andrea': 10, 'Brad': 5, 'Carter': 3}}, {'count': 26, 'ballot': {'Andrea': 10, 'Carter': 5, 'Brad': 3}}, {'count': 12, 'ballot': {'Andrea': 10, 'Carter': 5, 'Brad': 3}}, {'count': 13, 'ballot': {'Carter': 10, 'Andrea': 5, 'Brad': 3}}, {'count': 27, 'ballot': {'Brad': 10}}]
        output = SchulzeMethod(input, ballot_notation='rating').as_dict()
        self.assertEqual(output, {'candidates': set(['Carter', 'Brad', 'Andrea']), 
           'pairs': {('Andrea', 'Brad'): 63, 
                     ('Brad', 'Carter'): 39, 
                     ('Carter', 'Andrea'): 13, 
                     ('Andrea', 'Carter'): 50, 
                     ('Brad', 'Andrea'): 27, 
                     ('Carter', 'Brad'): 51}, 
           'strong_pairs': {('Andrea', 'Brad'): 63, 
                            ('Carter', 'Brad'): 51, 
                            ('Andrea', 'Carter'): 50}, 
           'winner': 'Andrea'})


if __name__ == '__main__':
    unittest.main()