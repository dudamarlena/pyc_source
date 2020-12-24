# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner25.py
# Compiled at: 2018-06-03 03:21:48
"""
Python 2.5 bytecode massaging.

This overlaps Python's 2.5's dis module, but it can be run from
Python 3 and other versions of Python. Also, we save token
information for later use in deparsing.
"""
import uncompyle6.scanners.scanner26 as scan
from xdis.opcodes import opcode_25
JUMP_OPS = opcode_25.JUMP_OPS

class Scanner25(scan.Scanner26):
    __module__ = __name__

    def __init__(self, show_asm=False):
        self.opc = opcode_25
        self.opname = opcode_25.opname
        scan.Scanner26.__init__(self, show_asm)
        self.version = 2.5