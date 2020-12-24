# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/html/test/test_html_tools.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 844 bytes
import logging
from unittest import TestCase
from markupsafe import Markup
from foxylib.tools.html.html_tool import wrap_html_tag, escape, join_html
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class TestHTMLTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = wrap_html_tag('asdaf', 'a')
        ref = '<a >asdaf</a>'
        self.assertEqual(str(hyp), ref)

    def test_02(self):
        hyp = escape(wrap_html_tag('asdaf', 'a'))
        ref = '<a >asdaf</a>'
        self.assertEqual(str(hyp), ref)

    def test_03(self):
        hyp = join_html('<a>', [Markup('<b />'), Markup('<c />')])
        ref = '<b />&lt;a&gt;<c />'
        self.assertEqual(str(hyp), ref)