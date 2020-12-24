# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/tests/BlockLocatorTestCases.py
# Compiled at: 2011-12-25 05:31:43
import unittest
from halicea.lib.codeBlocksHelpers import *

class BlockLocatorTestCase(unittest.TestCase):

    def setUp(self):
        self.blockContent = 'first\nsecond\nthirt\nfourth\nfifth'
        self.getTmpl = '$blindent## $blockname ##\n#content#\n$blindent## end_$blockname ##\n'

        def beginMatch(line):
            if line.strip().startswith('## ') and line.strip().endswith(' ##'):
                return line.strip()[3:-2].strip()
            else:
                return
                return

        def endMatch(line):
            return line.strip().startswith('## end') and line.strip().endswith(' ##')

        self.locatorHal = HalCodeBlockLocator()
        self.locatorGen = GenericCbl(beginMatch, endMatch, self.getTmpl)

    def test_HalLocator(self):
        result = self.locatorHal.createValidBlock('test', self.blockContent.split('\n'), blIndent=0, indent=4)
        expected = '{%block test%}\n    first\n    second\n    thirt\n    fourth\n    fifth\n{%endblock%}\n'
        self.assertEquals(result, expected)

    def test_GenLocator(self):
        result = self.locatorGen.createValidBlock('test', self.blockContent.split('\n'), blIndent=0, indent=4)
        expected = '## test ##\n    first\n    second\n    thirt\n    fourth\n    fifth\n## end_test ##\n'
        self.assertEquals(result, expected)