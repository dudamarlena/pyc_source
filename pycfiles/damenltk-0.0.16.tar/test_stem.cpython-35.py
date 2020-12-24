# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_stem.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1340 bytes
import unittest, nltk
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

class TddInPythonExample(unittest.TestCase):

    def test_stem_returns_correct_result(self):
        stemmer = PorterStemmer()
        self.assertEqual(stemmer.stem('vuelos'), 'vuelo')

    def test_snowball_stem_returns_correct_result(self):
        sb = SnowballStemmer('english').stem('generously')
        self.assertEqual(sb, 'generous')