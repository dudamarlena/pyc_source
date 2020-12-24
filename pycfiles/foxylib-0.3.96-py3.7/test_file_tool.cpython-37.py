# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/file/tests/test_file_tool.py
# Compiled at: 2020-01-01 15:08:00
# Size of source mod 2**32: 500 bytes
import os
from mimetypes import guess_type
from unittest import TestCase
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestFileTool(TestCase):

    def test_01(self):
        filepath = os.path.join(os.path.dirname(FILE_DIR), 'file_tool.py')
        hyp = FileTool.filepath2mimetype(filepath)
        self.assertEqual(hyp, MimetypeTool.V.TEXT_XPYTHON)