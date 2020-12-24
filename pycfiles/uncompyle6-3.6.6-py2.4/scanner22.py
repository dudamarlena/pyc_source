# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner22.py
# Compiled at: 2020-04-20 22:50:15
"""
Python 2.2 bytecode massaging.

This massages tokenized 2.2 bytecode to make it more amenable for
grammar parsing.
"""
import uncompyle6.scanners.scanner23 as scan
from xdis.opcodes import opcode_22
JUMP_OPS = opcode_22.JUMP_OPS

class Scanner22(scan.Scanner23):
    __module__ = __name__

    def __init__(self, show_asm=False):
        scan.Scanner23.__init__(self, show_asm=False)
        self.opc = opcode_22
        self.opname = opcode_22.opname
        self.version = 2.2
        self.genexpr_name = '<generator expression>'
        self.parent_ingest = self.ingest
        self.ingest = self.ingest22

    def ingest22(self, co, classname=None, code_objects={}, show_asm=None):
        (tokens, customize) = self.parent_ingest(co, classname, code_objects, show_asm)
        tokens = [ t for t in tokens if t.kind != 'SET_LINENO' ]
        return (tokens, customize)