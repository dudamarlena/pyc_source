# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/native/inspect/tests/test_inspect_tool.py
# Compiled at: 2020-02-07 17:13:26
# Size of source mod 2**32: 445 bytes
import logging
from unittest import TestCase
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.inspect.inspect_tool import InspectTool

class TestInspectTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        x = None
        hyp = InspectTool.variable2name(x)
        ref = 'x'
        self.assertEqual(hyp, ref)