# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Analyzer.py
# Compiled at: 2019-09-22 10:12:27
import unittest
from Cheetah import DirectiveAnalyzer

class AnalyzerTests(unittest.TestCase):

    def test_set(self):
        template = '\n        #set $foo = "bar"\n        Hello ${foo}!\n        '
        calls = DirectiveAnalyzer.analyze(template)
        self.assertEqual(1, calls.get('set'))

    def test_compilersettings(self):
        template = '\n#compiler-settings\nuseNameMapper = False\n#end compiler-settings\n        '
        calls = DirectiveAnalyzer.analyze(template)
        self.assertEqual(1, calls.get('compiler-settings'))