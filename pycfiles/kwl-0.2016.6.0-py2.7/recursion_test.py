# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/kwl2text/recursion_test.py
# Compiled at: 2016-02-06 05:55:41
import sys, os, recursion, unittest

class KWLTest(unittest.TestCase):

    def setUp(self):
        self.psr = recursion.recursionParser()
        self.maxDiff = None
        return

    def testToken(self):
        alpha = 'abc'
        number = '12'
        sem_alpha = {'t': 'alpha', 'v': 'abc'}
        sem_number = {'t': 'number', 'v': '12'}
        self.assertEquals('1', self.psr.parse('1', rule_name='expression'))
        self.assertEquals(['{', '1', '}'], self.psr.parse('{1}', rule_name='expression'))
        self.assertEquals(['{', ['{', '1', '}'], '}'], self.psr.parse('{{1}}', rule_name='expression'))
        self.assertEquals(['{', ['{', ['{', '1', '}'], '}'], '}'], self.psr.parse('{{{1}}}', rule_name='expression'))
        print self.psr.parse('{{{1}}}', rule_name='sentence')
        print self.psr.parse('{{{1}}} {1}', rule_name='sentence')
        print self.psr.parse('{{{1}}} {1} 1', rule_name='sentence')


if __name__ == '__main__':
    unittest.main()