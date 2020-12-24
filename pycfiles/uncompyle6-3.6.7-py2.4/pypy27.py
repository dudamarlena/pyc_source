# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/pypy27.py
# Compiled at: 2017-11-27 13:22:24
"""
Python PyPy 2.7 bytecode scanner/deparser

This overlaps Python's 2.7's dis module, but it can be run from
Python 3 and other versions of Python. Also, we save token
information for later use in deparsing.
"""
import uncompyle6.scanners.scanner27 as scan
from xdis.opcodes import opcode_27pypy
JUMP_OPS = opcode_27pypy.JUMP_OPS

class ScannerPyPy27(scan.Scanner27):
    __module__ = __name__

    def __init__(self, show_asm):
        scan.Scanner27.__init__(self, show_asm, is_pypy=True)
        self.version = 2.7