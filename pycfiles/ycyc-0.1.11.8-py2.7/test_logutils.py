# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/base/test_logutils.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
import sys, thread
from ycyc.base import logutils

class TestLoggerInfo(TestCase):

    def test_usage(self):
        frames = sys._current_frames()
        frame = frames[thread.get_ident()]
        loginfo = logutils.LoggerInfo()
        self.assertIs(frame, loginfo.frame)
        line_based = 18
        self.assertEqual(line_based + 1, loginfo.line_no)
        self.assertEqual(line_based + 2, loginfo.line_no)
        self_func = self.test_usage.im_func
        self.assertEqual(self_func.__name__, loginfo.code_name)