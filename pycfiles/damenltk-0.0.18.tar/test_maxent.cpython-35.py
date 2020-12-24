# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_maxent.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1788 bytes
import unittest
from nltk.classify import maxent

class TddInPythonExample(unittest.TestCase):

    def test_maxent_returns_correct_result(self):
        train = [
         (
          {'a': 1, 'b': 1, 'c': 1}, 'y'),
         (
          {'a': 5, 'b': 5, 'c': 5}, 'x'),
         (
          {'a': 0.9, 'b': 0.9, 'c': 0.9}, 'y'),
         (
          {'a': 5.5, 'b': 5.4, 'c': 5.3}, 'x'),
         (
          {'a': 0.8, 'b': 1.2, 'c': 1}, 'y'),
         (
          {'a': 5.1, 'b': 4.9, 'c': 5.2}, 'x')]
        test = [
         {'a': 1, 'b': 0.8, 'c': 1.2},
         {'a': 5.2, 'b': 5.1, 'c': 5}]
        encoding = maxent.TypedMaxentFeatureEncoding.train(train, count_cutoff=3, alwayson_features=True)
        classifier = maxent.MaxentClassifier.train(train, bernoulli=False, encoding=encoding, trace=0)
        self.assertEqual(classifier.classify_many(test), ['y', 'x'])