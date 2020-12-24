# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner10.py
# Compiled at: 2019-10-28 13:18:17
"""
Python 1.0 bytecode decompiler massaging.

This massages tokenized 1.0 bytecode to make it more amenable for
grammar parsing.
"""
import uncompyle6.scanners.scanner11 as scan
from xdis.opcodes import opcode_10
JUMP_OPS = opcode_10.JUMP_OPS

class Scanner10(scan.Scanner11):
    __module__ = __name__

    def __init__(self, show_asm=False):
        scan.Scanner11.__init__(self, show_asm)
        self.opc = opcode_10
        self.opname = opcode_10.opname
        self.version = 1.0