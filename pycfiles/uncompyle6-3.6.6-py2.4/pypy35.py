# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/pypy35.py
# Compiled at: 2019-05-05 16:10:40
"""
Python PyPy 3.5 decompiler scanner.

Does some additional massaging of xdis-disassembled instructions to
make things easier for decompilation.
"""
import uncompyle6.scanners.scanner35 as scan
from xdis.opcodes import opcode_35 as opc
JUMP_OPs = opc.JUMP_OPS

class ScannerPyPy35(scan.Scanner35):
    __module__ = __name__

    def __init__(self, show_asm):
        scan.Scanner35.__init__(self, show_asm, is_pypy=True)
        self.version = 3.5