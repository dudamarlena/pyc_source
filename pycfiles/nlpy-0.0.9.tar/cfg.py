# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/test/syntax/cfg.py
# Compiled at: 2015-01-05 20:11:46
import unittest
from nlpy.syntax.cfg import StanfordCFGParser, BatchStanfordCFGParser
from nlpy.basic import DefaultTokenizer
import corenlp
from nlpy.util import LineIterator

class StanfordCFGParserTest(unittest.TestCase):

    def _test_parse(self):
        testcase = 'One difference from C: I wrote a little wrapper around malloc/free, cymem.'
        tk = DefaultTokenizer()
        p = StanfordCFGParser()
        tree = p.parse(tk.tokenize(testcase))
        print tree

    def test_bath_parse(self):
        tk = DefaultTokenizer()
        p = BatchStanfordCFGParser()
        testcases = ['it turns out good', 'it will work (so it is)']
        tokenized_cases = []
        for case in testcases:
            tokenized_cases.append(tk.tokenize(case))

        p.cache(tokenized_cases)
        p.save('/tmp/jjsjsj.gz')
        p.load('/tmp/jjsjsj.gz')
        print p.parse(tk.tokenize('it will work (so it is)'))

    def _test_terminals(self):
        testcase = 'i cook rice.'
        tk = DefaultTokenizer()
        p = StanfordCFGParser()
        tree = p.parse(tk.tokenize(testcase))
        print p.extract_terminals(tree)