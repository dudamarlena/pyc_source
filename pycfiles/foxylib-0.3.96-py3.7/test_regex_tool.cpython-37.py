# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/regex/tests/test_regex_tool.py
# Compiled at: 2020-01-28 00:57:02
# Size of source mod 2**32: 1245 bytes
import logging, re
from unittest import TestCase
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import format_str

class TestRegexTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp1 = format_str('{}{{2,}}', 'a')
        ref1 = 'a{2,}'
        self.assertEqual(hyp1, ref1)
        m = re.match(hyp1, 'aaa')
        self.assertTrue(m)

    def test_02(self):
        str_in = 'hello world'
        p1 = re.compile('\\w+ \\w+')
        m1 = RegexTool.pattern_str2match_full(p1, str_in)
        self.assertIsNotNone(m1)
        p2 = re.compile('\\w+ \\w')
        m2 = RegexTool.pattern_str2match_full(p2, str_in)
        self.assertIsNone(m2)
        p3 = re.compile('\\w \\w+')
        m3 = RegexTool.pattern_str2match_full(p3, str_in)
        self.assertIsNone(m3)
        p4 = re.compile('\\w* \\w*')
        m4 = RegexTool.pattern_str2match_full(p4, str_in)
        self.assertIsNotNone(m4)
        p5 = re.compile('H\\w* \\w*D', re.I)
        m5 = RegexTool.pattern_str2match_full(p5, str_in)
        self.assertIsNotNone(m5)