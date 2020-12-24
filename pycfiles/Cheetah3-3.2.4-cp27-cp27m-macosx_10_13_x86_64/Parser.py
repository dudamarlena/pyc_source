# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Parser.py
# Compiled at: 2019-09-22 10:12:27
import unittest
from Cheetah import Parser

class ArgListTest(unittest.TestCase):

    def setUp(self):
        super(ArgListTest, self).setUp()
        self.al = Parser.ArgList()

    def test_merge1(self):
        """
        Testing the ArgList case results from
        Template.Preprocessors.test_complexUsage
        """
        self.al.add_argument('arg')
        expect = [('arg', None)]
        self.assertEqual(expect, self.al.merge())
        return

    def test_merge2(self):
        """
        Testing the ArgList case results from
        SyntaxAndOutput.BlockDirective.test4
        """
        self.al.add_argument('a')
        self.al.add_default('999')
        self.al.next()
        self.al.add_argument('b')
        self.al.add_default('444')
        expect = [
         ('a', '999'), ('b', '444')]
        self.assertEqual(expect, self.al.merge())

    def test_merge3(self):
        """
        Testing the ArgList case results from
        SyntaxAndOutput.BlockDirective.test13
        """
        self.al.add_argument('arg')
        self.al.add_default("'This is my block'")
        expect = [('arg', "'This is my block'")]
        self.assertEqual(expect, self.al.merge())