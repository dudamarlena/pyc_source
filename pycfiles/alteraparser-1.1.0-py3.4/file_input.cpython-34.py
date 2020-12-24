# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/io/file_input.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 740 bytes
from .input_stream import InputStream

class FileInput(InputStream):

    def __init__(self, file_path):
        f = open(file_path, 'r')
        self._FileInput__lines = f.readlines()
        f.close()
        self._FileInput__line_num = 0
        self._FileInput__col_num = 0

    def get_next_char(self):
        line = self._FileInput__lines[self._FileInput__line_num]
        next_char = line[self._FileInput__col_num]
        self._FileInput__col_num += 1
        if self._FileInput__col_num >= len(line):
            self._FileInput__line_num += 1
            self._FileInput__col_num = 0
        return next_char

    def has_next_char(self):
        if self._FileInput__line_num >= len(self._FileInput__lines):
            return False
        else:
            line = self._FileInput__lines[self._FileInput__line_num]
            return self._FileInput__col_num <= len(line) - 1