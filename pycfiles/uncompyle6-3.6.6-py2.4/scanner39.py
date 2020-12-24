# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner39.py
# Compiled at: 2019-12-09 22:02:19
"""Python 3.9 bytecode decompiler scanner.

Does some token massaging of xdis-disassembled instructions to make
things easier for decompilation.

This sets up opcodes Python's 3.9 and calls a generalized
scanner routine for Python 3.7 and up.
"""
from uncompyle6.scanners.scanner38 import Scanner38
from uncompyle6.scanners.scanner37base import Scanner37Base
from xdis.opcodes import opcode_38 as opc
JUMP_OPs = opc.JUMP_OPS

class Scanner39(Scanner38):
    __module__ = __name__

    def __init__(self, show_asm=None):
        Scanner37Base.__init__(self, 3.9, show_asm)


if __name__ == '__main__':
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 3.9:
        import inspect
        co = inspect.currentframe().f_code
        (tokens, customize) = Scanner39().ingest(co)
        for t in tokens:
            print t.format()

    else:
        print 'Need to be Python 3.9 to demo; I am %s.' % PYTHON_VERSION