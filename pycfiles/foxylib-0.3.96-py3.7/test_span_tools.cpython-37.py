# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/span/tests/test_span_tools.py
# Compiled at: 2020-01-28 14:31:32
# Size of source mod 2**32: 1978 bytes
import logging, re
from unittest import TestCase
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.string_tool import StringTool

class TestSpanTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)
        p1 = re.compile('\\s+')

        def f_gap2valid(span_gap):
            m = StringTool.str_span_pattern2match_full('a b c d e', span_gap, p1)
            return m is not None

        spans_pair1 = [
         [
          (0, 1), (4, 5)], [(2, 3)]]
        hyp1 = list(SpanTool.spans_list_f_gap2j_tuples_valid(spans_pair1, f_gap2valid))
        self.assertEqual(hyp1, [(0, 0)])
        spans_pair2 = [
         [
          (0, 1), (6, 7), (8, 9)], [(2, 3), (4, 5)]]
        hyp2 = list(SpanTool.spans_list_f_gap2j_tuples_valid(spans_pair2, f_gap2valid))
        self.assertEqual(hyp2, [(0, 0)])
        spans_pair3 = [
         [
          (2, 3), (4, 5)], [(0, 1), (6, 7), (8, 9)]]
        hyp3 = list(SpanTool.spans_list_f_gap2j_tuples_valid(spans_pair3, f_gap2valid))
        self.assertEqual(hyp3, [(1, 1)])
        spans_pair4 = [
         [
          (2, 3), (4, 5)], [(8, 9), (0, 1), (6, 7)]]
        hyp4 = list(SpanTool.spans_list_f_gap2j_tuples_valid(spans_pair4, f_gap2valid))
        self.assertEqual(hyp4, [(1, 2)])
        spans_pair5 = [
         [
          (2, 3), (6, 7)], [(8, 9), (0, 1), (4, 5)], [(6, 7)]]
        hyp5 = list(SpanTool.spans_list_f_gap2j_tuples_valid(spans_pair5, f_gap2valid))
        self.assertEqual(hyp5, [(0, 2, 0)])