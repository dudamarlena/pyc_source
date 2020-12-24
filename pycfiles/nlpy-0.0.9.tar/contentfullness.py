# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/test/basic/contentfullness.py
# Compiled at: 2015-01-07 03:12:01
import unittest
from nlpy.basic.contentfulness import ContentfullnessEstimator

class ContentfullnessEstimatorTest(unittest.TestCase):

    def test(self):
        ce = ContentfullnessEstimator()
        print ce.estimate(['China', 'travel'])
        print ce.estimate(['country', 'travel'])
        print ce.estimate(['yes', 'know'])
        print ce.estimate(['cook', 'cake'])

    def test_ranking(self):
        ce_f = ContentfullnessEstimator()
        ce_r = ContentfullnessEstimator(source='ranking')
        ce_s = ContentfullnessEstimator(source='/home/hadoop/works/chat/resources/topic_based_questions/just_questions.txt')
        testcases = ['hobby', 'China', 'Philippines']
        for case in testcases:
            print case, ce_f.estimate_word(case), ce_r.estimate_word(case), ce_s.estimate_word(case)