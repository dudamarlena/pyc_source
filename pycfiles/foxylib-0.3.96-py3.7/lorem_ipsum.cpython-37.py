# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/lorem_ipsum/lorem_ipsum.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 352 bytes
import os
from foxylib.tools.file.file_tool import FileTool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class LoremIpsum:

    @classmethod
    def lang2str(cls, lang):
        filepath = os.path.join(FILE_DIR, '{}.txt'.format(lang))
        s = FileTool.filepath2utf8(filepath)
        return s