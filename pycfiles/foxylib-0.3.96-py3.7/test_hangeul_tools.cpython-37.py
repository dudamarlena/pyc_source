# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/hangeul/tests/test_hangeul_tools.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 539 bytes
from unittest import TestCase
from foxylib.tools.hangeul.hangeul_tool import HangeulTool

class HangeulToolTest(TestCase):

    def test_01(self):
        str_in = '나의 살던 고향은 꽃피는 산골~! >.<'
        hyp = HangeulTool.str2compatibility_choseung(str_in)
        ref = 'ㄴㅇ ㅅㄷ ㄱㅎㅇ ㄲㅍㄴ ㅅㄱ~! >.<'
        self.assertEqual(hyp, ref)

    def test_02(self):
        str_in = '판'
        hyp = HangeulTool.str2compatibility_choseung(str_in)
        ref = 'ㅍ'
        self.assertEqual(hyp, ref)