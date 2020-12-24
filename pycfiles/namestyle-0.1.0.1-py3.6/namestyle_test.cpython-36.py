# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\namestyle\namestyle_test.py
# Compiled at: 2017-03-28 00:02:24
# Size of source mod 2**32: 1613 bytes
import os, sys, traceback, unittest
from namestyle_impl import Sentence, Style

class Test_DoWhatEverYourWant(unittest.TestCase):

    @property
    def pascal(self):
        return 'DoWhatEverYourWant'

    @property
    def camel(self):
        return 'doWhatEverYourWant'

    @property
    def python(self):
        return 'do_what_ever_your_want'

    @property
    def sentence(self):
        return 'Do what ever your want'

    def eq_sequence(self, s: Sentence):
        self.assertSequenceEqual(s.words, ('do', 'what', 'ever', 'your', 'want'))

    def test_pascal(self):
        s = Sentence(self.pascal, Style.PASCAL)
        self.eq_sequence(s)
        self.assertEqual(s.format(Style.PASCAL), self.pascal)

    def test_camel(self):
        s = Sentence(self.camel, Style.CAMEL)
        self.eq_sequence(s)
        self.assertEqual(s.format(Style.CAMEL), self.camel)

    def test_python(self):
        s = Sentence(self.python, Style.PYTHON)
        self.eq_sequence(s)
        self.assertEqual(s.format(Style.PYTHON), self.python)

    def test_sentence(self):
        s = Sentence(self.sentence, Style.SENTENCE)
        self.eq_sequence(s)
        self.assertEqual(s.format(Style.SENTENCE), self.sentence)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()
        input()


if __name__ == '__main__':
    main()