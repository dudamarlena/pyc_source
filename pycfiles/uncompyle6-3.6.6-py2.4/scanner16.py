# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner16.py
# Compiled at: 2019-10-28 13:18:17
"""
Python 1.6 bytecode decompiler massaging.

This massages tokenized 1.6 bytecode to make it more amenable for
grammar parsing.
"""
import uncompyle6.scanners.scanner21 as scan
from xdis.opcodes import opcode_16
JUMP_OPS = opcode_16.JUMP_OPS

class Scanner16(scan.Scanner21):
    __module__ = __name__

    def __init__(self, show_asm=False):
        scan.Scanner21.__init__(self, show_asm)
        self.opc = opcode_16
        self.opname = opcode_16.opname
        self.version = 1.6
        self.genexpr_name = '<generator expression>'

    def ingest(self, co, classname=None, code_objects={}, show_asm=None):
        """
        Pick out tokens from an uncompyle6 code object, and transform them,
        returning a list of uncompyle6 Token's.

        The transformations are made to assist the deparsing grammar.
        """
        (tokens, customize) = scan.Scanner21.ingest(self, co, classname, code_objects, show_asm)
        for t in tokens:
            if t.op == self.opc.UNPACK_LIST:
                t.kind = 'UNPACK_LIST_%d' % t.attr

        return (
         tokens, customize)