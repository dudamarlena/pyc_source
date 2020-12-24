# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/template.py
# Compiled at: 2009-09-07 17:44:28
"""
====================== 8< ============================
This file is an Hachoir parser template. Make a copy
of it, and adapt it to your needs.

You have to replace all "TODO" with you code.
====================== 8< ============================

TODO parser.

Author: TODO TODO
Creation date: YYYY-mm-DD
"""
from hachoir_parser import Parser
from hachoir_core.field import ParserError, UInt8, UInt16, UInt32, String, RawBytes
from hachoir_core.endian import LITTLE_ENDIAN, BIG_ENDIAN

class TODOFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'TODO', 'category': 'TODO', 'file_ext': ('TODO', ), 'mime': 'TODO', 'min_size': 0, 'description': 'TODO'}

    def validate(self):
        return False

    def createFields(self):
        if self.current_size < self._size:
            yield self.seekBit(self._size, 'end')