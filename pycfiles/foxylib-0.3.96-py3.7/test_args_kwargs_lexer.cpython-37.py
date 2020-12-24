# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/lexer/tests/test_args_kwargs_lexer.py
# Compiled at: 2019-02-26 14:49:41
# Size of source mod 2**32: 651 bytes
from unittest import TestCase
from foxylib.tools.lexer.args_kwargs_lexer import ArgsKwargsLexer

class ArgsKwargsLexerTest(TestCase):

    def test_success_01(self):
        s = '"los angeles" nickname="L. A."'
        hyp = ArgsKwargsLexer.str2args_kwargs_pair(s)
        ref = (['los angeles'], {'nickname': 'L. A.'})
        self.assertEqual(hyp, ref)

    def test_success_02(self):
        s = '"los angeles" "santa barbara" tags="L. A.","San Francisco", "S.F."'
        hyp = ArgsKwargsLexer.str2args_kwargs_pair(s)
        ref = (['los angeles', 'santa barbara'], {'tags': '"L. A.","San Francisco", "S.F."'})
        self.assertEqual(hyp, ref)