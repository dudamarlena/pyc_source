# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/jinja2/tests/test_jinja2_tools.py
# Compiled at: 2019-12-17 00:25:14
# Size of source mod 2**32: 402 bytes
import os
from unittest import TestCase
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class Jinja2ToolTest(TestCase):

    def test_01(self):
        filepath = os.path.join(FILE_DIR, 'test_01.part.txt')
        s = Jinja2Tool.tmplt_file2str(filepath, {'name': 'Peter'})
        self.assertEqual('hello, Peter', s)