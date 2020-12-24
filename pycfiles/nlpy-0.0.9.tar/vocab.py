# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/test/lm/vocab.py
# Compiled at: 2014-11-25 21:01:10
from nlpy.lm import Vocab
from nlpy.util import internal_resource
import unittest
from nlpy.lm.data_generator import RNNDataGenerator

class VocabTest(unittest.TestCase):

    def _test_vocab(self):
        data_path = internal_resource('lm_test/valid')
        v = Vocab()
        v.load(data_path)
        print v.size
        print v.binvector('ergerrghwegr')

    def test_generator(self):
        data_path = internal_resource('lm_test/valid')
        v = Vocab()
        v.load(data_path)
        c = 0
        g = RNNDataGenerator(v, data_path, history_len=0)
        for d in g:
            print d
            c += 1
            if c > 100:
                break