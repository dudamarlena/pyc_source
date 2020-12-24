# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_svc.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1712 bytes
import unittest
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

class TddInPythonExample(unittest.TestCase):

    def test_svc_returns_correct_result(self):
        train_data = [
         (
          {'a': 4, 'b': 1, 'c': 0}, 'ham'),
         (
          {'a': 5, 'b': 2, 'c': 1}, 'ham'),
         (
          {'a': 0, 'b': 3, 'c': 4}, 'spam'),
         (
          {'a': 5, 'b': 1, 'c': 1}, 'ham'),
         (
          {'a': 1, 'b': 4, 'c': 3}, 'spam')]
        classif = SklearnClassifier(SVC(), sparse=False).train(train_data)
        test_data = [{'a': 3, 'b': 2, 'c': 1},
         {'a': 0, 'b': 3, 'c': 7}]
        ccm = classif.classify_many(test_data)
        self.assertEqual(ccm, ['ham', 'spam'])