# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner21.py
# Compiled at: 2020-04-20 22:50:15
"""
Python 2.1 bytecode massaging.

This massages tokenized 2.1 bytecode to make it more amenable for
grammar parsing.
"""
import uncompyle6.scanners.scanner22 as scan
from xdis.opcodes import opcode_21
JUMP_OPS = opcode_21.JUMP_OPS

class Scanner21(scan.Scanner22):
    __module__ = __name__

    def __init__(self, show_asm=False):
        scan.Scanner22.__init__(self, show_asm=False)
        self.opc = opcode_21
        self.opname = opcode_21.opname
        self.version = 2.1
        self.genexpr_name = '<generator expression>'