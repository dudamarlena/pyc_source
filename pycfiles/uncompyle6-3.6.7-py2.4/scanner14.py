# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner14.py
# Compiled at: 2019-04-10 12:00:40
"""
Python 1.4 bytecode decompiler massaging.

This massages tokenized 1.4 bytecode to make it more amenable for
grammar parsing.
"""
import uncompyle6.scanners.scanner15 as scan
from xdis.opcodes import opcode_14
JUMP_OPS = opcode_14.JUMP_OPS

class Scanner14(scan.Scanner15):
    __module__ = __name__

    def __init__(self, show_asm=False):
        scan.Scanner15.__init__(self, show_asm)
        self.opc = opcode_14
        self.opname = opcode_14.opname
        self.version = 1.4
        self.genexpr_name = '<generator expression>'