# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/url/tests/test_url_tool.py
# Compiled at: 2020-01-21 01:51:39
# Size of source mod 2**32: 643 bytes
import logging, os
from functools import reduce
from unittest import TestCase
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import UrlpathTool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 4, FILE_DIR)

class TestUrlTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = UrlpathTool.filepath_pair2url(FILE_DIR, REPO_DIR)
        ref = '/foxylib/tools/url/tests/'
        self.assertEqual(hyp, ref)