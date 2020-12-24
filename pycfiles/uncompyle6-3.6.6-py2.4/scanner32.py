# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner32.py
# Compiled at: 2020-04-20 22:50:15
"""
Python 3.2 bytecode decompiler scanner.

Does some additional massaging of xdis-disassembled instructions to
make things easier for decompilation.

This sets up opcodes Python's 3.2 and calls a generalized
scanner routine for Python 3.
"""
from xdis.opcodes import opcode_32 as opc
JUMP_OPS = opc.JUMP_OPS
from uncompyle6.scanners.scanner3 import Scanner3

class Scanner32(Scanner3):
    __module__ = __name__

    def __init__(self, show_asm=None, is_pypy=False):
        Scanner3.__init__(self, 3.2, show_asm, is_pypy)


if __name__ == '__main__':
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 3.2:
        import inspect
        co = inspect.currentframe().f_code
        (tokens, customize) = Scanner32().ingest(co)
        for t in tokens:
            print t

    else:
        print 'Need to be Python 3.2 to demo; I am %s.' % PYTHON_VERSION