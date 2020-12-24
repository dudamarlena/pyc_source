# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/io/string_input.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 466 bytes
from .input_stream import InputStream

class StringInput(InputStream):

    def __init__(self, string_data):
        self._StringInput__string_data = string_data
        self._StringInput__cursor = -1

    def get_next_char(self):
        self._StringInput__cursor += 1
        if self._StringInput__cursor < len(self._StringInput__string_data):
            return self._StringInput__string_data[self._StringInput__cursor]
        else:
            return

    def has_next_char(self):
        return self._StringInput__cursor + 1 < len(self._StringInput__string_data)