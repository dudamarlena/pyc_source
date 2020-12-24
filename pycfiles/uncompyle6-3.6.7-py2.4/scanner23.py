# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner23.py
# Compiled at: 2018-06-03 03:21:48
"""
Python 2.3 bytecode massaging.

This massages tokenized 2.3 bytecode to make it more amenable for
grammar parsing.
"""
import uncompyle6.scanners.scanner24 as scan
from xdis.opcodes import opcode_23
JUMP_OPS = opcode_23.JUMP_OPS

class Scanner23(scan.Scanner24):
    __module__ = __name__

    def __init__(self, show_asm=False):
        scan.Scanner24.__init__(self, show_asm)
        self.opc = opcode_23
        self.opname = opcode_23.opname
        self.version = 2.3
        self.genexpr_name = '<generator expression>'