# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/pypy33.py
# Compiled at: 2019-11-10 13:37:14
"""
Python PyPy 3.3 decompiler scanner.

Does some additional massaging of xdis-disassembled instructions to
make things easier for decompilation.
"""
import uncompyle6.scanners.scanner33 as scan
from xdis.opcodes import opcode_33pypy as opc
JUMP_OPs = map(lambda op: opc.opname[op], opc.hasjrel + opc.hasjabs)

class ScannerPyPy33(scan.Scanner33):
    __module__ = __name__

    def __init__(self, show_asm):
        scan.Scanner33.__init__(self, show_asm, is_pypy=True)
        self.version = 3.3
        self.opc = opc